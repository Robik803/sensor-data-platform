from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# Define the Sensor model
class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Define the Reading model
class Reading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    acceleration_x = Column(Float, nullable=False)
    acceleration_y = Column(Float, nullable=False)
    acceleration_z = Column(Float, nullable=False)
    gyroscope_x = Column(Float, nullable=False)
    gyroscope_y = Column(Float, nullable=False)
    gyroscope_z = Column(Float, nullable=False)

    sensor = relationship("Sensor", back_populates="readings")

Sensor.readings = relationship("Reading", back_populates="sensor", cascade="all, delete-orphan")