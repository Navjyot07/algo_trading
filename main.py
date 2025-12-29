import time
from datetime import datetime

from data.candle_builder import CandleBuilder
from indicators.vwap import calculate_vwap
from indicators.supertrend import calculate_supertrend
from broker.rest import fetch_option_chain
from broker.websocket import MarketFeed
from strategy.option_selector import select_option_by_volume
from strategy.option_strategy import OptionStrategy
from config.settings import UNDERLYING, CANDLE_INTERVAL
from broker.websocket import MarketFeed

# ------------------ INIT ------------------

candle_builder = CandleBuilder()
strategy = OptionStrategy()


def select_initial_option():
    option_chain = fetch_option_chain(UNDERLYING)

    selected_ce = select_option_by_volume(option_chain, "CE")
    selected_pe = select_option_by_volume(option_chain, "PE")

    # choose highest volume between CE & PE
    candidates = []
    if selected_ce:
        candidates.append(selected_ce)
    if selected_pe:
        candidates.append(selected_pe)

    if candidates:
        best = max(candidates, key=lambda opt: opt["volume"])
        strategy.set_option(best)
    else:
        raise RuntimeError("No option found in premium range")


# ------------------ EVENT HANDLERS ------------------

def on_tick(data):
    """
    Called on every tick from WebSocket
    """
    price = data["ltp"]
    ts = data["timestamp"]

    candle_builder.on_tick(price, ts)
    strategy.on_tick(price)


def on_candle_close():
    """
    Called every 1 minute
    """
    candle_builder.close_candle()

    candles = candle_builder.candles
    if len(candles) < 2:
        return

    vwap = calculate_vwap(candles)
    supertrend = calculate_supertrend(candles)

    strategy.on_candle(candles[-1], vwap, supertrend)


# ------------------ SCHEDULER ------------------

def candle_scheduler():
    """
    Closes candle every CANDLE_INTERVAL seconds
    """
    while True:
        time.sleep(CANDLE_INTERVAL)
        on_candle_close()


# ------------------ MAIN ------------------

def main():
    print("Starting algo...")

    select_initial_option()

    # start candle scheduler in background thread
    import threading
    threading.Thread(target=candle_scheduler, daemon=True).start()

    # connect market feed
    feed = MarketFeed(on_tick)
    feed.connect()


if __name__ == "__main__":
    main()
