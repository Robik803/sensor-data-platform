from pydantic import BaseModel
from datetime import datetime


# Base schema for Sensor

class SensorBase(BaseModel):
    name: str
    location: str

class SensorCreate(SensorBase):
    pass

class Sensor(SensorBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Base schema for Reading

class ReadingBase(BaseModel):
    sensor_id: int
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float
    gyroscope_x: float
    gyroscope_y: float
    gyroscope_z: float

class ReadingCreate(ReadingBase):
    pass

class Reading(ReadingBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True