from typing import List, Optional
from pydantic import BaseModel

class GameState(BaseModel):
    on_progress: Optional[str] = ''
    log: Optional[List[str]] = []
    completed: Optional[List[str]] = []
    started: Optional[bool] = False
