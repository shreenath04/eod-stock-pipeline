# Serverless EOD Stock Data Pipeline

A fully automated serverless pipeline that collects and updates end-of-day OHLCV market data for 4,000+ NYSE stocks every night after market close. Zero manual intervention post-deployment.

## Architecture

EventBridge (cron: Mon-Fri 9PM UTC) → Lambda → S3

## Screenshots

<img width="1652" height="683" alt="Screenshot 2026-03-17 at 1 13 23 AM" src="https://github.com/user-attachments/assets/72f5a992-3d0b-4df7-a1ec-4adf88ff39f7" />

<img width="534" height="309" alt="Screenshot 2026-03-17 at 1 13 51 AM" src="https://github.com/user-attachments/assets/a9591814-d9c9-4bf3-a55e-fada7c7b5e94" />

<img width="532" height="304" alt="Screenshot 2026-03-17 at 1 13 57 AM" src="https://github.com/user-attachments/assets/3dfeb9e7-4b27-4b29-93f1-521d1eb94d76" />

<img width="1646" height="961" alt="Screenshot 2026-03-17 at 1 14 30 AM" src="https://github.com/user-attachments/assets/9c239efe-b036-4ea8-8c26-1c948a692e7a" />

<img width="1306" height="118" alt="Screenshot 2026-03-17 at 1 16 10 AM" src="https://github.com/user-attachments/assets/7554794c-8d77-4142-b9c0-4777dcce3a95" />


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
