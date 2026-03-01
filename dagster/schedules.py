from dagster import ScheduleDefinition
from jobs import daily_job

# Schedules
daily_schedule = ScheduleDefinition(
    job=daily_job,
    cron_schedule="0 1 * * *"
)