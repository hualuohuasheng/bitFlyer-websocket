import websocket
import json

class BitflyerWebSocket:

    def __init__(self, channel, product_code):

        self.endpoint = 'wss://ws.lightstream.bitflyer.com/json-rpc'
        self.channel = channel
        self.product_code = product_code

        self._connect()

    def _connect(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(self.endpoint,
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close
                                )
        ws.on_open = self.on_open
        ws.run_forever()

    def on_message(self, ws, message):
        data = json.loads(message)
        channel = data['params']['channel']
        message_ = data['params']['message']
        print(channel, message_)
        print()

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print('close')

    def on_open(self, ws):
        for c, p in zip(self.channel, self.product_code):
            data = {
                'method': 'subscribe',
                'params': {
                    'channel': '_'.join(('lightning', c, p))
                    }
                }
            ws.send(json.dumps(data))
        print('open')

if __name__ == '__main__':
    BitflyerWebSocket(channel=['board_snapshot', 'board', 'ticker'], product_code=['FX_BTC_JPY' for i in range(3)])