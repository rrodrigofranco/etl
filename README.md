# ETL – Data Pipeline with Dagster

This project implements a fully containerized data pipeline using:

- FastAPI (data source API)
- Pandas (data transformation)
- PostgreSQL (target database)
- Dagster (orchestration)
- Docker & Docker Compose

The pipeline extracts time-series data, aggregates it into 10-minute intervals, and stores the results in a target database. The orchestration layer supports daily partitions and scheduled execution.

---

## Architecture

The system is composed of the following services:

- **source_db** → PostgreSQL source database  
- **target_db** → PostgreSQL target database  
- **api** → FastAPI service simulating the data source  
- **etl** → Python ETL logic  
- **dagster** → Orchestrator responsible for scheduling and execution  

All services are containerized and managed with Docker Compose.

---

## How It Works

1. Dagster triggers a partitioned asset (`etl_asset`)
2. The asset executes the ETL script
3. The ETL:
   - Fetches data from the API
   - Aggregates into 10-minute intervals
   - Ensures idempotency by deleting existing data for the partition date
   - Inserts transformed records into the target database
4. Dagster tracks execution history and partition status

---

## Project Structure

```
project/
│
├── api/
│   ├── database.py
│   ├── main.py
│   ├── models/data.py
│   ├── core/security.py
│   ├── routes/data_router.py
│   ├── services/service.py
│   ├── seeds/seed_data.py
│   ├── tests/test_api.py
├── etl/
│   ├── etl.py
│   ├── target_models.py
├── dagster/            
│   ├── assets.py
│   ├── jobs.py
│   ├── schedules.py
│   ├── repository.py
│   └── workspace.yaml
│
├── docker-compose.yml
└── README.md
```

---

## Running the Project

### 1️Build and start services

```bash
docker-compose up --build | make up
```

---

### Access services

- API → http://localhost:8000/docs  
- Dagster UI → http://localhost:3000  

---

## Running the Pipeline

### Manual Execution (UI)

1. Open Dagster UI  
2. Click **Assets**  
3. Select `etl_asset`  
4. Choose a partition date  
5. Click **Materialize**

---

### Manual Execution (CLI)

```bash
docker exec -it dagster_web bash | make ssh-dagster 
dagster job execute -j etl_job --partition 2026-02-26
```

---

## Makefile Commands

Use the following commands to manage the project:

```bash
make up              # Build and start all services in detached mode
make logs            # Follow logs from all containers
make logs-api        # Follow logs from Api container
make logs-etl        # Follow logs from ETL container
make logs-dagster    # Follow logs from Dagster container
make ssh-api         # Access the Api container shell
make ssh-etl         # Access the ETL container shell
make ssh-dagster     # Access the Dagster container shell
make ssh-source-db   # Access the Source DB container shell
make ssh-target-db   # Access the Target DB container shell
make test-api        # Run automated tests inside the API container
make run-etl         # Execute the ETL manually for a specifc date
make seed            # Run the seed
make down            # Stop and remove all containers
make clean           # Clear all containers
```
---

## Partitions

The pipeline uses **daily partitions** starting from:

```
2026-02-20
```

Each partition represents one day of data and can be independently reprocessed.

---

## Idempotency

The ETL ensures idempotency with:

```sql
DELETE FROM data WHERE timestamp BETWEEN :start AND :end;
```

This guarantees that reprocessing a day does not duplicate records.

---

## Scheduling

A cron-based schedule is defined in `schedules.py`.

Example:

```python
cron_schedule="0 1 * * *"
```

Runs every day at 01:00.

For testing:

```python
cron_schedule="* * * * *"
```

Runs every minute.

---

## Design Decisions

- Containers are isolated for clean separation of concerns
- The orchestrator does not contain business logic
- ETL logic is reusable and independent
- Daily partitioning enables safe reprocessing
- Multiprocess executor is enabled by default
- The architecture supports extension for ML workflows

---

## Technologies Used

- Python 3.11
- FastAPI
- Pandas
- SQLAlchemy
- PostgreSQL
- Dagster
- Docker

---

## Author

Rodrigo Ribeiro Franco  