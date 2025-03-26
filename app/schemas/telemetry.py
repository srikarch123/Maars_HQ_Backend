from pydantic import BaseModel
from datetime import datetime

class TelemetryCreate(BaseModel):
    robot_id: str
    battery: float
    fuel: float
    engine_temp: float
    speed: float
    runtime: float
    task: str
    location: str

class TelemetryOut(TelemetryCreate):
    timestamp: datetime

    class Config:
        orm_mode = True
