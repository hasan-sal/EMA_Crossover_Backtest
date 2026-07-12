import data 
import pandas as pd
import numpy as np


def get_signals(ticker, start_date, end_date, ema_short, ema_long, atr_period, raw_data=None):
    if raw_data is None:
        datas = data.get_price_data(ticker, start_date, end_date)
    else:
        datas = raw_data.copy()

    datas["EMA_SHORT"] = datas["Close"].ewm(span=ema_short, adjust=False).mean()
    datas["EMA_LONG"] = datas["Close"].ewm(span=ema_long, adjust=False).mean()

    datas["highlow"] = abs(datas["High"] - datas["Low"])
    datas["highclose"] = abs(datas["High"] - datas["Close"].shift(1))
    datas["lowclose"] = abs(datas["Low"] - datas["Close"].shift(1))                 
    datas["TR"] = datas[["highlow", "highclose", "lowclose"]].max(axis=1)
    datas["ATR"] = datas["TR"].rolling(window=atr_period).mean()

    datas["Buy"] = (datas["EMA_SHORT"].shift(1) < datas["EMA_LONG"].shift(1)) \
            & (datas["EMA_SHORT"] > datas["EMA_LONG"]) \

    datas["Sell"] = (datas["EMA_SHORT"].shift(1) > datas["EMA_LONG"].shift(1))\
            & (datas["EMA_SHORT"] < datas["EMA_LONG"])
    return datas
