import pandas as pd
import logging
from azure_storage import upload_file_to_adls
import os

from logger_config import setup_logger

setup_logger()


def transform_data():
    try:
        logging.info("Starting transform step")

        df = pd.read_csv("../data/raw/crypto/crypto_raw.csv")

        if df.empty:
            raise ValueError("Raw input file is empty.")

        required_columns = [
            "id",
            "symbol",
            "name",
            "current_price",
            "market_cap",
            "market_cap_rank",
            "total_volume",
            "high_24h",
            "low_24h",
            "price_change_percentage_24h",
            "circulating_supply",
            "last_updated"
        ]

        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        df = df[required_columns].copy()

        df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
        df["symbol"] = df["symbol"].str.upper().str.strip()
        df["name"] = df["name"].astype(str).str.strip()

        df = df.dropna(subset=["id", "symbol", "name", "current_price", "last_updated"])
        df = df.drop_duplicates(subset=["id"])

        if df.empty:
            raise ValueError("Transformed DataFrame is empty after cleaning.")

        os.makedirs("../data/processed/crypto", exist_ok=True)

        local_processed_path = "../data/processed/crypto/crypto_transformed.csv"
        df.to_csv(local_processed_path, index=False)

        upload_file_to_adls(
        local_file_path=local_processed_path,
        blob_path="processed/crypto/crypto_transformed.csv"
)

        logging.info("Transformed data saved locally and uploaded to ADLS")
        logging.info(f"Transformed row count: {len(df)}")

    except FileNotFoundError:
        logging.error("Input file ../data/raw/crypto/crypto_raw.csv not found")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in transform step: {e}")
        raise


if __name__ == "__main__":
    transform_data()