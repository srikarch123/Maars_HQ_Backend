import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql+asyncpg://user:pass@localhost/agrobot")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

settings = Settings()
