"""
Automated versions of the 10 manual test cases in TEST_CASES.md.

Run offline (no network):
    python3 -m pip install -r requirements-dev.txt
    python3 -m pytest

Run including live Yahoo Finance checks:
    pytest -m integration
"""

import pytest
from config.strategies import STRATEGIES, get_all_strategy_names
from core.validator import validate_investment_amount, validate_strategies
from core.portfolio import Portfolio


# --- Test Case 1: all strategies, >= 3 securities each ---


def test_case_01_all_strategies_have_minimum_securities():
    """Manual TC1 — five strategies, each with at least 3 tickers."""
    assert len(STRATEGIES) == 5
    expected_names = {
        "ethical": "Ethical Investing",
        "growth": "Growth Investing",
        "index": "Index Investing",
        "quality": "Quality Investing",
        "value": "Value Investing",
    }
    for key, display_name in expected_names.items():
        assert key in STRATEGIES
        assert STRATEGIES[key]["name"] == display_name
        assert len(STRATEGIES[key]["securities"]) >= 3

    assert {"AAPL", "ADBE", "NSRGY"} <= set(STRATEGIES["ethical"]["securities"])
    assert {"VTI", "IXUS", "ILTB"} == set(STRATEGIES["index"]["securities"])
    assert {"TSLA", "NVDA", "AMD"} <= set(STRATEGIES["growth"]["securities"])
    assert {"JNJ", "KO", "PG"} <= set(STRATEGIES["quality"]["securities"])
    assert {"BAC", "F", "XOM"} <= set(STRATEGIES["value"]["securities"])


# --- Test Case 2: reject amount below $5000 ---


def test_case_02_reject_investment_below_minimum():
    """Manual TC2 — minimum $5,000 USD."""
    with pytest.raises(ValueError, match="5,000"):
        validate_investment_amount(4999)

    assert validate_investment_amount(5000) is True
    assert validate_investment_amount(10000) is True


# --- Test Case 3: web rejects below minimum ---


def test_case_03_web_rejects_amount_below_minimum(client):
    """Manual TC3 — POST /api/portfolio with amount < $5000."""
    response = client.post(
        "/api/portfolio",
        json={"amount": 1000, "strategies": ["index"]},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "5,000" in data["message"]


# --- Test Case 4: Index Investing, $10,000 ---


def test_case_04_index_investing_single_strategy(portfolio_with_mocks):
    """Manual TC4 — VTI, IXUS, ILTB only; equal split."""
    portfolio, _ = portfolio_with_mocks(10000, ["index"])
    tickers = set(portfolio.holdings.keys())

    assert tickers == {"VTI", "IXUS", "ILTB"}
    for ticker in tickers:
        assert portfolio.holdings[ticker]["strategy"] == "index"
        assert portfolio.holdings[ticker]["allocated_amount"] == pytest.approx(
            10000 / 3, rel=1e-2
        )

    composition = portfolio.get_portfolio_composition()
    assert composition["total_value"] == pytest.approx(10000, rel=1e-2)
    assert len(composition["composition"]["index"]) == 3


# --- Test Case 5: Ethical Investing, $7,500 ---


def test_case_05_ethical_investing_single_strategy(portfolio_with_mocks):
    """Manual TC5 — AAPL, ADBE, NSRGY, MSFT; ~25% each."""
    portfolio, prices = portfolio_with_mocks(7500, ["ethical"])
    tickers = set(portfolio.holdings.keys())

    assert tickers == {"AAPL", "ADBE", "NSRGY", "MSFT"}
    per_stock = 7500 / 4
    for ticker in tickers:
        assert portfolio.holdings[ticker]["allocated_amount"] == pytest.approx(
            per_stock, rel=1e-2
        )
        assert prices[ticker] > 0

    composition = portfolio.get_portfolio_composition()
    assert composition["total_value"] == pytest.approx(7500, rel=1e-2)


# --- Test Case 6: Growth + Value, $20,000 ---


def test_case_06_two_strategies_fifty_fifty_split(portfolio_with_mocks):
    """Manual TC6 — 50% per strategy; 9 total positions."""
    portfolio, _ = portfolio_with_mocks(20000, ["growth", "value"])

    growth_tickers = {"TSLA", "NVDA", "AMD", "NFLX", "COIN"}
    value_tickers = {"BAC", "F", "XOM", "JPM"}
    assert set(portfolio.holdings.keys()) == growth_tickers | value_tickers
    assert len(portfolio.holdings) == 9

    for ticker, holding in portfolio.holdings.items():
        if holding["strategy"] == "growth":
            assert holding["allocated_amount"] == pytest.approx(2000, rel=1e-2)
        else:
            assert holding["allocated_amount"] == pytest.approx(
                2500, rel=1e-2
            )

    breakdown = portfolio.get_strategy_breakdown()
    assert breakdown["growth"] == pytest.approx(10000, rel=1e-2)
    assert breakdown["value"] == pytest.approx(10000, rel=1e-2)


# --- Test Case 7: reject more than two strategies ---


def test_case_07_reject_more_than_two_strategies():
    """Manual TC7 — at most 2 strategies."""
    with pytest.raises(ValueError, match="1 or 2"):
        validate_strategies(["ethical", "growth", "index"])


# --- Test Case 8: reject duplicate strategy ---


def test_case_08_reject_duplicate_strategy():
    """Manual TC8 — same strategy twice."""
    with pytest.raises(ValueError, match="same strategy"):
        validate_strategies(["ethical", "ethical"])


# --- Test Case 9: invalid strategy name ---


def test_case_09_reject_invalid_strategy_name():
    """Manual TC9 — unknown strategy 'crypto'."""
    with pytest.raises(ValueError, match="Invalid strategy"):
        validate_strategies(["crypto"])

    valid = get_all_strategy_names()
    assert set(valid) == {"ethical", "growth", "index", "quality", "value"}


# --- Test Case 10: web success + validation ---


def test_case_10_web_quality_investing_success(client):
    """Manual TC10 Part A — Quality strategy via API."""
    response = client.post(
        "/api/portfolio",
        json={"amount": 15000, "strategies": ["quality"]},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"

    comp = data["composition"]
    tickers = {
        h["ticker"]
        for holdings in comp["composition"].values()
        for h in holdings
    }
    assert tickers == {"JNJ", "KO", "PG", "UNH"}
    assert comp["total_value"] > 0
    assert len(data["history"]) >= 2
    assert data["trend"] is not None
    assert data["trend"]["trend"] in ("UP", "DOWN", "FLAT")


def test_case_10_web_rejects_empty_strategies(client):
    """Manual TC10 Part B — must select 1 or 2 strategies."""
    response = client.post(
        "/api/portfolio",
        json={"amount": 15000, "strategies": []},
    )
    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


# --- Optional: live integration (not part of grader manual steps) ---


@pytest.mark.integration
def test_integration_live_prices_from_yahoo():
    """Optional — verifies yfinance returns positive prices (needs network)."""
    from data.fetcher import StockDataFetcher

    fetcher = StockDataFetcher()
    prices = fetcher.get_current_prices(["VTI", "AAPL"])
    assert prices["VTI"] > 0
    assert prices["AAPL"] > 0
