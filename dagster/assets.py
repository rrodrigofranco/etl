from dagster import asset, DailyPartitionsDefinition
from datetime import datetime
import subprocess

daily_partitions = DailyPartitionsDefinition(
    start_date="2026-02-20"
)

@asset(partitions_def=daily_partitions)
def etl_asset(context):
    partition_date = context.partition_key
    subprocess.run(
        ["python", "/app/etl/etl.py", partition_date],
        check=True
    )