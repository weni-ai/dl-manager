from typing import Any, List

from datalake_manager.clients.redshift_client import RedshiftClient
from datalake_manager.config import (
    DATALAKE_API_URL,
    REDSHIFT_MSG_METRIC,
    REDSHIFT_TRACE_METRIC,
)
from datalake_manager.manager_interface import DatalakeManager


class RedshiftManager(DatalakeManager):
    def __init__(self, api_url: str = DATALAKE_API_URL):
        self.client = RedshiftClient(api_url, {"Content-Type": "application/json"})

    def execute_query(self, query: str) -> List[Any]:  # pragma: no cover
        return NotImplemented

    def insert(self, path: str, data: List[dict]) -> None:
        payload = {"name": REDSHIFT_MSG_METRIC, "kind": path, "fields": data}
        response = self.client.send(payload)
        return response

    def insert_trace(self, path: str, data: List[dict]) -> None:
        payload = {"name": REDSHIFT_TRACE_METRIC, "kind": path, "fields": data}
        response = self.client.send(payload)
        return response
