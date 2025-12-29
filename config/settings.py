import os
from dotenv import load_dotenv

load_dotenv()

DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")

UNDERLYING = os.getenv("UNDERLYING")
PREMIUM_MIN = int(os.getenv("PREMIUM_MIN"))
PREMIUM_MAX = int(os.getenv("PREMIUM_MAX"))

QTY = int(os.getenv("QTY"))
LOTS = int(os.getenv("LOTS"))

MAX_TRADES_PER_DAY = int(os.getenv("MAX_TRADES_PER_DAY"))

CANDLE_INTERVAL = 60  # seconds
