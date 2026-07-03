import data 
import pandas as pd
import numpy as np

data = data.get_price_data(data.TICKER, data.START_DATE, data.END_DATE)

data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()
data["EMA_100"] = data["Close"].ewm(span=100, adjust=False).mean()

data["highlow"] = abs(data["High"] - data["Low"])
data["highclose"] = abs(data["High"] - data["Close"].shift(1))
data["lowclose"] = abs(data["Low"] - data["Close"].shift(1))

data["TR"] = data[["highlow", "highclose", "lowclose"]].max(axis=1)
data["ATR"] = data["TR"].rolling(window=14).mean()



data["Buy"] = (data["EMA_20"].shift(1) < data["EMA_100"].shift(1)) \
          & (data["EMA_20"] > data["EMA_100"]) \
          & (data["ATR"].shift(3) < data["ATR"].shift(2)) \
          & (data["ATR"].shift(2) < data["ATR"].shift(1)) \
          & (data["ATR"].shift(1) < data["ATR"])

data["Sell"] = (data["EMA_20"].shift(1) > data["EMA_100"].shift(1))\
          & (data["EMA_20"] < data["EMA_100"]) \
          & (data["ATR"].shift(3) < data["ATR"].shift(2)) \
          & (data["ATR"].shift(2) < data["ATR"].shift(1)) \
          & (data["ATR"].shift(1) < data["ATR"])


print(data[data["Buy"] == True])
print(data[data["Sell"] == True])
