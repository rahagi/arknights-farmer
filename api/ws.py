from typing import List, Any, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .utils.game_state import GameState
from .utils.ws_events import WSEvents

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
    
    async def send(self, ws: WebSocket, msg: Any):
        await ws.send_json(self.__create_msg('priv', msg))
    
    async def broadcast(self, msg: Any, evt: Optional[str] = ''):
        for conn in self.active_conn:
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
            elif event == WSEvents.ON_FINISH:
                curr_state.completed.append(msg)
            elif event == WSEvents.ON_EXIT:
                curr_state = GameState()
            elif event == WSEvents.REQ_CURR_STATE:
                await pool.send(ws, curr_state.dict())
            if event != WSEvents.REQ_CURR_STATE:
                await pool.broadcast(msg, event)
    except WebSocketDisconnect:
        pool.remove(ws)
