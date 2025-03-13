import os


DATALAKE_API_URL = "https://rc.vtex.com/api/analytics/schemaless-events"
REDSHIFT_METRIC = os.getenv("REDSHIFT_METRIC", "redshift_metric")
# REDSHIFT_METRIC = "weni-product"

# Configurações do Redshift via variáveis de ambiente
REDSHIFT_HOST = os.getenv("REDSHIFT_HOST", "default-host")
REDSHIFT_USER = os.getenv("REDSHIFT_USER", "default-user")
REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD", "default-password")
REDSHIFT_DATABASE = os.getenv("REDSHIFT_DATABASE", "default-database")