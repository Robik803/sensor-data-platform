from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas


# CRUD operations for Sensor

# Get a sensor by ID
def get_sensor(db: Session, sensor_id: int):
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()

# Get multiple sensors with pagination
def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sensor).offset(skip).limit(limit).all()

# Create a new sensor
def create_sensor(db: Session, sensor: schemas.SensorCreate):
    db_sensor = models.Sensor(name=sensor.name, location=sensor.location)
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

# Delete a sensor by ID
def delete_sensor(db: Session, sensor_id: int):
    db_sensor = get_sensor(db, sensor_id)
    if db_sensor:
        db.delete(db_sensor)
        db.commit()
    return db_sensor


# CRUD operations for Reading

# Create a new reading
def create_reading(db: Session, reading: schemas.ReadingCreate):
    db_reading = models.Reading(**reading.dict())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

# Get readings for a specific sensor with pagination
def get_readings(db: Session, sensor_id: int = None, start: str = None, end: str = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Reading)
    if sensor_id:
        query = query.filter(models.Reading.sensor_id == sensor_id)
    if start:
        query = query.filter(models.Reading.timestamp >= start)
    if end:
        query = query.filter(models.Reading.timestamp <= end)
    return query.offset(skip).limit(limit).all()

# Get a reading by ID
def get_reading(db: Session, reading_id: int):
    return db.query(models.Reading).filter(models.Reading.id == reading_id).first()

# Delete a reading by ID
def delete_reading(db: Session, reading_id: int):
    db_reading = get_reading(db, reading_id)
    if db_reading:
        db.delete(db_reading)
        db.commit()
    return db_reading

# Get sensor statistics (min, max, avg) for acceleration
def get_sensor_acceleration_stats(db: Session, sensor_id: int, start: str = None, end: str = None):
    stats = db.query(
        func.min(models.Reading.acceleration_x).label('min_accel_x'),
        func.max(models.Reading.acceleration_x).label('max_accel_x'),
        func.avg(models.Reading.acceleration_x).label('avg_accel_x'),
        func.min(models.Reading.acceleration_y).label('min_accel_y'),
        func.max(models.Reading.acceleration_y).label('max_accel_y'),
        func.avg(models.Reading.acceleration_y).label('avg_accel_y'),
        func.min(models.Reading.acceleration_z).label('min_accel_z'),
        func.max(models.Reading.acceleration_z).label('max_accel_z'),
        func.avg(models.Reading.acceleration_z).label('avg_accel_z')
    ).filter(models.Reading.sensor_id == sensor_id)
    if start:
        stats = stats.filter(models.Reading.timestamp >= start)
    if end:
        stats = stats.filter(models.Reading.timestamp <= end)
    return stats.first()