document.addEventListener('DOMContentLoaded', () => {
    const strategyCards = document.querySelectorAll('.strategy-card');
    const amountInput = document.getElementById('amount');
    const generateBtn = document.getElementById('generate-btn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');
    const errorMsg = document.getElementById('error-message');
    const resultsPanel = document.getElementById('results-panel');
    
    let selectedStrategies = [];
    let trendChart = null;

    // Handle strategy selection
    strategyCards.forEach(card => {
        card.addEventListener('click', () => {
            const strategy = card.dataset.strategy;
            
            if (selectedStrategies.includes(strategy)) {
                selectedStrategies = selectedStrategies.filter(s => s !== strategy);
                card.classList.remove('selected');
            } else {
                if (selectedStrategies.length >= 2) {
                    // Remove first selected to allow new one
                    const first = selectedStrategies.shift();
                    document.querySelector(`.strategy-card[data-strategy="${first}"]`).classList.remove('selected');
                }
                selectedStrategies.push(strategy);
                card.classList.add('selected');
            }
        });
    });

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
    };

    generateBtn.addEventListener('click', async () => {
        const amount = parseFloat(amountInput.value);
        
        if (isNaN(amount) || amount < 5000) {
            showError("Investment amount must be at least $5,000.");
            return;
        }
        if (selectedStrategies.length === 0) {
            showError("Please select 1 or 2 investment strategies.");
            return;
        }

        // UI Loading State
        errorMsg.classList.add('hidden');
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        generateBtn.disabled = true;
        resultsPanel.classList.add('hidden');

        try {
            const response = await fetch('/api/portfolio', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    amount: amount,
                    strategies: selectedStrategies
                })
            });

            const data = await response.json();

            if (data.status === 'success') {
                renderResults(data);
            } else {
                showError(data.message || "An error occurred.");
            }
        } catch (err) {
            showError("Failed to connect to the server.");
        } finally {
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
            generateBtn.disabled = false;
        }
    });

    function showError(msg) {
        errorMsg.textContent = msg;
        errorMsg.classList.remove('hidden');
    }

    function renderResults(data) {
        resultsPanel.classList.remove('hidden');
        
        const comp = data.composition;
        
        // Render Summary
        document.getElementById('res-investment').textContent = formatCurrency(comp.total_value - comp.gain_loss); // original investment
        document.getElementById('res-current-value').textContent = formatCurrency(comp.total_value);
        
        const gainEl = document.getElementById('res-gain');
        const gainSign = comp.gain_loss >= 0 ? '+' : '';
        gainEl.textContent = `${gainSign}${formatCurrency(comp.gain_loss)} (${comp.return_percentage}%)`;
        gainEl.className = `value ${comp.gain_loss >= 0 ? 'positive' : 'negative'}`;

        // Render Holdings
        const holdingsList = document.getElementById('holdings-list');
        holdingsList.innerHTML = '';
        
        for (const [strategy, holdings] of Object.entries(comp.composition)) {
            const group = document.createElement('div');
            group.className = 'strategy-group';
            
            const title = document.createElement('h4');
            title.textContent = strategy.toUpperCase();
            group.appendChild(title);
            
            holdings.forEach(h => {
                const gainLoss = h.position_value - (h.shares * h.purchase_price);
                const isPositive = gainLoss >= 0;
                
                const item = document.createElement('div');
                item.className = 'holding-item';
                item.innerHTML = `
                    <div class="holding-info">
                        <span class="holding-ticker">${h.ticker}</span>
                        <span class="holding-shares">${h.shares.toFixed(2)} shares @ ${formatCurrency(h.current_price)}</span>
                    </div>
                    <div class="holding-values">
                        <div class="holding-total">${formatCurrency(h.position_value)}</div>
                        <div class="holding-gain ${isPositive ? 'positive' : 'negative'}">
                            ${isPositive ? '+' : ''}${formatCurrency(gainLoss)}
                        </div>
                    </div>
                `;
                group.appendChild(item);
            });
            holdingsList.appendChild(group);
        }

        // Render Chart
        renderChart(data.history);
        
        // Render Trend Stats
        if (data.trend) {
            const statsEl = document.getElementById('trend-stats');
            const trendSign = data.trend.change >= 0 ? '+' : '';
            statsEl.innerHTML = `
                <div class="trend-stat">
                    <span>Trend</span>
                    <strong>${data.trend.trend === 'UP' ? '📈 UP' : data.trend.trend === 'DOWN' ? '📉 DOWN' : '➡️ FLAT'}</strong>
                </div>
                <div class="trend-stat">
                    <span>Change</span>
                    <strong class="${data.trend.change >= 0 ? 'positive' : 'negative'}">
                        ${trendSign}${formatCurrency(data.trend.change)} (${data.trend.change_percent.toFixed(2)}%)
                    </strong>
                </div>
            `;
        }
        
        // Scroll to results
        resultsPanel.scrollIntoView({ behavior: 'smooth' });
    }

    function renderChart(history) {
        const ctx = document.getElementById('trendChart').getContext('2d');
        
        if (trendChart) {
            trendChart.destroy();
        }

        if (!history || history.length === 0) return;

        const labels = history.map(h => h.date);
        const values = history.map(h => h.value);
        
        const isPositive = values[values.length - 1] >= values[0];
        const lineColor = isPositive ? '#10b981' : '#ef4444';
        const bgColor = isPositive ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)';

        trendChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Portfolio Value',
                    data: values,
                    borderColor: lineColor,
                    backgroundColor: bgColor,
                    borderWidth: 3,
                    pointBackgroundColor: lineColor,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#f8fafc',
                        bodyColor: '#e2e8f0',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return formatCurrency(context.parsed.y);
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { 
                            color: '#94a3b8',
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }
});
