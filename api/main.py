from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy import text
from database import engine
import pandas as pd
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

security = HTTPBearer()

API_TOKEN = os.getenv("API_TOKEN")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )

@app.get("/data")
def get_data(
    start: str,
    end: str,
    variables: list[str] = Query(...),
    credentials: HTTPAuthorizationCredentials = Depends(verify_token),
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