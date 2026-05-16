# Stock Portfolio Suggestion Engine

A Python-based investment portfolio recommendation system that suggests stock/ETF allocations based on selected investment strategies. 

This engine is designed to help users intelligently allocate their investments into curated financial strategies, utilizing real-time financial data to demonstrate current values and simulate short-term historical trends.

## Team Members

Neeraja Abhinav Buch (018178238)
Tanisha Ashishbhai Dave (019110351)
Deven Jaimin Desai (018286944)
Mokshit Chopra (018344482)

## Features

- **Multiple Investment Strategies**:
  - *Ethical Investing*: Focuses on companies with strong environmental, social, and governance (ESG) practices (e.g., AAPL, ADBE, NSRGY).
  - *Growth Investing*: Targets companies with strong growth potential and earnings (e.g., TSLA, NVDA, AMD).
  - *Index Investing*: A passive indexing strategy using diversified ETFs (e.g., VTI, IXUS, ILTB).
  - *Quality Investing*: Focuses on financially stable companies with strong fundamentals (e.g., JNJ, KO, PG).
  - *Value Investing*: Targets undervalued companies trading below their intrinsic value (e.g., BAC, F, XOM).
- **Real-time Stock Data**: Fetches live, up-to-the-minute stock and ETF prices using the `yfinance` API.
- **Intelligent Money Allocation**: Distributes the inputted investment amount across the recommended securities for your chosen strategies (equally splitting funds).
- **Simulated Portfolio Tracking**: Displays a 5-day historical trend analysis of your *suggested* portfolio, helping you understand how it would have performed over the past week.
- **CLI Interface**: User-friendly, interactive command-line interface.

## Requirements

- Python 3.8+
- Active internet connection (to fetch live stock data via Yahoo Finance)

## Installation

**Python Version Required:** Python 3.8 or higher

### Step 1: Create & Activate Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows
```

### Step 2: Install Dependencies

For general use (CLI and web UI):
```bash
python -m pip install -r requirements.txt
```

For development and testing (includes test dependencies):
```bash
python -m pip install -r requirements-dev.txt
```

This installs:
- `pytest` - Testing framework (dev only)
- All packages from `requirements.txt`
- On macOS, if `pip` is not found, use `python3 -m pip` instead

## Testing

### Test Files Location

- **Main test file**: `tests/test_term_project_cases.py` (10 automated test cases)
- **Test fixtures**: `tests/conftest.py` (mock data and Flask test client setup)

### Prerequisites

Ensure you've completed the [Installation](#installation) steps above, including installing dev dependencies from `requirements-dev.txt`.

### Running the Tests

**Run all 10 test cases (offline, mocked prices):**
```bash
python -m pytest tests/test_term_project_cases.py -v
```

**Expected Output (all 10 should pass):**
```
tests/test_term_project_cases.py::test_case_01_all_strategies_have_minimum_securities PASSED
tests/test_term_project_cases.py::test_case_02_reject_investment_below_minimum PASSED
tests/test_term_project_cases.py::test_case_03_web_rejects_amount_below_minimum PASSED
tests/test_term_project_cases.py::test_case_04_index_investing_single_strategy PASSED
tests/test_term_project_cases.py::test_case_05_ethical_investing_single_strategy PASSED
tests/test_term_project_cases.py::test_case_06_two_strategies_fifty_fifty_split PASSED
tests/test_term_project_cases.py::test_case_07_reject_more_than_two_strategies PASSED
tests/test_term_project_cases.py::test_case_08_reject_duplicate_strategy PASSED
tests/test_term_project_cases.py::test_case_09_reject_invalid_strategy_name PASSED
tests/test_term_project_cases.py::test_case_10_web_quality_investing_success PASSED
======================== 10 passed in X.XXs ========================
```

### Test Cases Overview

The 10 automated test cases validate:

| Test # | Name | Coverage |
|--------|------|----------|
| 1 | Strategy Configuration | All 5 strategies exist with ≥3 securities |
| 2 | Backend Validation | Reject investment amounts < $5,000 |
| 3 | API Validation | Web endpoint rejects < $5,000 |
| 4 | Index Strategy | $10K equal split across VTI, IXUS, ILTB |
| 5 | Ethical Strategy | $7.5K allocation to ethical holdings |
| 6 | Multi-Strategy | $20K 50/50 Growth + Value split (9 positions) |
| 7 | Max Strategies | Reject selection of 3+ strategies |
| 8 | Duplicate Check | Reject same strategy selected twice |
| 9 | Invalid Strategy | Reject unknown strategy names |
| 10 | API Success | Quality strategy returns complete portfolio |

**Optional: Integration Test (requires internet connection)**

To test against live Yahoo Finance data:
```bash
python -m pytest tests/test_term_project_cases.py -m integration -v
```

This verifies the system can fetch real current prices for VTI and AAPL.

## Usage

Start the suggestion engine by running:

### Option 1: Command-Line Interface (CLI)
Start the CLI suggestion engine by running:

```bash
python main.py
```

### Option 2: Web Interface (GUI)
Start the beautiful, interactive web interface by running:

```bash
python app.py
```
Then open your browser and navigate to `http://127.0.0.1:5001`

### Step-by-Step Instructions

1. **Enter Investment Amount**: Input the dollar amount you wish to invest in USD. The engine requires a minimum investment of $5,000.
2. **Select Strategies**: Pick one or two investment strategies from the displayed list by typing the name or the corresponding number.
3. **Review Allocation**: The engine will calculate how your money is divided to buy the suggested stocks/ETFs, presenting the current values and the resulting gain/loss.
4. **View Trend Analysis**: The engine will automatically generate a 5-day historical trend of the overall suggested portfolio value.

## Project Structure

- `main.py` - The entry point of the application.
- `config/` - Contains `strategies.py` with definitions and stock/ETF mappings.
- `core/` - Handles core logic: validation, portfolio generation, and money allocation algorithms.
- `data/` - Manages real-time data fetching and historical price tracking from Yahoo Finance.
- `ui/` - Contains the command-line user interface and formatting logic.
