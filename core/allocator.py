"""
Money allocation algorithm.
Determines how to divide investment amount across selected securities.
"""

from typing import Dict, List
from config.strategies import get_strategy_securities


def allocate_securities(investment_amount: float, 
                       selected_strategies: List[str], 
                       current_prices: Dict[str, float]) -> Dict:
    """
    Allocate investment amount across securities from selected strategies.
    
    Allocation Strategy:
    - If 1 strategy: Split equally among all securities in that strategy
    - If 2 strategies: Allocate 50% to each strategy, then split within each
    
    Args:
        investment_amount: Total investment amount
        selected_strategies: List of 1-2 strategy names
        current_prices: Current market prices for all securities
        
    Returns:
        Dictionary with holdings {ticker: {shares, price, strategy}}
    """
    holdings = {}
    
    # Get all securities from selected strategies
    all_securities = {}
    for strategy in selected_strategies:
        securities = get_strategy_securities(strategy)
        all_securities[strategy] = securities
    
    # Allocate money
    if len(selected_strategies) == 1:
        # Single strategy: allocate all to this strategy
        strategy = selected_strategies[0]
        holdings = _allocate_within_strategy(
            strategy, 
            all_securities[strategy], 
            investment_amount, 
            current_prices
        )
    else:
        # Two strategies: 50% each
        per_strategy_amount = investment_amount / 2
        
        for strategy in selected_strategies:
            holdings_for_strategy = _allocate_within_strategy(
                strategy,
                all_securities[strategy],
                per_strategy_amount,
                current_prices
            )
            holdings.update(holdings_for_strategy)
    
    return holdings


def _allocate_within_strategy(strategy: str, 
                             securities: Dict, 
                             amount: float,
                             current_prices: Dict[str, float]) -> Dict:
    """
    Allocate a given amount equally among securities in a strategy.
    
    Args:
        strategy: Strategy name
        securities: Dictionary of securities in this strategy
        amount: Amount to allocate to this strategy
        current_prices: Current market prices
        
    Returns:
        Dictionary with holdings for this strategy
    """
    holdings = {}
    num_securities = len(securities)
    
    if num_securities == 0:
        return holdings
    
    # Equal allocation per security
    amount_per_security = amount / num_securities
    
    for ticker in securities:
        price = current_prices.get(ticker, 0)
        if price <= 0:
            continue
        
        # Calculate shares that can be bought with allocated amount
        shares = amount_per_security / price
        
        holdings[ticker] = {
            "shares": shares,
            "price": price,
            "strategy": strategy,
            "allocated_amount": amount_per_security
        }
    
    return holdings


def calculate_allocation_percentages(holdings: Dict) -> Dict[str, float]:
    """
    Calculate percentage allocation by current value.
    
    Args:
        holdings: Dictionary of holdings {ticker: {shares, price, ...}}
        
    Returns:
        Dictionary with {ticker: percentage}
    """
    total_value = sum(h["shares"] * h["price"] for h in holdings.values())
    
    if total_value == 0:
        return {}
    
    return {
        ticker: round((h["shares"] * h["price"] / total_value) * 100, 2)
        for ticker, h in holdings.items()
    }
