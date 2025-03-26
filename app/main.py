from fastapi import FastAPI
from app.api.routes import telemetry
from app.api.websocket_manager import router as ws_router
from app.core.mqtt_client import mqtt_client

app = FastAPI()

# Routes
app.include_router(telemetry.router, prefix="/api")
app.include_router(ws_router, prefix="/ws")

@app.on_event("startup")
async def startup_event():
    mqtt_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    mqtt_client.disconnect()
