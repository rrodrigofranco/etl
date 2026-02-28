import os
from dagster import resource
from sqlalchemy import create_engine

def build_db_url(prefix: str) -> str:
    host = os.getenv(f"{prefix}_HOST")
    port = os.getenv(f"{prefix}_PORT")
    name = os.getenv(f"{prefix}_NAME")
    user = os.getenv(f"{prefix}_USER")
    password = os.getenv(f"{prefix}_PASSWORD")

    if not all([host, port, name, user, password]):
        raise Exception(f"Missing environment variables for {prefix}")

    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


@resource
def source_db():
    return create_engine(build_db_url("SOURCE_DB"))


@resource
def target_db():
    return create_engine(build_db_url("TARGET_DB"))