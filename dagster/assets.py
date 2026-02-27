from dagster import asset
import subprocess

@asset
def etl_asset():
    subprocess.run(
        ["python", "/app/etl/etl.py", "2026-02-27"],
        check=True
    )