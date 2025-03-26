import redis.asyncio as redis_async
from app.core.config import settings

redis = None

async def get_redis():
    global redis
    if redis is None:
        redis = redis_async.from_url(settings.REDIS_URL, decode_responses=True)
    return redis
