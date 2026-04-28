"""
Real-time stock data fetching via yfinance API.
"""

import yfinance as yf
from typing import Dict, List
from datetime import datetime, timedelta


class StockDataFetcher:
    """Fetches real-time and historical stock data."""
    
    def __init__(self):
        """Initialize the fetcher."""
        self.cache = {}  # Cache prices to reduce API calls
        self.last_update = {}
        self.cache_duration = 60  # seconds
    
    def get_current_prices(self, tickers: List[str]) -> Dict[str, float]:
        """
        Get current prices for a list of tickers.
        
        Args:
            tickers: List of stock/ETF tickers
            
        Returns:
            Dictionary with {ticker: current_price}
        """
        prices = {}
        tickers_to_fetch = []
        
        # Check cache
        now = datetime.now()
        for ticker in tickers:
            if ticker in self.cache:
                age = (now - self.last_update.get(ticker, now)).total_seconds()
                if age < self.cache_duration:
                    prices[ticker] = self.cache[ticker]
                    continue
            tickers_to_fetch.append(ticker)
        
        # Fetch missing prices
        if tickers_to_fetch:
            try:
                data = yf.download(
                    tickers_to_fetch,
                    period="1d",
                    progress=False
                )
                
                if len(tickers_to_fetch) == 1:
                    # Single ticker returns Series
                    ticker = tickers_to_fetch[0]
                    price = data['Close'].iloc[-1] if len(data) > 0 else 0
                    prices[ticker] = price
                    self.cache[ticker] = price
                    self.last_update[ticker] = now
                else:
                    # Multiple tickers return DataFrame
                    for ticker in tickers_to_fetch:
                        if ticker in data.columns:
                            price = data[ticker]['Close'].iloc[-1] if len(data) > 0 else 0
                        else:
                            price = 0
                        prices[ticker] = price
                        self.cache[ticker] = price
                        self.last_update[ticker] = now
            except Exception as e:
                print(f"Error fetching prices: {e}")
                # Return cached prices if available, otherwise 0
                for ticker in tickers_to_fetch:
                    prices[ticker] = self.cache.get(ticker, 0)
        
        return prices
    
    def get_historical_prices(self, ticker: str, days: int = 5) -> List[Dict]:
        """
        Get historical prices for a ticker.
        
        Args:
            ticker: Stock/ETF ticker
            days: Number of days of history to fetch
            
        Returns:
            List of dictionaries with {date, price}
        """
        try:
            data = yf.download(
                ticker,
                period=f"{days}d",
                progress=False
            )
            
            history = []
            for date, close in data['Close'].items():
                history.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "price": round(float(close), 2)
                })
            
            return history
        except Exception as e:
            print(f"Error fetching historical prices for {ticker}: {e}")
            return []
    
    def clear_cache(self):
        """Clear the price cache."""
        self.cache.clear()
        self.last_update.clear()
