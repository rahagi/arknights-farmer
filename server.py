from fastapi import FastAPI
from api import farmer, adb, ws
import uvicorn
import os

app = FastAPI()
app.include_router(farmer.router)
app.include_router(adb.router)
app.include_router(ws.router)

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    uvicorn.run(app, host='0.0.0.0', port=port)
