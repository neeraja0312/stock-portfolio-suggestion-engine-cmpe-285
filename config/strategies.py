"""
Investment strategy definitions and stock/ETF mappings.
Each strategy maps to at least 3 stocks or ETFs.
"""

STRATEGIES = {
    "ethical": {
        "name": "Ethical Investing",
        "description": "Focus on companies with strong environmental, social, and governance practices",
        "securities": {
            "AAPL": {"name": "Apple Inc.", "weight": 0.25, "type": "stock"},
            "ADBE": {"name": "Adobe Inc.", "weight": 0.25, "type": "stock"},
            "NSRGY": {"name": "Nestle SA", "weight": 0.25, "type": "stock"},
            "MSFT": {"name": "Microsoft Corporation", "weight": 0.25, "type": "stock"},
        }
    },
    "growth": {
        "name": "Growth Investing",
        "description": "Target companies with strong growth potential and earnings potential",
        "securities": {
            "TSLA": {"name": "Tesla Inc.", "weight": 0.20, "type": "stock"},
            "NVDA": {"name": "NVIDIA Corporation", "weight": 0.20, "type": "stock"},
            "AMD": {"name": "Advanced Micro Devices", "weight": 0.20, "type": "stock"},
            "NFLX": {"name": "Netflix Inc.", "weight": 0.20, "type": "stock"},
            "COIN": {"name": "Coinbase Global", "weight": 0.20, "type": "stock"},
        }
    },
    "index": {
        "name": "Index Investing",
        "description": "Passive indexing strategy through diversified ETFs",
        "securities": {
            "VTI": {"name": "Vanguard Total Stock Market ETF", "weight": 0.40, "type": "etf"},
            "IXUS": {"name": "iShares Core MSCI Total Intl Stock", "weight": 0.30, "type": "etf"},
            "ILTB": {"name": "iShares Core 10+ Year USD Bond", "weight": 0.30, "type": "etf"},
        }
    },
    "quality": {
        "name": "Quality Investing",
        "description": "Focus on financially stable companies with strong fundamentals",
        "securities": {
            "JNJ": {"name": "Johnson & Johnson", "weight": 0.25, "type": "stock"},
            "KO": {"name": "The Coca-Cola Company", "weight": 0.25, "type": "stock"},
            "PG": {"name": "Procter & Gamble", "weight": 0.25, "type": "stock"},
            "UNH": {"name": "UnitedHealth Group", "weight": 0.25, "type": "stock"},
        }
    },
    "value": {
        "name": "Value Investing",
        "description": "Target undervalued companies trading below intrinsic value",
        "securities": {
            "BAC": {"name": "Bank of America", "weight": 0.25, "type": "stock"},
            "F": {"name": "Ford Motor Company", "weight": 0.25, "type": "stock"},
            "XOM": {"name": "Exxon Mobil Corporation", "weight": 0.25, "type": "stock"},
            "JPM": {"name": "JPMorgan Chase & Co.", "weight": 0.25, "type": "stock"},
        }
    }
}

def get_strategy_securities(strategy_key):
    """Get all securities for a given strategy."""
    if strategy_key.lower() not in STRATEGIES:
        raise ValueError(f"Strategy '{strategy_key}' not found")
    return STRATEGIES[strategy_key.lower()]["securities"]

def get_all_strategy_names():
    """Get list of all available strategy names."""
    return list(STRATEGIES.keys())

def get_strategy_description(strategy_key):
    """Get description of a strategy."""
    if strategy_key.lower() not in STRATEGIES:
        raise ValueError(f"Strategy '{strategy_key}' not found")
    return STRATEGIES[strategy_key.lower()]
