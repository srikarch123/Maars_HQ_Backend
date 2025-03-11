from fastapi import FastAPI
from .api.routes import router as api_router
from .api.websocket import ws_router
from .core.mqtt_client import start_mqtt

def create_app() -> FastAPI:
    app = FastAPI(title="MAARS HQ Backend")

    # Start MQTT client
    mqtt_client = start_mqtt()

    # Include routes
    app.include_router(api_router, prefix="/api")
    app.include_router(ws_router, prefix="/ws", tags=["websocket"])

    return app

app = create_app()
