from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    robot_id = Column(String, index=True)
    battery = Column(Float)
    fuel = Column(Float)
    engine_temp = Column(Float)
    speed = Column(Float)
    runtime = Column(Float)
    task = Column(String)
    location = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
