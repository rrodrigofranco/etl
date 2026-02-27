from dagster import Definitions
from assets import etl_asset

defs = Definitions(
    assets=[etl_asset],
)