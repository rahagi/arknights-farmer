import json
import websocket

class WSClient:

    WS_ADDR = 'wss://echo.websocket.org/'
    WS_CONN = websocket.create_connection(WS_ADDR)

    @classmethod
    def send(self, event, msg=""):
        m = {
            'event': event,
            'msg': msg
        }
        self.WS_CONN.send(json.dumps(m))
        self.WS_CONN.close()
        