import os
import sys
import httpx
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from target_models import Base, Signal


def run_etl(date: str):

    try:
        SOURCE_API = os.getenv("SOURCE_API_URL")
        API_TOKEN  = os.getenv("API_TOKEN")

        TARGET_DB = (
            f"postgresql://{os.getenv('TARGET_DB_USER')}:"
            f"{os.getenv('TARGET_DB_PASSWORD')}@"
            f"{os.getenv('TARGET_DB_HOST')}:"
            f"{os.getenv('TARGET_DB_PORT')}/"
            f"{os.getenv('TARGET_DB_NAME')}"
        )

        engine = create_engine(TARGET_DB)
        Base.metadata.create_all(bind=engine)

        start = f"{date} 00:00:00"
        end = f"{date} 23:59:59"

        # =========================
        # API REQUEST
        # =========================
        try:
            response = httpx.get(
                f"{SOURCE_API}/data",
                params={
                    "start": start,
                    "end": end,
                    "variables": ["wind_speed", "power"]
                },
                headers={
                    "Authorization": f"Bearer {API_TOKEN}"
                },
                timeout=30.0
            )
            response.raise_for_status()

        except httpx.HTTPError as e:
            print(f"[ERROR] API request failed: {e}")
            return

        df = pd.DataFrame(response.json())

        if df.empty:
            print("[INFO] No data returned for this date.")
            return

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)

        agg = df.resample("10min").agg(["mean", "min", "max", "std"])
        agg.columns = ["_".join(col) for col in agg.columns]
        agg.reset_index(inplace=True)

        # =========================
        # DATABASE OPERATIONS
        # =========================
        try:
            with Session(engine) as session:

                # Idempotência
                session.execute(
                    text("DELETE FROM data WHERE timestamp BETWEEN :start AND :end"),
                    {"start": start, "end": end}
                )
                session.commit()

                signals = {}

                for col in agg.columns:
                    if col == "timestamp":
                        continue

                    signal = session.query(Signal).filter_by(name=col).first()
                    if not signal:
                        signal = Signal(name=col)
                        session.add(signal)
                        session.commit()
                        session.refresh(signal)

                    signals[col] = signal.id

                rows = []

                for col, signal_id in signals.items():
                    temp = agg[["timestamp", col]].copy()
                    temp["signal_id"] = signal_id
                    temp.rename(columns={col: "value"}, inplace=True)
                    rows.append(temp)

                final_df = pd.concat(rows)

                final_df.to_sql("data", engine, if_exists="append", index=False)

        except SQLAlchemyError as e:
            print(f"[ERROR] Database operation failed: {e}")
            return

        print("ETL completed successfully.")

    except Exception as e:
        print(f"[CRITICAL] Unexpected error: {e}")


if __name__ == "__main__":
    run_etl(sys.argv[1])