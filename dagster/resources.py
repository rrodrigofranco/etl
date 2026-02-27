import os
from dagster import resource
from sqlalchemy import create_engine

@resource
def source_db():
    return os.getenv("SOURCE_DB_URL")

@resource
def target_db():
    return create_engine(os.getenv("TARGET_DB_URL"))