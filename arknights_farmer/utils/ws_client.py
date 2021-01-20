import json
import websocket
import time
import threading

class WSClient:

    WS_ADDR = 'ws://localhost:5000/ws'
    WS_CONN = None

    @classmethod
    def keep_alive(self):
        old_ws = self.WS_CONN
        while self.WS_CONN is old_ws:
            try:
                self.send('ping', 'ping')
                pong = self.recv()
                print('pong:', pong)
                time.sleep(5)
            except Exception:
                continue

    @classmethod
    def send(self, event, msg=''):
        m = {
            'event': event,
            'msg': msg
        }
        if event == 'on-exit':
            print('onEXITsend')
        self.WS_CONN.send(json.dumps(m))

    @classmethod
    def recv(self):
        ret = self.WS_CONN.recv()
        return json.loads(ret)
    
    @classmethod
    def close(self):
        print('onEXITclose')
        self.WS_CONN.close()

    @classmethod
    def init(self):
        if self.WS_CONN:
            self.close()
            time.sleep(0.1)
        self.WS_CONN = websocket.create_connection(self.WS_ADDR)
        t = threading.Thread(target=self.keep_alive, daemon=True, name="KeepAliveThread")
        t.start()

