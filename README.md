# Serverless EOD Stock Data Pipeline

A fully automated serverless pipeline that collects and updates end-of-day OHLCV market data for 4,000+ NYSE stocks every night after market close. Zero manual intervention post-deployment.

## Architecture

EventBridge (cron: Mon-Fri 9PM UTC) → Lambda → S3

## What it does

- Fetches end-of-day OHLCV data for 4,000+ tickers using yFinance
- Normalizes timestamps to UTC for consistency
- Deduplicates records and appends only new data
- Stores cleaned CSV files to AWS S3
- Runs automatically every weeknight via EventBridge cron trigger
- Processes 3M+ records with 50 parallel workers via ThreadPoolExecutor

## Stack

- **AWS Lambda** — serverless compute
- **AWS EventBridge** — scheduled cron trigger
- **AWS S3** — cloud storage
- **Python** — pipeline logic
- **yFinance** — market data ingestion
- **Pandas** — data processing
- **ThreadPoolExecutor** — parallel fetching

## Performance

- 4,000+ tickers processed per run
- 3M+ total records
- Full pipeline completes in under 10 minutes
- 0 errors on production runs

## Project Status

**Phase 1 — Complete:** Nightly data ingestion and storage pipeline live on AWS.

**Phase 2 — In progress:** ML-based stock behavior modeling and anomaly detection layer.
