import asyncio
from app.core.database import engine, Base
from app.models.telemetry import Telemetry  # ✅ THIS is needed so SQLAlchemy registers the model

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created")

if __name__ == "__main__":
    asyncio.run(init_db())
