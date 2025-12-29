from enum import Enum, auto

class TradeState(Enum):
    IDLE = auto()
    WAITING_FOR_BREAKOUT = auto()
    IN_TRADE = auto()
