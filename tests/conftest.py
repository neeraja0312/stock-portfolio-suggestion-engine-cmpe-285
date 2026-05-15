"""Shared fixtures for pytest (mock prices so tests run offline)."""

import pytest
from unittest.mock import patch

# Fixed prices for deterministic allocation tests
MOCK_PRICES = {
    "VTI": 100.0,
    "IXUS": 50.0,
    "ILTB": 80.0,
    "AAPL": 150.0,
    "ADBE": 400.0,
    "NSRGY": 90.0,
    "MSFT": 300.0,
    "TSLA": 200.0,
    "NVDA": 500.0,
    "AMD": 100.0,
    "NFLX": 400.0,
    "COIN": 150.0,
    "JNJ": 160.0,
    "KO": 60.0,
    "PG": 150.0,
    "UNH": 500.0,
    "BAC": 35.0,
    "F": 12.0,
    "XOM": 100.0,
    "JPM": 180.0,
}

_HISTORY_DATES = [
    "2026-05-05",
    "2026-05-06",
    "2026-05-07",
    "2026-05-08",
    "2026-05-09",
]


def _build_mock_history(base_price: float, drift: float = 1.0):
    """Five trading days of prices around base_price."""
    return {
        date: round(base_price + (i - 2) * drift, 2)
        for i, date in enumerate(_HISTORY_DATES)
    }


MOCK_HISTORY = {
    ticker: _build_mock_history(price, drift=1.0 if price < 200 else 2.0)
    for ticker, price in MOCK_PRICES.items()
}


def _mock_current_prices(tickers):
    return {t: MOCK_PRICES[t] for t in tickers if t in MOCK_PRICES}


def _mock_historical_prices(tickers, days=5):
    return {t: MOCK_HISTORY.get(t, {}) for t in tickers}


@pytest.fixture
def mock_fetcher():
    """Patch app-level fetcher used by Flask routes."""
    with patch("app.fetcher") as fetcher:
        fetcher.get_current_prices.side_effect = _mock_current_prices
        fetcher.get_historical_prices.side_effect = _mock_historical_prices
        yield fetcher


@pytest.fixture
def client(mock_fetcher):
    from app import app

    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def portfolio_with_mocks():
    """Build a Portfolio using mock prices (no Flask)."""
    from core.portfolio import Portfolio

    def _build(amount, strategies):
        tickers = set()
        from config.strategies import STRATEGIES

        for s in strategies:
            tickers.update(STRATEGIES[s]["securities"].keys())
        prices = _mock_current_prices(list(tickers))
        p = Portfolio(amount, strategies)
        p.allocate_portfolio(prices)
        return p, prices

    return _build
