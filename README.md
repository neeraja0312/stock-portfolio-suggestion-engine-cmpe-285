# Stock Portfolio Suggestion Engine

A Python-based investment portfolio recommendation system that suggests stock/ETF allocations based on selected investment strategies. 

This engine is designed to help users intelligently allocate their investments into curated financial strategies, utilizing real-time financial data to demonstrate current values and simulate short-term historical trends.

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

1. Install the required dependencies (on macOS, use `python3 -m pip` if `pip` is not found):
   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Automated tests (pytest)

The ten manual test cases in `TEST_CASES.md` are also implemented as pytest tests (offline, with mocked prices):

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -v
```

Optional integration test against live Yahoo Finance data:

```bash
python3 -m pytest -m integration -v
```

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
