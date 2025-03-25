import os

DATALAKE_API_URL = os.getenv("DATALAKE_API_URL", "https://rc.vtex.com/api/analytics/schemaless-events")
REDSHIFT_METRIC = os.getenv("REDSHIFT_METRIC", "redshift_metric")
