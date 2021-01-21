from fastapi import APIRouter
from arknights_farmer.utils.tools import Adb

router = APIRouter(prefix='/adb')

@router.post('/connect')
def connect(host: str, port: str):
    res = Adb.connect(host, port)
    res = res.decode('utf-8')
    return {'connect': False if 'failed' in res else True}

@router.get('/devices')
def devices():
    devices = Adb.list_devices()
    if len(devices) == 1:
        devices = [
            {
                'serial': devices[0],
                'name': Adb.exec_out('getprop ro.product.model').decode('utf-8').strip(),
                'screen': Adb.exec_out('wm size').decode('utf-8').strip().split(': ')[1],
            }
        ]
    return {
        'devices': devices
    }

