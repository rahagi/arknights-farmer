from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from arknights_farmer import farmer
from arknights_farmer.utils.tools import Elp
from .utils.farmer_thread import FarmerThread

router = APIRouter(prefix='/farmer')

class Task(BaseModel):
    stage: str
    count: int

@router.post('/start-onestage')
async def start_onestage(amount: int, refill: int):
    f = FarmerThread.create(target=farmer.init, kwargs={'refill': refill, 'manual': amount})
    f.start()
    return {'manual': amount}

@router.post('/start')
async def start(task: List[Task], refill: Optional[int] = 0):
    task_list = [t.dict() for t in task]
    f = FarmerThread.create(farmer.init, kwargs={'refill': refill, 'task': task_list})
    f.start()
    return task

@router.get('/get-recent-task')
async def get_recent_task():
    recent = Elp.get_recent_task()
    return [{'stage': stage.name, 'count': count} for stage, count in recent.items()] if recent else [];

