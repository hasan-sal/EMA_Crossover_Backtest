import strategy
import data
import pandas as pd


backtest_data = strategy.get_signals(data.TICKER, data.START_DATE, data.END_DATE)
Position = False
Buy_Price = 0
Sell_Price = 0
trades = []

for row in backtest_data.itertuples():
    if row.Buy and not Position:
        Buy_Price = row.Close
        Position = True
        print(f"Buy at {Buy_Price} on {row.Index.date()}")
        buy_date = row.Index.date()
    elif row.Sell and Position:
        Sell_Price = row.Close
        Position = False
        print(f"Sell at {Sell_Price} on {row.Index.date()}")
        print(f"Percentage Gain: {(Sell_Price/Buy_Price) - 1:.2%}\n")
        trades.append({ "buy_price": Buy_Price, "buy_date": buy_date, "sell_price": Sell_Price, "sell_date": row.Index.date(), "percentage_gain": (Sell_Price/Buy_Price) - 1 })

trades_df = pd.DataFrame(trades)
print(trades_df)