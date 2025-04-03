import os

DATALAKE_API_URL = os.getenv(
    "DATALAKE_API_URL", "https://rc.vtex.com/api/analytics/schemaless-events"
)
REDSHIFT_MSG_METRIC = os.getenv("REDSHIFT_MSG_METRIC", "redshift_metric")
REDSHIFT_TRACE_METRIC = os.getenv("REDSHIFT_TRACE_METRIC", "redshift_metric")
