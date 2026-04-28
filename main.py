#!/usr/bin/env python3
"""
Main entry point for the Stock Portfolio Suggestion Engine.

Usage:
    python main.py
"""

from ui.cli import PortfolioUI


def main():
    """Main entry point."""
    ui = PortfolioUI()
    ui.run()


if __name__ == "__main__":
    main()
