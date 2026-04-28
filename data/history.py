"""
Portfolio value history tracking (5-day history).
"""

from datetime import datetime, timedelta
from typing import List, Dict
import json
import os


class PortfolioHistory:
    """Tracks historical portfolio values."""
    
    def __init__(self, history_file: str = ".portfolio_history.json"):
        """
        Initialize history tracker.
        
        Args:
            history_file: File to persist history
        """
        self.history_file = history_file
        self.history = []  # List of {timestamp, date, portfolio_value}
        self._load_history()
    
    def add_entry(self, portfolio_value: float):
        """
        Add current portfolio value to history.
        
        Args:
            portfolio_value: Current total portfolio value
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "value": round(portfolio_value, 2)
        }
        
        # Remove duplicate today entries (keep the latest)
        self.history = [h for h in self.history if h["date"] != entry["date"]]
        self.history.append(entry)
        
        # Keep only last 5 days
        self._prune_history()
        self._save_history()
    
    def get_history(self, days: int = 5) -> List[Dict]:
        """
        Get portfolio value history.
        
        Args:
            days: Number of days of history
            
        Returns:
            List of history entries
        """
        cutoff = datetime.now() - timedelta(days=days)
        return [
            h for h in self.history 
            if datetime.fromisoformat(h["timestamp"]) >= cutoff
        ]
    
    def get_trend(self) -> Dict:
        """
        Get portfolio trend information.
        
        Returns:
            Dictionary with trend metrics
        """
        history = self.get_history(5)
        
        if len(history) < 2:
            return {
                "status": "insufficient_data",
                "message": "Need at least 2 data points for trend"
            }
        
        values = [h["value"] for h in history]
        first_value = values[0]
        last_value = values[-1]
        
        change = last_value - first_value
        change_percent = (change / first_value * 100) if first_value > 0 else 0
        
        trend = "📈 UP" if change > 0 else "📉 DOWN" if change < 0 else "➡️ FLAT"
        
        return {
            "status": "success",
            "trend": trend,
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "start_value": round(first_value, 2),
            "end_value": round(last_value, 2),
            "min_value": round(min(values), 2),
            "max_value": round(max(values), 2),
            "data_points": len(history)
        }
    
    def _prune_history(self, days: int = 5):
        """Remove entries older than specified days."""
        cutoff = datetime.now() - timedelta(days=days)
        self.history = [
            h for h in self.history 
            if datetime.fromisoformat(h["timestamp"]) >= cutoff
        ]
    
    def _save_history(self):
        """Save history to file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save history: {e}")
    
    def _load_history(self):
        """Load history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
                    self._prune_history()  # Remove old entries
        except Exception as e:
            print(f"Warning: Could not load history: {e}")
            self.history = []
    
    def clear_history(self):
        """Clear all history."""
        self.history = []
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
        except:
            pass
