# Algo Trading Strategy Backtest

EMA crossover trend-following strategy with ATR-based stop loss, backtested on BTC-USD.

## Strategy

- **Signal:** Buy when fast EMA crosses above slow EMA (and vice versa for sell)
- **Risk management:** Stop loss at entry price − 2×ATR (ATR used for risk sizing only, not signal confirmation)
- **Parameters (optimized):** Fast EMA 7, Slow EMA 100, ATR period 20

## Files

- `data.py` — pulls price data from yfinance
- `strategy.py` — calculates EMA/ATR indicators and generates buy/sell signals
- `backtest.py` — simulates trades, tracks portfolio value, computes CAGR
- `optimization.py` — grid search over EMA/ATR parameters on in-sample data
- `report.py` — plots the equity curve

## Methodology

Parameters were optimized on in-sample data (2010–2017) via grid search, then validated on out-of-sample data (2017–2026) that was never touched during optimization.

## Results (out-of-sample, 2017–2026)

- **CAGR:** 38.64%
- **Total Gain:** 1619.49%
- **Trades:** 27

## Limitations

- Tested on a single asset (BTC-USD) — no diversification
- No transaction costs or slippage modeled
- SPY version of this strategy only generated 3 trades over 15 years — too few for statistical significance, which is why BTC-USD was used instead
- Backtest loop uses `itertuples()`, fine for daily data but wouldn't scale to intraday
- One in-sample/out-of-sample split rather than full rolling walk-forward validation

## Next steps

- Rolling walk-forward validation across multiple windows
- Add transaction costs and slippage
- Test across a multi-asset universe
- Add Sharpe ratio and max drawdown to reported metrics
```
