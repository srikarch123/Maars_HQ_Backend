import json
import paho.mqtt.client as mqtt
import asyncio
from app.core.config import settings
from app.core.database import async_session
from app.models.telemetry import Telemetry
from app.core.redis_client import get_redis
from app.api.websocket_manager import manager

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT)
        self.client.loop_start()
        self.client.subscribe("robot/+/telemetry")

    def disconnect(self):
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        print("✅ MQTT connected with result code", rc)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"📩 MQTT Message received: {payload}")
        asyncio.run(self.handle_telemetry(payload))

    async def handle_telemetry(self, payload: str):
        try:
            data = json.loads(payload)
            robot_id = data.get("robot_id")
            telemetry = Telemetry(
                robot_id=robot_id,
                battery=data.get("battery"),
                fuel=data.get("fuel"),
                engine_temp=data.get("engine_temp"),
                speed=data.get("speed"),
                runtime=data.get("runtime"),
                task=data.get("task"),
                location=data.get("location"),
            )

            # Save to PostgreSQL
            async with async_session() as session:
                session.add(telemetry)
                await session.commit()

            # Cache in Redis
            redis = await get_redis()
            await redis.set(f"telemetry:{robot_id}", json.dumps(data))

            # Send to WebSocket clients
            await manager.broadcast(json.dumps(data))

        except Exception as e:
            print("❌ Error processing telemetry:", str(e))

mqtt_client = MQTTClient()
