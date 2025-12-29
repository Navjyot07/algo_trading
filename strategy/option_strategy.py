from strategy.state import TradeState
from broker.rest import place_order
from config.settings import LOTS


class OptionStrategy:
    def __init__(self):
        self.state = TradeState.IDLE
        self.entry = None
        self.sl = None
        self.trades = 0

        self.lots = LOTS          # e.g. 1, 2, 3
        self.lot_size = None     # comes from selected_option
        self.symbol = None       # option symbol

    def set_option(self, selected_option: dict):
        """
        Must be called before trading starts
        """
        self.symbol = selected_option["symbol"]
        self.lot_size = selected_option["lotSize"]

    def _get_qty(self):
        """
        qty = lots x lot_size
        """
        if self.lot_size is None:
            raise RuntimeError("Lot size not set. Did you call set_option()?")

        return self.lots * self.lot_size

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
