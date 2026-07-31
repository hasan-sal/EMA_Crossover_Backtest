import data 
import backtest
import pandas as pd
import matplotlib.pyplot as plt

fast_ema_range = range(5, 21, 2)     
slow_ema_range = range(50, 101, 5)    
atr_range = range(10, 21, 2)          
in_sample_start_date = "2024-01-01"
in_sample_end_date = "2025-01-01"
out_of_sample_start_date = "2025-01-01"
out_of_sample_end_date = "2026-01-01"

results = []

raw_data = data.get_price_data(data.TICKER, in_sample_start_date, in_sample_end_date)

for fast_ema in fast_ema_range:
    for slow_ema in slow_ema_range:
        if fast_ema * 1.25 > slow_ema:
            continue
        for atr_period in atr_range:
            total_gain, compound_annual_growth_rate, total_trades, portfolio_values, sharpe_ratio = backtest.backtest_strategy(data.TICKER, in_sample_start_date, in_sample_end_date, fast_ema, slow_ema, atr_period, raw_data)
            if total_trades > 5 and compound_annual_growth_rate > 0:
                results.append({
                    "fast_ema": fast_ema,
                    "slow_ema": slow_ema,
                    "atr_period": atr_period,
                    "total_gain": total_gain,
                    "compound_annual_growth_rate": compound_annual_growth_rate,
                    "total_trades": total_trades,
                    "sharpe_ratio": sharpe_ratio
                })


results_df = pd.DataFrame(results)
print("Optimization Results:")
print(results_df.sort_values(by="sharpe_ratio", ascending=False).head(10))

