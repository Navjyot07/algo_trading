from strategy.state import TradeState
from broker.rest import place_order
from config.settings import LOTS


class OptionStrategy:
    def __init__(self):
        self.state = TradeState.IDLE
        self.entry = None
        self.sl = None
        self.trades = 0

        self.lots = LOTS
        self.lot_size = None
        self.symbol = None

    def set_option(self, selected_option: dict):
        self.symbol = selected_option["symbol"]
        self.lot_size = selected_option["lotSize"]

    def _get_qty(self):
        if self.lot_size is None:
            raise RuntimeError("Lot size not set. Call set_option() first.")
        return self.lots * self.lot_size

    def on_candle(self, candle, vwap, supertrend):
        """
        Called ONLY on candle close
        """
        if self.state != TradeState.IDLE:
            return

        if supertrend == "BUY" and candle["close"] > vwap:
            self.entry = candle["high"]
            self.sl = candle["low"]
            self.state = TradeState.WAITING_FOR_BREAKOUT

    def on_tick(self, price):
        if self.state == TradeState.WAITING_FOR_BREAKOUT:
            if price > self.entry:
                self.buy()
                self.state = TradeState.IN_TRADE

        elif self.state == TradeState.IN_TRADE:
            if price <= self.sl:
                self.sell()
                self.state = TradeState.IDLE

    def buy(self):
        place_order({
            "side": "BUY",
            "symbol": self.symbol,
            "qty": self._get_qty()
        })

    def sell(self):
        place_order({
            "side": "SELL",
            "symbol": self.symbol,
            "qty": self._get_qty()
        })
