class CandleBuilder:
    def __init__(self):
        self.current = None
        self.candles = []

    def on_tick(self, price, ts):
        if self.current is None:
            self.current = {
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "timestamp": ts
            }
        else:
            self.current["high"] = max(self.current["high"], price)
            self.current["low"] = min(self.current["low"], price)
            self.current["close"] = price

    def close_candle(self):
        if self.current:
            self.candles.append(self.current)
            self.current = None
