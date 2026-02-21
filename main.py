# Import required libraries
# yfinance for downloading market data
# pandas for data manipulation
# matplotlib for plotting results
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# ===== Performance metric functions =====

# Total return from a cumulative growth series
def total_return(cumulative_series):
    return cumulative_series.iloc[-1] - 1


# Annualized return using average daily return and compounding
def annualized_return(daily_returns, trading_days=252):
    return (1 + daily_returns.mean()) ** trading_days - 1


# Annualized volatility based on daily return and standard deviation
def annualized_vol(daily_returns, trading_days=252):
    return daily_returns.std() * (trading_days ** 0.5)


# Sharpe ratio (risk-based reward)
def sharpe_ratio(daily_returns, trading_days=252, risk_free_rate=0.0):
    excess = daily_returns - (risk_free_rate / trading_days)
    vol = annualized_vol(excess, trading_days)
    return (excess.mean() * trading_days) / vol if vol != 0 else 0


# Maximum drawdown (worst peak-to-trough decline)
def max_drawdown(cumulative_series):
    running_max = cumulative_series.cummax()
    drawdown = cumulative_series / running_max - 1
    return drawdown.min()


# ===== Download historical SPY data =====
df = yf.download(tickers="SPY", period="1y")

# Preview raw data
print(df.head(5))

# ===== Buy-and-hold returns =====

# Daily percentage returns
df["Return"] = df["Close"].pct_change()

# Growth of $1 invested (Compounding)
df["Cumulative"] = (1 + df["Return"]).cumprod()

# Preview columns
print(df[["Close", "Return", "Cumulative"]].head(10))


# Plot buy-and-hold equity curve
df["Cumulative"].plot(title="Growth of $1 Invested in SPY (1Y)")
plt.show()


# ===== Moving averages for strategy =====

# Short-term and long-term moving averages
df["MA20"] = df["Close"].rolling(window=20).mean()
df["MA50"] = df["Close"].rolling(window=50).mean()

# Plot price with moving averages
df[["Close", "MA20", "MA50"]].plot(title="SPY with Moving Averages (1Y)")
plt.show()


# ===== Generate trading signals =====

# Signal = 1 when MA20 > MA50, else 0
df["Signal"] = (df["MA20"] > df["MA50"]).astype(int)

# Shift signal forward 1 day to avoid look-ahead bias
df["Position"] = df["Signal"].shift(1)


# ===== Strategy performance =====

# Strategy returns only when invested
df["StrategyReturn"] = df["Return"] * df["Position"]

# Strategy cumulative growth
df["StrategyCumulative"] = (1 + df["StrategyReturn"]).cumprod()


# ===== Series for metric calculations =====
market_ret = df["Return"].dropna()
market_cum = df["Cumulative"].dropna()
strat_ret = df["StrategyReturn"].dropna()
strat_cum = df["StrategyCumulative"].dropna()


# ===== Print buy-and-hold metrics =====
print("\n===== Buy & Hold (SPY) =====")
print(f"Total Market Return: {total_return(market_cum): .2%}")
print(f"Annual Market Return: {annualized_return(market_ret): .2%}")
print(f"Annual Market Volatility: {annualized_vol(market_ret): .2%}")
print(f"Market Sharpe Ratio: {sharpe_ratio(market_ret): .2f}")
print(f"Max Market Drawdown: {max_drawdown(market_cum): .2%}")


# ===== Print strategy metrics =====
print("\n===== Strategy (MA20 > MA50) =====")
print(f"Total Strategic Return: {total_return(strat_cum): .2%}")
print(f"Annual Strategic Return: {annualized_return(strat_ret): .2%}")
print(f"Annual Strategic Volatility: {annualized_vol(strat_ret): .2%}")
print(f"Strategic Sharpe Ratio: {sharpe_ratio(strat_ret): .2f}")
print(f"Max Strategic Drawdown: {max_drawdown(strat_cum): .2%}")


# ===== Plot drawdowns =====
df["Market Drawdown"] = df["Cumulative"] / df["Cumulative"].cummax() - 1
df["Strategy Drawdown"] = df["StrategyCumulative"] / df["StrategyCumulative"].cummax() - 1

df[["Market Drawdown", "Strategy Drawdown"]].plot(title="Market vs. Strategy Drawdown Plot")
plt.show()