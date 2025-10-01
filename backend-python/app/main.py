from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db, Base


# Create the database tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI app
app = FastAPI(title= "Sensor Data API", description="API for managing sensor data", version="1.0.0")

from sqlalchemy import text
@app.get("/healthz")
def healthz(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


# Sensor Endpoints

# Create a new sensor
@app.post("/sensors/", response_model=schemas.Sensor)
def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    return crud.create_sensor(db=db, sensor=sensor)

# Get a sensor by ID
@app.get("/sensors/{sensor_id}", response_model=schemas.Sensor)
def read_sensor(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = crud.get_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor

# Get multiple sensors with pagination
@app.get("/sensors/", response_model=list[schemas.Sensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensors = crud.get_sensors(db, skip=skip, limit=limit)
    return sensors

# Delete a sensor by ID
@app.delete("/sensors/{sensor_id}", response_model=schemas.Sensor)
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = crud.delete_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor


# Reading Endpoints

# Create a new reading
@app.post("/readings/", response_model=schemas.Reading)
def create_reading(reading: schemas.ReadingCreate, db: Session = Depends(get_db)):
    return crud.create_reading(db=db, reading=reading)

# Get readings with optional filters and pagination
@app.get("/readings/", response_model=list[schemas.Reading])
def read_readings(
    sensor_id: int = Query(None, description="Filter by sensor ID"),
    start: str = Query(None, description="Start timestamp (ISO format)"),
    end: str = Query(None, description="End timestamp (ISO format)"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    readings = crud.get_readings(db, sensor_id=sensor_id, start=start, end=end, skip=skip, limit=limit)
    return readings

# Get a reading by ID
@app.get("/readings/{reading_id}", response_model=schemas.Reading)
def read_reading(reading_id: int, db: Session = Depends(get_db)):
    db_reading = crud.get_reading(db, reading_id=reading_id)
    if db_reading is None:
        raise HTTPException(status_code=404, detail="Reading not found")
    return db_reading

# Delete a reading by ID
@app.delete("/readings/{reading_id}", response_model=schemas.Reading)
def delete_reading(reading_id: int, db: Session = Depends(get_db)):
    db_reading = crud.delete_reading(db, reading_id=reading_id)
    if db_reading is None:
        raise HTTPException(status_code=404, detail="Reading not found")
    return db_reading

# Statistics Endpoint
@app.get("/stats/sensors/{sensor_id}")
def sensor_stats(sensor_id: int, start: str = Query(None), end: str = Query(None), db: Session = Depends(get_db)):
    stats = crud.get_sensor_stats(db, sensor_id=sensor_id, start=start, end=end)
    if stats is None:
        raise HTTPException(status_code=404, detail="Sensor not found or no readings available")
    return stats._asdict()  #Convert Sqlalchemy Row object to dictionary