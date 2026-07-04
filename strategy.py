import data 
import pandas as pd
import numpy as np

def get_signals(ticker, start_date, end_date):

    datas = data.get_price_data(ticker, start_date, end_date)

    datas["EMA_20"] = datas["Close"].ewm(span=20, adjust=False).mean()
    datas["EMA_100"] = datas["Close"].ewm(span=100, adjust=False).mean()

    datas["highlow"] = abs(datas["High"] - datas["Low"])
    datas["highclose"] = abs(datas["High"] - datas["Close"].shift(1))
    datas["lowclose"] = abs(datas["Low"] - datas["Close"].shift(1))                 
    datas["TR"] = datas[["highlow", "highclose", "lowclose"]].max(axis=1)
    datas["ATR"] = datas["TR"].rolling(window=14).mean()

    datas["Buy"] = (datas["EMA_20"].shift(1) < datas["EMA_100"].shift(1)) \
            & (datas["EMA_20"] > datas["EMA_100"]) \
            & (datas["ATR"].shift(3) < datas["ATR"].shift(2)) \
            & (datas["ATR"].shift(2) < datas["ATR"].shift(1)) \
            & (datas["ATR"].shift(1) < datas["ATR"])

    datas["Sell"] = (datas["EMA_20"].shift(1) > datas["EMA_100"].shift(1))\
            & (datas["EMA_20"] < datas["EMA_100"]) \
            & (datas["ATR"].shift(3) < datas["ATR"].shift(2)) \
            & (datas["ATR"].shift(2) < datas["ATR"].shift(1)) \
            & (datas["ATR"].shift(1) < datas["ATR"])
    return datas
