from database import engine
from models.data import Base, Data
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np


# Declaring the function run_seed to insert data into the database
def run_seed():
    Base.metadata.create_all(bind=engine)

    start = pd.Timestamp("2024-01-01")
    periods = 10 * 24 * 60

    with Session(engine) as session:
        for i in range(periods):
            data = Data(
                timestamp=start + pd.Timedelta(minutes=i),
                wind_speed=np.random.uniform(3, 20),
                power=np.random.uniform(100, 500),
                ambient_temperature=np.random.uniform(15, 35),
            )
            session.add(data)

        session.commit()

    print("Seed completed.")

if __name__ == "__main__":
    run_seed()