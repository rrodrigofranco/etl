from fastapi import FastAPI, Query
from sqlalchemy import text
from database import engine
import pandas as pd

app = FastAPI()

@app.get("/data")
def get_data(
    start: str,
    end: str,
    variables: list[str] = Query(...)
):
    allowed = {"wind_speed", "power", "ambient_temperature"}
    variables = [v for v in variables if v in allowed]

    cols = ", ".join(["timestamp"] + variables)

    query = text(f"""
        SELECT {cols}
        FROM data
        WHERE timestamp BETWEEN :start AND :end
    """)

    df = pd.read_sql(query, engine, params={"start": start, "end": end})
    return df.to_dict(orient="records")