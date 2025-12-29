from strategy.state import TradeState
from broker.rest import place_order
from config.settings import QTY

class OptionStrategy:
    def __init__(self):
        self.state = TradeState.IDLE
        self.entry = None
        self.sl = None
        self.trades = 0

    def on_candle(self, candle, vwap, supertrend):
        if self.state != TradeState.IDLE:
            return

        if supertrend == "BUY" and candle["close"] > vwap:
            self.entry = candle["high"]
            self.sl = candle["low"]
            self.state = TradeState.WAITING_FOR_BREAKOUT

    def on_tick(self, price):
        if not self.symbol:
            return

        if self.state == TradeState.WAITING_FOR_BREAKOUT:
            if price > self.entry:
                self.buy()
                self.state = TradeState.IN_TRADE

        elif self.state == TradeState.IN_TRADE:
            if price <= self.sl:
                self.sell()
                self.state = TradeState.IDLE

    def buy(self):
        place_order({"side": "BUY", "qty": QTY})

    def sell(self):
        place_order({"side": "SELL", "qty": QTY})
