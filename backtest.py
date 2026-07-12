import strategy
import pandas as pd
  

def backtest_strategy(ticker, start_date, end_date, ema_short, ema_long, atr_period, raw_data=None):
    backtest_data = strategy.get_signals(ticker, start_date, end_date, ema_short, ema_long, atr_period, raw_data)
    Position = False
    Buy_Price = 0
    Sell_Price = 0
    trades = []
    portfolio_values = []
    portfolio_value = 1.0 

    for row in backtest_data.itertuples():
        if Position:
            current_value = portfolio_value * (row.Close/ Buy_Price)
        else:
            current_value = portfolio_value
        portfolio_values.append({"date": row.Index.date(), "value": current_value})
        if row.Buy and not Position:
            Buy_Price = row.Close
            Position = True
            buy_date = row.Index.date()
        elif (row.Sell and Position) or ((Buy_Price - 2 * row.ATR > row.Close) and Position):
            Sell_Price = row.Close
            Position = False
            days_held = (row.Index.date() - buy_date).days
            percentage_gain = (Sell_Price/Buy_Price) - 1
            trades.append({ "buy_price": Buy_Price, 
                        "buy_date": buy_date, 
                        "sell_price": Sell_Price, 
                        "sell_date": row.Index.date(),
                        "days_held": days_held,
                        "percentage_gain": percentage_gain,
                        "annualized_return": ((Sell_Price/Buy_Price) ** (365 / days_held))- 1})
            portfolio_value = portfolio_value * (Sell_Price / Buy_Price)

    trades_df = pd.DataFrame(trades)
    if trades_df.empty:
        print("No trades were executed.")
        return 0, 0, 0, []
    total_gain = trades_df["percentage_gain"].sum()
    total_trades_length = (trades_df.iloc[-1]["sell_date"] - trades_df.iloc[0]["buy_date"]).days
    compound_annual_growth_rate = ((1 + total_gain) ** (365 / total_trades_length) - 1)
    total_trades = len(trades_df)

    return  total_gain, compound_annual_growth_rate, total_trades, portfolio_values