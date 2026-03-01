from dagster import define_asset_job
from assets import etl_asset

# Daily jobs
daily_job = define_asset_job("daily_job")