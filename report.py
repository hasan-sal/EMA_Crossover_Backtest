import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import data
import backtest

TICKER, START_DATE, END_DATE = "SPY", "2015-01-01", "2026-01-01"

total_gain, compound_annual_growth_rate, total_trades, portfolio_values, sharpe_ratio = backtest.backtest_strategy(TICKER, START_DATE, END_DATE, 17, 85, 12)

price_data = data.get_price_data(TICKER, START_DATE, END_DATE)
buy_hold_value = price_data["Close"] / price_data["Close"].iloc[0]
buy_hold_gain = buy_hold_value.iloc[-1] - 1
buy_hold_days = (price_data.index[-1] - price_data.index[0]).days
buy_hold_cagr = (1 + buy_hold_gain) ** (365 / buy_hold_days) - 1
buy_hold_returns = buy_hold_value.pct_change().dropna()
buy_hold_sharpe = (buy_hold_returns.mean() / buy_hold_returns.std()) * np.sqrt(365)

print(f"Strategy   -> Total Gain: {total_gain:.2%} | CAGR: {compound_annual_growth_rate:.2%} | Trades: {total_trades} | Sharpe: {sharpe_ratio:.2f}")
print(f"Buy & Hold -> Total Gain: {buy_hold_gain:.2%} | CAGR: {buy_hold_cagr:.2%} | Sharpe: {buy_hold_sharpe:.2f}")

portfolio_df = pd.DataFrame(portfolio_values)
plt.plot(portfolio_df["date"], portfolio_df["value"], label="Strategy")
plt.plot(price_data.index, buy_hold_value, label="Buy & Hold")
plt.title("Portfolio Value Over Time")
plt.xlabel("Date")
plt.ylabel("Portfolio Value")
plt.legend()
plt.figtext(0.5, 0.02,
            f"Strategy: {total_gain:.2%} gain, {compound_annual_growth_rate:.2%} CAGR, {total_trades} trades, {sharpe_ratio:.2f} Sharpe | "
            f"Buy & Hold: {buy_hold_gain:.2%} gain, {buy_hold_cagr:.2%} CAGR, {buy_hold_sharpe:.2f} Sharpe",
            ha="center", fontsize=9)
plt.xticks(rotation=45)
plt.subplots_adjust(bottom=0.2)
plt.show()
