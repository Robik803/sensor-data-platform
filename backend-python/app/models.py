from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey, Index
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
    #...columns...
    __table_args__ = (Index("idx_readings_sensor_ts", "sensor_id", "timestamp"),
    )
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), index=True)  
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    acceleration_x = Column(Float)
    acceleration_y = Column(Float)
    acceleration_z = Column(Float)
    gyroscope_x = Column(Float)
    gyroscope_y = Column(Float)
    gyroscope_z = Column(Float)

    sensor = relationship("Sensor", back_populates="readings")

Sensor.readings = relationship("Reading", back_populates="sensor", cascade="all, delete-orphan")