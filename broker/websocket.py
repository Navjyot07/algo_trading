import websocket
import json

class MarketFeed:
    def __init__(self, on_tick):
        self.on_tick = on_tick

    def on_message(self, ws, message):
        data = json.loads(message)
        self.on_tick(data)

    def connect(self, url):
        ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message
        )
        ws.run_forever()
