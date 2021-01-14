from fastapi import APIRouter
from arknights_farmer.utils.tools import Adb

router = APIRouter(prefix='/adb')

@router.get('/devices')
def devices():
    devices = Adb.list_devices()
    return {
        'devices': devices
    }