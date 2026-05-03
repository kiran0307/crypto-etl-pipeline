from extract import extract_data
from transform import transform_data
#from load import load_to_postgres
from load import load_to_database
import logging
from logger_config import setup_logger

setup_logger()

def run_pipeline():
    try:
        extract_data()
        transform_data()
        #load_to_postgres()
        load_to_database()
        logging.info("Pipeline completed successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()