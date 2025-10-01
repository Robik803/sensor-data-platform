# Sensor Data Platform

A compact backend to manage **inertial sensor** data (accelerometer/gyroscope).  
Built with **Python (FastAPI + SQLAlchemy + PostgreSQL)** and prepared to add a **Rust sensor simulator** later.

> Goal: demonstrate backend skills, API design, and database handling in a small, extensible project.

---

## ✨ Features

- CRUD for **sensors**
- CRUD for **readings** with **filters** (`sensor_id`, `start`, `end`)
- **Swagger UI** at `/docs` and OpenAPI at `/openapi.json`
- **Health check** at `/healthz`
- **Docker Compose** for one-command startup (PostgreSQL + backend)
- Clean structure, ready to grow (Rust simulator, stats, charts, tests)

> Tables are created automatically on startup via SQLAlchemy. Alembic/migrations can be added later.

---

## 🧱 Tech Stack

- **Backend:** FastAPI, Uvicorn  
- **ORM/Models:** SQLAlchemy, Pydantic  
- **Database:** PostgreSQL  
- **Infra:** Docker & Docker Compose  

---

## 🗺️ Architecture

[Future Rust Simulator] --HTTP--> [FastAPI Backend] --SQLAlchemy--> [PostgreSQL] — Swagger UI: /docs

- FastAPI Backend exposes CRUD endpoints for sensors and readings.
- PostgreSQL stores sensors and time-series readings.
- Swagger UI at `/docs` provides interactive API documentation.
- Rust Simulator (future) will generate fake IMU data and POST it to the backend.

---

## 📂 Project Structure

```text
sensor-data-platform/
├── backend-python/
│ ├── app/
│ │ ├── main.py # FastAPI app + routes
│ │ ├── models.py # SQLAlchemy models (Sensor, Reading)
│ │ ├── schemas.py # Pydantic schemas
│ │ ├── crud.py # Data-access logic
│ │ └── database.py # DB connection + Base.metadata.create_all()
│ ├── requirements.txt
│ ├── Dockerfile
│ └── .dockerignore
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## ⚙️ Configuration

By default, the backend reads a PostgreSQL connection from environment variables:

```ini
# .env.example
DB_HOST=db
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=sensors
DB_PORT=5432
```
The connection URL is built in backend-python/app/database.py from these variables.

---

## 🚀 Quickstart (Docker)
Requirements: Docker & Docker Compose.

```bash
git clone https://github.com/Robik803/sensor-data-platform.git
cd sensor-data-platform
cp .env.example .env
docker compose up --build
```
API: http://localhost:8000

Swagger UI: http://localhost:8000/docs

Health: http://localhost:8000/healthz

If the database takes a moment to boot, try the URLs again after a few seconds.

---

## 🧪 Try the API (curl)

### Health

```bash
curl "http://localhost:8000/healthz"
```

### Sensors

#### Create
```bash
curl -X POST "http://localhost:8000/sensors/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Sensor A","location":"Lab 1"}'
``` 

#### List

```bash
curl "http://localhost:8000/sensors/"
```

#### Get by ID

```bash
curl "http://localhost:8000/sensors/1"
```

#### Delete

```bash
curl -X DELETE "http://localhost:8000/sensors/1"
```

### Readings

#### Create

```bash
curl -X POST "http://localhost:8000/readings/" \
  -H "Content-Type: application/json" \
  -d '{"sensor_id":1,"accel_x":0.1,"accel_y":0.2,"accel_z":9.8,"gyro_x":0.01,"gyro_y":0.02,"gyro_z":0.03}'
```

#### List with filters

```bash
# by sensor
curl "http://localhost:8000/readings/?sensor_id=1"

# by date range (ISO 8601)
curl "http://localhost:8000/readings/?sensor_id=1&start=2025-09-30T00:00:00Z&end=2025-10-01T23:59:59Z"
```

---

## 📌 Minimal Data Model

**sensors**
- id (PK, int)
- name (string)
- location (string)
- created_at (timestamp, default now)

**readings**
- id (PK)
- sensor_id (FK → sensors.id)
- timestamp (timestamp, default now)
- accel_x, accel_y, accel_z (float)
- gyro_x, gyro_y, gyro_z (float)

**Suggested index for performance:**
```sql
CREATE INDEX idx_readings_sensor_ts ON readings(sensor_id, timestamp);
```
(Declared as a composite index in `models.py`.)

---

## 🗺️ Roadmap
- Rust simulator: generate fake readings and POST them to the backend
- Statistics: averages, min/max over a date range
- Visualization: small dashboard (React/Chart.js) or a notebook
- Tests: unit/integration (pytest)
- Migrations: Alembic for schema evolution
- Auth & pagination: tokens, page-based listing

---

## 📜 License
MIT — see `LICENSE`.