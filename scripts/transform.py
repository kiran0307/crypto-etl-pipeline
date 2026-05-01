import pandas as pd
import logging

from logger_config import setup_logger

setup_logger()


def transform_data():
    try:
        logging.info("Starting transform step")

        df = pd.read_csv("../data/crypto_raw.csv")

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

        df.to_csv("../data/crypto_transformed.csv", index=False)

        logging.info("Transformed data saved successfully to ../data/crypto_transformed.csv")
        logging.info(f"Transformed row count: {len(df)}")

    except FileNotFoundError:
        logging.error("Input file ../data/crypto_raw.csv not found")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in transform step: {e}")
        raise


if __name__ == "__main__":
    transform_data()