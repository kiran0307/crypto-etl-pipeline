import os
import logging
import uuid
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from logger_config import setup_logger

setup_logger()

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


def load_to_postgres():
    try:
        logging.info("Starting load step")

        df = pd.read_csv("../data/processed/crypto/crypto_transformed.csv")
        
        if df.empty:
            raise ValueError("Transformed input file is empty.")
            

        batch_id = str(uuid.uuid4())
        load_timestamp = pd.Timestamp.now()

        df["batch_id"] = batch_id
        df["load_timestamp"] = load_timestamp

        df = df.drop_duplicates(subset=["id", "batch_id"])

        username = os.getenv("DB_USER")
        password_raw = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")

        if not all([username, password_raw, host, port, database]):
            raise ValueError(
                "Missing one or more DB environment variables. "
                "Check .env file and variable names."
            )

        password = quote_plus(password_raw)

        engine = create_engine(
            f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
        )

        with engine.begin() as connection:
            # Append to historical table
            df.to_sql(
                "crypto_prices_history",
                con=connection,
                if_exists="append",
                index=False
            )

            # Refresh current table without dropping schema
            connection.execute(text("DELETE FROM crypto_prices_current"))

            df.to_sql(
                "crypto_prices_current",
                con=connection,
                if_exists="append",
                index=False
            )

        with engine.connect() as connection:
            history_count = connection.execute(
                text("SELECT COUNT(*) FROM crypto_prices_history")
            ).scalar()

            current_count = connection.execute(
                text("SELECT COUNT(*) FROM crypto_prices_current")
            ).scalar()

        logging.info("Data appended to crypto_prices_history")
        logging.info("Data refreshed in crypto_prices_current")
        logging.info(f"Loaded row count: {len(df)}")
        logging.info(f"Batch ID: {batch_id}")
        logging.info(f"History table row count: {history_count}")
        logging.info(f"Current table row count: {current_count}")

    except FileNotFoundError:
        logging.error("Input file ../data/processed/crypto/crypto_transformed.csv not found")
        raise
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in load step: {e}")
        raise


if __name__ == "__main__":
    load_to_postgres()