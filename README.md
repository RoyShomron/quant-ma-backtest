# Quant MA Backtest (SPY)

This project is a beginner quantitative finance backtest model built in Python.  
It downloads historical SPY data while computing daily returns and portfolio growth, and evaluates a simple trend-following strategy.

## Strategy
- Compute 20-day and 50-day moving averages of SPY closing price
- **Invest** when MA20 > MA50
- **Cash** otherwise
- Uses a 1-day signal shift, where yesterday's strategy signal affects today's decisions

## What’s Included
- Data pull with `yfinance`
- Analysis with `pandas`
- Plots with `matplotlib`
- Backtest outputs:
  - equity curve (strategy vs buy-and-hold)
  - drawdown comparison
  - metrics: total return, annualized return, annualized volatility, Sharpe ratio, max drawdown

## How to Run
pip install requirements.txt
python main.py
