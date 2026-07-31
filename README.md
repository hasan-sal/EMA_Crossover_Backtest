EMA crossover trend-following strategy with ATR-based stop loss, backtested on SPY.

## Strategy

- **Signal:** Buy when fast EMA crosses above slow EMA (and vice versa for sell)
- **Risk management:** Stop loss at entry price − 2×ATR (ATR used for risk sizing only, not signal confirmation)
- **Execution:** Trades fill at the next bar's open after a signal fires on the current bar's close, to avoid look-ahead bias
- **Parameters:** Fast EMA 17, Slow EMA 85, ATR period 12 (selected via grid search on in-sample data)

## Files

- `data.py` — pulls price data from yfinance
- `strategy.py` — calculates EMA/ATR indicators and generates buy/sell signals
- `backtest.py` — simulates trades, tracks portfolio value, computes CAGR and Sharpe
- `optimization.py` — grid search over EMA/ATR parameters on in-sample data
- `report.py` — plots the equity curve against buy-and-hold

## Methodology

Parameters were grid-searched on in-sample data (2015–2023), then checked against out-of-sample data (2023–2026). The out-of-sample window only produced a single trade — too few to draw any conclusion from — so the results below are the full-period (2015–2026) backtest instead, reported next to plain buy-and-hold over the same window as the actual benchmark.

## Results (SPY, 2015–2026)

| | Total Gain | CAGR | Sharpe | Trades |
|---|---|---|---|---|
| Strategy | 175.73% | 10.59% | 1.20 | 14 |
| Buy & Hold | 299.74% | 13.42% | 0.96 | — |

## Finding

The strategy does not beat buy-and-hold on raw return — it gives up nearly half the total gain over the period. Its Sharpe ratio is somewhat better, meaning it achieves that lower return with less volatility (it sits in cash between the 14 trades rather than riding the full drawdown history of the index), but that's a real return/risk trade-off, not a free win. On an 11-year daily EMA crossover, that's the honest result: a trend filter that avoids some drawdown but also gives up a large share of the market's long-run compounding.

The bigger issue is statistical: 14 trades over 11 years is not enough to be confident this Sharpe edge is real rather than noise, and the proper out-of-sample check (above) couldn't even test that, since it only contained one trade.

## Limitations

- Single asset (SPY) — no cross-market evidence that the parameters generalize
- No transaction costs or slippage modeled
- One static in-sample/out-of-sample split rather than rolling walk-forward validation, and that split produced only 1 out-of-sample trade — not a meaningful test
- Backtest loop uses `itertuples()`, fine for daily data but wouldn't scale to intraday
- All-or-nothing position sizing — no volatility targeting or diversification across concurrent positions

## Next steps (not pursued here)

- Rolling walk-forward validation across multiple windows, to get more than one out-of-sample data point
- Multi-asset testing, to see whether the chosen parameters are a real signal or an artifact of this one ticker/window
- Transaction costs and slippage
- Max drawdown as a reported metric
- Parameter robustness check (heatmap across the grid search) to check the chosen params aren't an isolated lucky cell
