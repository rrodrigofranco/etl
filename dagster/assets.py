from dagster import asset, DailyPartitionsDefinition
from etl.etl import run_etl

daily = DailyPartitionsDefinition(start_date="2024-01-01")

@asset(partitions_def=daily)
def etl_asset(context):
    date = context.partition_key
    run_etl(date)