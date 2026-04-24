# Stock Portfolio Suggestion Engine

A Python-based investment portfolio recommendation system that suggests stock/ETF allocations based on selected investment strategies.

## Features

- **Multiple Investment Strategies**: Ethical, Growth, Index, Quality, and Value investing
- **Real-time Stock Data**: Live stock prices via yfinance API
- **Intelligent Money Allocation**: Distributes investment amount across recommended securities
- **Portfolio Tracking**: 5-day historical portfolio value tracking
- **CLI Interface**: User-friendly command-line interface

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Follow the prompts to:
1. Enter investment amount (minimum $5,000)
2. Select 1-2 investment strategies
3. Review portfolio recommendations
4. See current and historical portfolio values

## Project Structure

- `config/` - Strategy definitions and stock/ETF mappings
- `core/` - Core portfolio calculation and allocation logic
- `data/` - Real-time data fetching and historical tracking
- `ui/` - Command-line user interface
