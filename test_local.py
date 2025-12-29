from data.candle_builder import CandleBuilder
from indicators.vwap import calculate_vwap
from indicators.supertrend import calculate_supertrend

builder = CandleBuilder()

ticks = [
    {"ltp": 55, "timestamp": 1700000000},
    {"ltp": 57, "timestamp": 1700000060},
    {"ltp": 62, "timestamp": 1700000120},
]

for t in ticks:
    builder.on_tick(t["ltp"], t["timestamp"])

builder.close_candle()

candles = builder.candles

print("Candles:", candles)
print("VWAP:", calculate_vwap(candles))
print("Supertrend:", calculate_supertrend(candles))


from strategy.option_selector import select_option_by_volume

dummy_chain = [
    {"type": "CE", "ltp": 52, "volume": 1000, "symbol": "CE1", "lotSize": 50},
    {"type": "CE", "ltp": 60, "volume": 2000, "symbol": "CE2", "lotSize": 50},
    {"type": "PE", "ltp": 55, "volume": 3000, "symbol": "PE1", "lotSize": 40},
]

print(select_option_by_volume(dummy_chain, "CE"))
print(select_option_by_volume(dummy_chain, "PE"))



from strategy.option_strategy import OptionStrategy

sel = {"type":"CE","ltp":60,"volume":2000,"symbol":"CE2","lotSize":50}
strategy = OptionStrategy()
strategy.set_option(sel)

# Simulate a candle close and tick
strategy.on_candle({"high":61,"close":61,"low":59}, 60.5, "BUY")
strategy.on_tick(62)

print("State after buy:", strategy.state)
