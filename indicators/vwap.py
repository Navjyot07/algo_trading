import pandas as pd

def calculate_vwap(candles):
    df = pd.DataFrame(candles)
    pv = (df["close"] * df["high"]).cumsum()
    vol = df["high"].cumsum()
    return (pv / vol).iloc[-1]
