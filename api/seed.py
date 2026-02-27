import pandas as pd
import numpy as np
from database import engine
from models import Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

start = pd.Timestamp("2024-01-01")
periods = 10 * 24 * 60

df = pd.DataFrame({
    "timestamp": pd.date_range(start, periods=periods, freq="1min"),
    "wind_speed": np.random.uniform(3, 20, periods),
    "power": np.random.uniform(100, 500, periods),
    "ambient_temperature": np.random.uniform(15, 35, periods),
})

df.to_sql("data", engine, if_exists="replace", index=False)

print("Seed completed.")