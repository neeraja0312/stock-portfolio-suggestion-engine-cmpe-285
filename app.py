from flask import Flask, render_template, request, jsonify
from config.strategies import STRATEGIES
from core.portfolio import Portfolio
from core.validator import validate_investment_amount, validate_strategies
from data.fetcher import StockDataFetcher

app = Flask(__name__)
fetcher = StockDataFetcher()

@app.route('/')
def index():
    return render_template('index.html', strategies=STRATEGIES)

@app.route('/api/portfolio', methods=['POST'])
def create_portfolio():
    data = request.json
    try:
        amount = float(data.get('amount', 0))
        strategies = data.get('strategies', [])
        
        validate_investment_amount(amount)
        validate_strategies(strategies)
        
        # Get all tickers needed
        all_tickers = set()
        for strategy in strategies:
            tickers = STRATEGIES[strategy]["securities"].keys()
            all_tickers.update(tickers)
            
        prices = fetcher.get_current_prices(list(all_tickers))
        
        portfolio = Portfolio(amount, strategies)
        portfolio.allocate_portfolio(prices)
        
        # Get historical
        historical_prices = fetcher.get_historical_prices(list(all_tickers), days=5)
        history = portfolio.get_historical_values(historical_prices)
        
        # Trend
        trend_data = None
        if len(history) >= 2:
            values = [h["value"] for h in history]
            first_value = values[0]
            last_value = values[-1]
            change = last_value - first_value
            change_percent = (change / first_value * 100) if first_value > 0 else 0
            trend_str = "UP" if change > 0 else "DOWN" if change < 0 else "FLAT"
            trend_data = {
                "trend": trend_str,
                "change": change,
                "change_percent": change_percent,
                "min": min(values),
                "max": max(values)
            }
        
        return jsonify({
            "status": "success",
            "composition": portfolio.get_portfolio_composition(),
            "history": history,
            "trend": trend_data
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Using port 5001 to avoid macOS Control Center "Access Denied" issue on 5000
    app.run(debug=True, port=5001)
