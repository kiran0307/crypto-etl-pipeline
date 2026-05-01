# Crypto ETL Data Pipeline

## Project Overview

This project is an end-to-end data engineering pipeline that ingests cryptocurrency market data from the CoinGecko API, transforms it using Python and pandas, loads current and historical snapshots into PostgreSQL, visualizes insights in Power BI, and orchestrates the workflow using Apache Airflow.

The pipeline is fully containerized using Docker, making it portable and reproducible across environments.

---

## Architecture

CoinGecko API  
→ Python Extract  
→ Raw CSV  
→ Python Transform  
→ Processed CSV  
→ PostgreSQL  
→ Power BI Dashboard  

Orchestration: Apache Airflow  
Containerization: Docker  

---

## Tech Stack

- Python
- pandas
- requests
- PostgreSQL
- SQLAlchemy
- psycopg2
- python-dotenv
- Docker
- Apache Airflow
- Power BI
- Git/GitHub

---

## Project Structure

crypto-data-pipeline/
│
├── dags/
│   └── crypto_etl_dag.py
│
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── run_pipeline.py
│   └── logger_config.py
│
├── data/
│   ├── crypto_raw.csv
│   └── crypto_transformed.csv
│
├── logs/
│   └── pipeline.log
│
├── Dockerfile
├── docker-compose.yaml
├── .dockerignore
├── .gitignore
├── requirements.txt
├── README.md
└── .env.example

---

## End-to-End Flow

1. Extract cryptocurrency data from CoinGecko API (Top 50 coins)
2. Store raw data as CSV
3. Transform data (cleaning, validation, normalization)
4. Load into PostgreSQL (current + history tables)
5. Visualize in Power BI
6. Orchestrate using Airflow
7. Containerize using Docker

---

## Real-World Problems Solved

- Fixed Python environment mismatch (pip vs python)
- Handled API failures using retry logic
- Resolved DB connection issues with special characters
- Implemented incremental loading with batch_id
- Prevented duplicate data via PK strategy
- Solved Docker networking using host.docker.internal
- Overcame Airflow Windows limitation using Docker

---

## How to Run

pip install -r requirements.txt

Create .env:

DB_USER=postgres  
DB_PASSWORD=your_password  
DB_HOST=localhost  
DB_PORT=5432  
DB_NAME=crypto_db  

Run:

python scripts/run_pipeline.py

---

## Docker

docker build -t crypto-pipeline .  
docker run --env-file .env crypto-pipeline  

---

## Airflow

docker compose up -d  

http://localhost:8080  

Trigger DAG: crypto_etl_pipeline_split  

---

## Validation

SELECT COUNT(*) FROM crypto_prices_current;  
SELECT COUNT(*) FROM crypto_prices_history;  

---

## Future Improvements

- Azure migration  
- CI/CD  
- Data quality checks  

---

## Interview Summary

Built an end-to-end ETL pipeline using Python, PostgreSQL, Docker, Airflow, and Power BI.
