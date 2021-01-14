import threading
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from arknights_farmer import farmer

router = APIRouter(prefix='/farmer')

class Task(BaseModel):
    stage: str
    count: int

@router.post('/start-manual')
async def start_manual(amount: int):
    f = threading.Thread(target=farmer.init, kwargs={'manual': amount}, daemon=True)
    f.start()
    return {'manual': amount}

@router.post('/start')
async def start(task: List[Task], refill: Optional[int] = 0):
    task_list = [t.dict() for t in task]
    f = threading.Thread(target=farmer.init, kwargs={'refill': refill, 'task': task_list}, daemon=True)
    f.start()
    return task
