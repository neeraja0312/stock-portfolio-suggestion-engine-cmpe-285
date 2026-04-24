"""
Core portfolio management and calculation logic.
This module handles all portfolio value calculations, composition, and analytics.
"""

from typing import Dict, List, Tuple
from config.strategies import get_strategy_securities


class Portfolio:
    """Manages portfolio composition, allocation, and calculations."""
    
    def __init__(self, investment_amount: float, selected_strategies: List[str]):
        """
        Initialize portfolio with investment amount and strategies.
        
        Args:
            investment_amount: Total amount to invest (must be >= $5000)
            selected_strategies: List of 1-2 strategy names (e.g., ["ethical", "growth"])
        """
        self.investment_amount = investment_amount
        self.selected_strategies = [s.lower() for s in selected_strategies]
        self.holdings = {}  # {ticker: {"shares": X, "price": Y, "strategy": Z}}
        self.current_values = {}  # {ticker: current_price}
        self._validate_input()
    
    def _validate_input(self):
        """Validate portfolio inputs."""
        from core.validator import validate_investment_amount, validate_strategies
        validate_investment_amount(self.investment_amount)
        validate_strategies(self.selected_strategies)
    
    def allocate_portfolio(self, current_prices: Dict[str, float]) -> Dict:
        """
        Allocate investment across selected securities.
        
        Args:
            current_prices: Dictionary of {ticker: current_price}
            
        Returns:
            Dictionary with allocation details
        """
        from core.allocator import allocate_securities
        
        self.current_values = current_prices
        self.holdings = allocate_securities(
            self.investment_amount,
            self.selected_strategies,
            current_prices
        )
        
        return self._get_allocation_summary()
    
    def get_portfolio_composition(self) -> Dict:
        """
        Get detailed portfolio composition.
        
        Returns:
            Dictionary with holdings breakdown by strategy and total allocation
        """
        composition = {}
        total_value = 0
        
        for ticker, holding in self.holdings.items():
            current_value = holding["shares"] * self.current_values.get(ticker, 0)
            total_value += current_value
            strategy = holding["strategy"]
            
            if strategy not in composition:
                composition[strategy] = []
            
            composition[strategy].append({
                "ticker": ticker,
                "shares": round(holding["shares"], 2),
                "purchase_price": round(holding["price"], 2),
                "current_price": round(self.current_values.get(ticker, 0), 2),
                "position_value": round(current_value, 2)
            })
        
        return {
            "composition": composition,
            "total_value": round(total_value, 2),
            "gain_loss": round(total_value - self.investment_amount, 2),
            "return_percentage": round(((total_value - self.investment_amount) / self.investment_amount * 100), 2) if self.investment_amount else 0
        }
    
    def get_current_portfolio_value(self) -> float:
        """Calculate current total portfolio value."""
        total = 0
        for ticker, holding in self.holdings.items():
            total += holding["shares"] * self.current_values.get(ticker, 0)
        return round(total, 2)
    
    def update_prices(self, new_prices: Dict[str, float]):
        """Update current market prices for all holdings."""
        self.current_values.update(new_prices)
    
    def _get_allocation_summary(self) -> Dict:
        """Get summary of allocation."""
        summary = {
            "investment_amount": self.investment_amount,
            "strategies": self.selected_strategies,
            "holdings": self.holdings,
            "total_allocated": sum(h["shares"] * h["price"] for h in self.holdings.values())
        }
        return summary
    
    def get_strategy_breakdown(self) -> Dict[str, float]:
        """
        Get portfolio value breakdown by strategy.
        
        Returns:
            Dictionary with {strategy_name: total_value}
        """
        breakdown = {}
        for ticker, holding in self.holdings.items():
            strategy = holding["strategy"]
            value = holding["shares"] * self.current_values.get(ticker, 0)
            
            if strategy not in breakdown:
                breakdown[strategy] = 0
            breakdown[strategy] += value
        
        return {k: round(v, 2) for k, v in breakdown.items()}
