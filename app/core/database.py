from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Create the async engine
engine = create_async_engine(settings.POSTGRES_URL, echo=True, future=True)

# Session factory (correct way to manage per-task sessions)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Declarative base for your models
Base = declarative_base()
