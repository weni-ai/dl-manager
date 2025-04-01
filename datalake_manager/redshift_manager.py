from typing import Any, List

from datalake_manager.clients.redshift_client import RedshiftClient
from datalake_manager.config import DATALAKE_API_URL, REDSHIFT_METRIC
from datalake_manager.manager_interface import DatalakeManager


class RedshiftManager(DatalakeManager):
    def __init__(self, metric: str = REDSHIFT_METRIC, api_url: str = DATALAKE_API_URL):
        self.client = RedshiftClient(api_url, {"Content-Type": "application/json"})
        self.metric = metric

    def execute_query(self, query: str) -> List[Any]:
        return NotImplemented

    def insert(self, path: str, data: List[dict]) -> None:
        payload = {"name": self.metric, "kind": path, "fields": data}
        response = self.client.send(payload)
        return response
