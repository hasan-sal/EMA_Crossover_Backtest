import strategy
import pandas as pd
import numpy as np


def backtest_strategy(ticker, start_date, end_date, ema_short, ema_long, atr_period, raw_data=None):
    backtest_data = strategy.get_signals(ticker, start_date, end_date, ema_short, ema_long, atr_period, raw_data)
    rows = list(backtest_data.itertuples())
    Position = False
    Buy_Price = 0
    Sell_Price = 0
    trades = []
    portfolio_values = []
    portfolio_value = 1.0

    # Signals are computed from the day's close, so a signal on day i can only be
    # acted on at day i+1's open - trading at day i's own close would be look-ahead.
    for i in range(len(rows) - 1):
        row = rows[i]
        next_row = rows[i + 1]
        if Position:
            current_value = portfolio_value * (row.Close / Buy_Price)
        else:
            current_value = portfolio_value
        portfolio_values.append({"date": row.Index.date(), "value": current_value})

        if row.Buy and not Position:
            Buy_Price = next_row.Open
            Position = True
            buy_date = next_row.Index.date()
        elif (row.Sell and Position) or ((Buy_Price - 2 * row.ATR > row.Close) and Position):
            Sell_Price = next_row.Open
            Position = False
            days_held = (next_row.Index.date() - buy_date).days
            percentage_gain = (Sell_Price/Buy_Price) - 1
            trades.append({ "buy_price": Buy_Price,
                        "buy_date": buy_date,
                        "sell_price": Sell_Price,
                        "sell_date": next_row.Index.date(),
                        "days_held": days_held,
                        "percentage_gain": percentage_gain,
                        "annualized_return": ((Sell_Price/Buy_Price) ** (365 / days_held))- 1})
            portfolio_value = portfolio_value * (Sell_Price / Buy_Price)

    last_row = rows[-1]
    final_value = portfolio_value * (last_row.Close / Buy_Price) if Position else portfolio_value
    portfolio_values.append({"date": last_row.Index.date(), "value": final_value})

    trades_df = pd.DataFrame(trades)
    if trades_df.empty:
        print("No trades were executed.")
        return 0, 0, 0, [], 0
    # Use the compounded portfolio value rather than summing per-trade percentage
    # gains, which understates/overstates true return once trades compound.
    total_gain = portfolio_value - 1
    total_trades_length = (trades_df.iloc[-1]["sell_date"] - trades_df.iloc[0]["buy_date"]).days
    compound_annual_growth_rate = ((1 + total_gain) ** (365 / total_trades_length) - 1)
    total_trades = len(trades_df)
    sharpe_ratio = calculate_sharpe_ratio(portfolio_values)

    return  total_gain, compound_annual_growth_rate, total_trades, portfolio_values, sharpe_ratio


def calculate_sharpe_ratio(portfolio_values, risk_free_rate=0.0, periods_per_year=365):
    if not portfolio_values:
        return 0
    values = pd.DataFrame(portfolio_values)["value"]
    daily_returns = values.pct_change().dropna()
    if len(daily_returns) < 2 or daily_returns.std() == 0:
        return 0
    daily_risk_free_rate = risk_free_rate / periods_per_year
    excess_returns = daily_returns - daily_risk_free_rate
    return (excess_returns.mean() / excess_returns.std()) * np.sqrt(periods_per_year)