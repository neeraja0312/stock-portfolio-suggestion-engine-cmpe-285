"""
Input validation for portfolio creation and user inputs.
"""

from config.strategies import get_all_strategy_names


def validate_investment_amount(amount: float) -> bool:
    """
    Validate investment amount.
    
    Args:
        amount: Investment amount in USD
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If amount is invalid
    """
    if not isinstance(amount, (int, float)):
        raise ValueError("Investment amount must be a number")
    
    if amount < 5000:
        raise ValueError("Minimum investment amount is $5,000 USD")
    
    if amount <= 0:
        raise ValueError("Investment amount must be positive")
    
    return True


def validate_strategies(strategies: list) -> bool:
    """
    Validate selected strategies.
    
    Args:
        strategies: List of strategy names
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If strategies are invalid
    """
    if not isinstance(strategies, list):
        raise ValueError("Strategies must be a list")
    
    if len(strategies) < 1 or len(strategies) > 2:
        raise ValueError("Must select 1 or 2 strategies")
    
    valid_strategies = get_all_strategy_names()
    for strategy in strategies:
        if strategy.lower() not in valid_strategies:
            raise ValueError(f"Invalid strategy: '{strategy}'. Valid options: {', '.join(valid_strategies)}")
    
    # Check for duplicates
    if len(strategies) == 2 and strategies[0].lower() == strategies[1].lower():
        raise ValueError("Cannot select the same strategy twice")
    
    return True


def validate_ticker(ticker: str) -> bool:
    """
    Basic ticker format validation.
    
    Args:
        ticker: Ticker symbol
        
    Returns:
        True if valid format
    """
    if not isinstance(ticker, str):
        return False
    
    ticker = ticker.strip()
    if len(ticker) < 1 or len(ticker) > 5:
        return False
    
    if not ticker.isupper():
        return False
    
    return True
