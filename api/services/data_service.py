from sqlalchemy import text
import pandas as pd
from database import engine

ALLOWED_VARIABLES = {"wind_speed", "power", "ambient_temperature"}

def get_data(start: str, end: str, variables: list[str]):
    variables = [v for v in variables if v in ALLOWED_VARIABLES]
    cols = ", ".join(["timestamp"] + variables)

    query = text(f"""
        SELECT {cols}
        FROM data
        WHERE timestamp BETWEEN :start AND :end
    """)

    df = pd.read_sql(query, engine, params={"start": start, "end": end})
    return df.to_dict(orient="records")