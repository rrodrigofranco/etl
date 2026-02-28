# ==============================
# Project: ETL Delfos
# ==============================

# Default compose command
COMPOSE=docker-compose

# ------------------------------
# Build images
# ------------------------------
build:
	$(COMPOSE) build

# ------------------------------
# Start services
# ------------------------------
up:
	$(COMPOSE) up -d --build

# ------------------------------
# Stop services
# ------------------------------
down:
	$(COMPOSE) down

# ------------------------------
# Restart services
# ------------------------------
restart:
	$(COMPOSE) restart

# ------------------------------
# Logs (all services)
# ------------------------------
logs:
	$(COMPOSE) logs -f

# ------------------------------
# Logs per service
# ------------------------------
logs-api:
	$(COMPOSE) logs -f api

logs-etl:
	$(COMPOSE) logs -f etl

logs-dagster:
	$(COMPOSE) logs -f dagster_web

# ------------------------------
# Access containers
# ------------------------------
ssh-api:
	docker exec -it api bash

ssh-etl:
	docker exec -it etl_container bash

ssh-dagster:
	docker exec -it dagster_web bash

ssh-source-db:
	docker exec -it source_db psql -U user -d source

ssh-target-db:
	docker exec -it target_db psql -U user -d target

# ------------------------------
# Run Seed (API)
# ------------------------------

seed:
	docker exec -it api python -m seeds.seed_data

# ------------------------------
# Run tests (API)
# ------------------------------
test-api:
	docker exec -it api pytest

# ------------------------------
# Run ETL manually
# ------------------------------
run-etl:
	docker exec -it etl_container python etl.py 2024-01-02

# ------------------------------
# Clean Docker system
# ------------------------------
clean:
	docker system prune -a --volumes -f