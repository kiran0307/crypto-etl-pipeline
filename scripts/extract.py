import requests
import pandas as pd
import os
import logging
import time

from logger_config import setup_logger

setup_logger()


def extract_data():
    try:
        logging.info("Starting extract step")

        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 50,
            "page": 1,
            "sparkline": False
        }

        max_retries = 3
        retry_delay = 5
        response = None

        for attempt in range(1, max_retries + 1):
            try:
                logging.info(f"API request attempt {attempt}")
                response = requests.get(url, params=params, timeout=15)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                logging.warning(f"Attempt {attempt} failed: {e}")
                if attempt == max_retries:
                    raise
                time.sleep(retry_delay)

        data = response.json()

        if not data:
            raise ValueError("API returned empty data.")

        df = pd.DataFrame(data)

        if df.empty:
            raise ValueError("Extracted DataFrame is empty.")

        os.makedirs("../data/raw/crypto", exist_ok=True)
        df.to_csv("../data/raw/crypto/crypto_raw.csv", index=False)

        logging.info("Raw data saved successfully to ../data/raw/crypto/crypto_raw.csv")
        logging.info(f"Extracted {len(df)} records")

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in extract step: {e}")
        raise


if __name__ == "__main__":
    extract_data()