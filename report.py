import matplotlib.pyplot as plt
import pandas as pd 
import backtest



position = False
total_gain, compound_annual_growth_rate, total_trades, portfolio_values = backtest.backtest_strategy("BTC-USD", "2026-01-01", "2026-07-12x", 7, 100, 20)  

plt.plot(pd.DataFrame(portfolio_values)["date"], pd.DataFrame(portfolio_values)["value"])
plt.title("Portfolio Value Over Time")
plt.xlabel("Date")
plt.ylabel("Portfolio Value")   
plt.figtext(0.5, 0.02, f"Total Gain: {total_gain:.2%} | CAGR: {compound_annual_growth_rate:.2%} | Trades: {total_trades}", ha="center", fontsize=10)
plt.xticks(rotation=45)
plt.subplots_adjust(bottom=0.2)
plt.show()