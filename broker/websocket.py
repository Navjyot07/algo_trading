import websocket
import json
from config.settings import (
    DHAN_WSS_BASE_URL,
    DHAN_FEED_VERSION,
    DHAN_ACCESS_TOKEN,
    DHAN_CLIENT_ID,
    DHAN_AUTH_TYPE,
)


def build_wss_url():
    return (
        f"{DHAN_WSS_BASE_URL}"
        f"?version={DHAN_FEED_VERSION}"
        f"&token={DHAN_ACCESS_TOKEN}"
        f"&clientId={DHAN_CLIENT_ID}"
        f"&authType={DHAN_AUTH_TYPE}"
    )


class MarketFeed:
    def __init__(self, on_tick):
        self.on_tick = on_tick

    def on_message(self, ws, message):
        data = json.loads(message)

        # 🔒 guard: ignore non-tick messages
        if "ltp" not in data:
            return

        self.on_tick(data)

    def connect(self):
        ws_url = build_wss_url()

        ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
        )
        ws.run_forever()
