import yfinance as yf 
import pandas as pd

TICKER = "SPY"
START_DATE= "2015-01-01"
END_DATE= "2026-01-01"

def get_price_data(tick, start_date, end_date):
    try:
        data = yf.download(tick,start=start_date,end=end_date, multi_level_index=False)
        if data.empty:
            raise ValueError(f"No data found for {tick} between {start_date} and {end_date}.")
        return data.ffill().dropna()
    except Exception as e:
        print(f"Error fetching data for {tick}: {e}")
