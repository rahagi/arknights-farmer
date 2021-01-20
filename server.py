from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import farmer, adb, ws
import uvicorn
import os

app = FastAPI()
app.include_router(farmer.router)
app.include_router(adb.router)
app.include_router(ws.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
