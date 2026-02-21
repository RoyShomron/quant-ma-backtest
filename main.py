import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def total_return(cumulative_series):
    return cumulative_series.iloc[-1] - 1

def annualized_return(daily_returns, trading_days=252):
    return (1 + daily_returns.mean()) ** trading_days - 1

def annualized_vol(daily_returns, trading_days=252):
    return daily_returns.std() * (trading_days ** 0.5)

def sharpe_ratio(daily_returns, trading_days=252, risk_free_rate=0.0):
    excess = daily_returns - (risk_free_rate / trading_days)
    vol = annualized_vol(excess, trading_days)
    return (excess.mean() * trading_days) / vol if vol != 0 else 0

def max_drawdown(cumulative_series):
    running_max = cumulative_series.cummax()
    drawdown = cumulative_series / running_max - 1
    return drawdown.min()

df = yf.download(tickers="SPY", period="1y")

print(df.head(5))

df["Return"] = df["Close"].pct_change()

df["Cumulative"] = (1 + df["Return"]).cumprod()

print(df[["Close", "Return", "Cumulative"]].head(10))

df["Cumulative"].plot(title="Growth of $1 Invested in SPY (1Y)")
plt.show()

df["MA20"] = df["Close"].rolling(window=20).mean()
df["MA50"] = df["Close"].rolling(window=50).mean()

df[["Close", "MA20", "MA50"]].plot(title="SPY with Moving Averages (1Y)")
plt.show()

df["Signal"] = (df["MA20"] > df["MA50"]).astype(int)

df["Position"] = df["Signal"].shift(1)

df["StrategyReturn"] = df["Return"] * df["Position"]

df["StrategyCumulative"] = (1 + df["StrategyReturn"]).cumprod()

market_ret = df["Return"].dropna()
market_cum = df["Cumulative"].dropna()
strat_ret = df["StrategyReturn"].dropna()
strat_cum =df["StrategyCumulative"].dropna()

print("\n===== Buy & Hold (SPY) =====")
print(f"Total Market Return: {total_return(market_cum): .2%}")
print(f"Annual Market Return: {annualized_return(market_ret): .2%}")
print(f"Annual Market Volatility: {annualized_vol(market_ret): .2%}")
print(f"Market Sharpe Ratio: {sharpe_ratio(market_ret): .2f}")
print(f"Max Market Drawdown: {max_drawdown(market_ret): .2%}")

print("\n===== Strategy (MA20 > MA50) =====")
print(f"Total Strategic Return: {total_return(strat_cum): .2%}")
print(f"Annual Strategic Return: {annualized_return(strat_ret): .2%}")
print(f"Annual Strategic Volatility: {annualized_vol(strat_ret): .2%}")
print(f"Strategic Sharpe Ratio: {sharpe_ratio(strat_ret): .2f}")
print(f"Max Strategic Drawdown: {max_drawdown(strat_ret): .2%}")

df["Market Drawdown"] = df["Cumulative"]/df["Cumulative"].cummax() - 1
df["Strategy Drawdown"] = df["StrategyCumulative"]/df["StrategyCumulative"].cummax() - 1
df[["Market Drawdown", "Strategy Drawdown"]].plot(title="Market vs. Strategy Drawdown Plot")
plt.show()