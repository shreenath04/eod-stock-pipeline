import boto3
import io
import pandas as pd
from botocore.exceptions import ClientError
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

s3 = boto3.client("s3")
BUCKET = "shreenath-eod-pipeline"

def read_tickers():
    body = s3.get_object(Bucket=BUCKET, Key="tickers.csv")
    df = pd.read_csv(body["Body"])
    return df["ticker"].tolist()


def read_existing_csv(tkr):
    try:
        body = s3.get_object(Bucket=BUCKET, Key=f"bars1/{tkr}.csv")
        df = pd.read_csv(body["Body"])
        df["date"] = pd.to_datetime(df["date"], utc=True).dt.normalize()
        return df
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise  # if it's a different S3 error, re-raise it


def yahoo_symbol(tkr):
    return tkr.replace(".", "-")


def fetch_latest(tkr):
    try:
        df = yf.Ticker(yahoo_symbol(tkr)).history(
            period="5d",
            interval="1d",
            auto_adjust=True
        )

        if df.empty:
            return pd.DataFrame()

        df = df.reset_index()

        date_col = "Date" if "Date" in df.columns else "Datetime"

        df["date"] = (
            pd.to_datetime(df[date_col], utc=True)
              .dt.normalize()
        )

        df = df.drop(columns=[date_col, "Dividends", "Stock Splits"], errors="ignore")

        df = df.rename(columns={
            "Open":   "open",
            "High":   "high",
            "Low":    "low",
            "Close":  "close",
            "Volume": "volume"
        })

        df["timestamp"] = df["date"].astype("int64") // 10**6

        return df[["date", "open", "high", "low", "close", "volume", "timestamp"]]

    except Exception as e:
        return pd.DataFrame()


def write_to_s3(tkr, df):
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    s3.put_object(Bucket=BUCKET, Key=f"bars1/{tkr}.csv", Body=buf.getvalue())


def process_ticker(tkr):
    latest = fetch_latest(tkr)

    # If yfinance returned nothing, skip
    if latest.empty:
        return "skipped"

    existing = read_existing_csv(tkr)

    # If no existing file, write everything we fetched
    if existing is None:
        write_to_s3(tkr, latest)
        return "created"

    # Find rows not already in existing
    new_rows = latest[~latest["date"].isin(existing["date"])].copy()

    if new_rows.empty:
        return "up_to_date"

    # Append and write back
    updated = pd.concat(
        [existing, new_rows[existing.columns]],
        ignore_index=True
    ).sort_values("date").reset_index(drop=True)

    write_to_s3(tkr, updated)
    return "updated"


def run_pipeline():
    tickers = read_tickers()

    updated  = 0
    skipped  = 0
    created  = 0
    errors   = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(process_ticker, tkr): tkr for tkr in tickers}

        for future in as_completed(futures):
            tkr = futures[future]
            try:
                result = future.result()
                if result == "updated":  updated += 1
                elif result == "created": created += 1
                else:                    skipped += 1
            except Exception as e:
                errors.append(tkr)

    log = logging.info(f"Pipeline complete: updated={updated}, created={created}, skipped={skipped}, errors={len(errors)}")

    return {
        "total":   len(tickers),
        "updated": updated,
        "created": created,
        "skipped": skipped,
        "errors":  errors
    }

