"""
Command-line user interface for the portfolio suggestion engine.
"""

import sys
from typing import List, Tuple
from config.strategies import STRATEGIES, get_all_strategy_names
from core.portfolio import Portfolio
from core.validator import validate_investment_amount, validate_strategies
from data.fetcher import StockDataFetcher
from data.history import PortfolioHistory


class PortfolioUI:
    """Command-line interface for portfolio management."""
    
    def __init__(self):
        """Initialize the UI."""
        self.fetcher = StockDataFetcher()
        self.portfolio = None
    
    def display_welcome(self):
        """Display welcome message."""
        print("\n" + "="*70)
        print("         STOCK PORTFOLIO SUGGESTION ENGINE")
        print("="*70)
        print("\nWelcome! This engine will help you build an investment portfolio")
        print("based on your investment amount and preferred strategies.\n")
    
    def get_investment_amount(self) -> float:
        """
        Get investment amount from user.
        
        Returns:
            Valid investment amount (>= $5000)
        """
        while True:
            try:
                amount_str = input("Enter investment amount (USD, minimum $5,000): $")
                amount = float(amount_str.replace(",", ""))
                validate_investment_amount(amount)
                return amount
            except ValueError as e:
                print(f"❌ Invalid input: {e}")
                print("   Please enter a number >= $5,000\n")
    
    def display_strategies(self):
        """Display available investment strategies."""
        print("\n" + "-"*70)
        print("AVAILABLE INVESTMENT STRATEGIES")
        print("-"*70)
        
        strategies = get_all_strategy_names()
        for i, strategy in enumerate(strategies, 1):
            info = STRATEGIES[strategy]
            print(f"\n{i}. {info['name'].upper()}")
            print(f"   {info['description']}")
            print(f"   Securities: {', '.join(info['securities'].keys())}")
    
    def get_strategies(self) -> List[str]:
        """
        Get 1-2 strategies from user.
        
        Returns:
            List of 1-2 strategy names
        """
        strategies = get_all_strategy_names()
        self.display_strategies()
        
        selected = []
        print("\n" + "-"*70)
        
        while True:
            prompt = f"Select 1 or 2 strategies (comma-separated, e.g., '1, 4' or 'ethical, value'): "
            user_input = input(prompt).strip().lower()
            
            # Split by comma
            parts = [p.strip() for p in user_input.split(',')]
            
            if len(parts) < 1 or len(parts) > 2:
                print("❌ Please enter exactly 1 or 2 strategies.\n")
                continue
                
            selected = []
            invalid = False
            for part in parts:
                if not part:
                    invalid = True
                    break
                if part.isdigit():
                    idx = int(part) - 1
                    if 0 <= idx < len(strategies):
                        selected.append(strategies[idx])
                    else:
                        print(f"❌ Invalid selection number: {part}")
                        invalid = True
                        break
                else:
                    if part in strategies:
                        selected.append(part)
                    else:
                        print(f"❌ Invalid strategy name: {part}")
                        invalid = True
                        break
            
            if invalid:
                print("Please try again.\n")
                continue
                
            # Check for duplicates
            if len(selected) == 2 and selected[0] == selected[1]:
                print("❌ Cannot select the same strategy twice. Please try again.\n")
                continue
                
            break
            
        print(f"✓ Selected: {', '.join([STRATEGIES[s]['name'] for s in selected])}\n")
        
        try:
            validate_strategies(selected)
            return selected
        except ValueError as e:
            print(f"❌ {e}")
            return self.get_strategies()
    
    def create_portfolio(self, amount: float, strategies: List[str]) -> Portfolio:
        """
        Create portfolio and allocate funds.
        
        Args:
            amount: Investment amount
            strategies: Selected strategies
            
        Returns:
            Allocated portfolio object
        """
        print("\n" + "-"*70)
        print("CREATING PORTFOLIO...")
        print("-"*70)
        
        # Get all tickers needed
        all_tickers = set()
        for strategy in strategies:
            tickers = STRATEGIES[strategy]["securities"].keys()
            all_tickers.update(tickers)
        
        print(f"\nFetching current prices for {len(all_tickers)} securities...")
        prices = self.fetcher.get_current_prices(list(all_tickers))
        
        # Create and allocate portfolio
        portfolio = Portfolio(amount, strategies)
        portfolio.allocate_portfolio(prices)
        
        self.portfolio = portfolio
        return portfolio
    
    def display_portfolio_summary(self, portfolio: Portfolio):
        """Display portfolio allocation summary."""
        print("\n" + "="*70)
        print("PORTFOLIO ALLOCATION")
        print("="*70)
        
        composition = portfolio.get_portfolio_composition()
        
        print(f"\nTotal Investment: ${portfolio.investment_amount:,.2f}")
        print(f"Current Portfolio Value: ${composition['total_value']:,.2f}")
        print(f"Gain/Loss: ${composition['gain_loss']:,.2f} ({composition['return_percentage']:.2f}%)")
        
        print("\n" + "-"*70)
        print("HOLDINGS BY STRATEGY")
        print("-"*70)
        
        for strategy, holdings in composition["composition"].items():
            strategy_info = STRATEGIES[strategy]
            print(f"\n{strategy_info['name'].upper()}")
            print("-" * 70)
            
            total_strategy_value = sum(h["position_value"] for h in holdings)
            print(f"Strategy Total: ${total_strategy_value:,.2f}\n")
            
            print(f"{'Ticker':<8} {'Shares':<12} {'Price':<12} {'Value':<15} {'Gain/Loss':<12}")
            print("-" * 70)
            
            for holding in holdings:
                shares = holding["shares"]
                current_price = holding["current_price"]
                purchase_price = holding["purchase_price"]
                position_value = holding["position_value"]
                gain_loss = position_value - (shares * purchase_price)
                
                print(f"{holding['ticker']:<8} {shares:<12.2f} ${current_price:<11.2f} "
                      f"${position_value:<14.2f} ${gain_loss:<11.2f}")
    
    def display_portfolio_history(self):
        """Display portfolio value history and trend."""
        print("\n" + "="*70)
        print("PORTFOLIO HISTORY & TREND (Last 5 Days)")
        print("="*70)
        
        if not self.portfolio:
            return
            
        tickers = list(self.portfolio.holdings.keys())
        print(f"\nFetching historical prices for {len(tickers)} securities...")
        historical_prices = self.fetcher.get_historical_prices(tickers, days=5)
        history = self.portfolio.get_historical_values(historical_prices)
        
        if not history:
            print("\nCould not retrieve historical data.")
            return
            
        print("\nDaily Portfolio Values:")
        print("-" * 70)
        print(f"{'Date':<15} {'Value':<15}")
        print("-" * 70)
        
        for entry in history:
            print(f"{entry['date']:<15} ${entry['value']:<14,.2f}")
            
        if len(history) >= 2:
            values = [h["value"] for h in history]
            first_value = values[0]
            last_value = values[-1]
            change = last_value - first_value
            change_percent = (change / first_value * 100) if first_value > 0 else 0
            trend = "📈 UP" if change > 0 else "📉 DOWN" if change < 0 else "➡️ FLAT"
            
            print("\n" + "-" * 70)
            print("TREND ANALYSIS")
            print("-" * 70)
            print(f"Trend: {trend}")
            print(f"Change: ${change:,.2f} ({change_percent:.2f}%)")
            print(f"Range: ${min(values):,.2f} - ${max(values):,.2f}")
    
    def run(self):
        """Run the main interactive loop."""
        try:
            self.display_welcome()
            
            # Get user inputs
            amount = self.get_investment_amount()
            strategies = self.get_strategies()
            
            # Create and display portfolio
            portfolio = self.create_portfolio(amount, strategies)
            self.display_portfolio_summary(portfolio)
            
            # Display historical trend
            self.display_portfolio_history()
            
            print("\n" + "="*70)
            print("Thank you for using the Portfolio Suggestion Engine!")
            print("="*70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nExiting... Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            sys.exit(1)
