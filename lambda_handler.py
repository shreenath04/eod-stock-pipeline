import json
import logging
from pipeline import run_pipeline

log = logging.getLogger()
log.setLevel(logging.INFO)

def handler(event, context):
    try:
        summary = run_pipeline()
        return {
            "statusCode": 200,
            "body": json.dumps(summary)
        }
    except Exception as e:
        log.error(f"Pipeline failed: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }