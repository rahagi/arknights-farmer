from typing import List, Any, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .utils.game_state import GameState
from .utils.ws_events import WSEvents
from .utils.farmer_thread import FarmerThread

router = APIRouter()

class ConnPool:
    def __init__(self):
        self.active_conn: List[WebSocket] = []

    def __create_msg(self, evt: str, msg: str):
        return {
            'event': evt,
            'msg': msg,
        }
    
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_conn.append(ws)
    
    def remove(self, ws: WebSocket):
        self.active_conn.remove(ws)
    
    async def send(self, ws: WebSocket, evt: str, msg: Any):
        await ws.send_json(self.__create_msg(evt, msg))
    
    async def broadcast(self, ws: WebSocket, msg: Any, evt: Optional[str] = ''):
        for conn in self.active_conn:
            if conn is not ws:
                await conn.send_json(self.__create_msg(evt or 'broadcast', msg))

pool = ConnPool()
curr_state = GameState()

@router.websocket('/ws')
async def ws_endpoint(ws: WebSocket):
    await pool.connect(ws)
    try:
        while True:
            data = await ws.receive_json()
            event, msg = [data[k] for k in data]
            global curr_state
            if event == WSEvents.ON_LOG:
                curr_state.log.append(msg)
            elif event == WSEvents.ON_PROGRESS:
                curr_state.on_progress = msg
            elif event == WSEvents.ON_START:
                curr_state.started = True
            elif event == WSEvents.ON_FINISH:
                curr_state.completed.append(msg)
            elif event in [WSEvents.ON_EXIT, WSEvents.ON_STOP]:
                curr_state = GameState()
                FarmerThread.raise_exception(KeyboardInterrupt)
            elif event == WSEvents.REQ_CURR_STATE:
                await pool.send(ws, WSEvents.REQ_CURR_STATE, curr_state.dict())
            elif event == WSEvents.PING:
                await pool.send(ws, 'PONG', 'PONG')
            if event not in [WSEvents.REQ_CURR_STATE, WSEvents.ON_STOP, WSEvents.PING]:
                await pool.broadcast(ws, msg, event)
    except WebSocketDisconnect:
        pool.remove(ws)

