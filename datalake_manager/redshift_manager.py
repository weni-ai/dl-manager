from typing import Any, List

from datalake_manager.clients.redshift_client import RedshiftClient
from datalake_manager.config import (
    DATALAKE_API_URL,
    REDSHIFT_MESSAGE_TEMPLATE_METRIC,
    REDSHIFT_MESSAGE_TEMPLATE_STATUS_METRIC,
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

    def insert_message_template(self, message_template_dict: dict) -> None:
        payload = {
            "name": REDSHIFT_MESSAGE_TEMPLATE_METRIC,
            "contact_urn": message_template_dict["contact_urn"],
            "channel": message_template_dict["channel"],
            "template_language": message_template_dict["template_language"],
            "template_name": message_template_dict["template_name"],
            "template_uuid": message_template_dict["template_uuid"],
            "message_id": message_template_dict["message_id"],
            "direction": message_template_dict["direction"],
            "template_variables": message_template_dict["template_variables"],
            "text": message_template_dict["text"],
            "fields": message_template_dict["data"],
        }

        response = self.client.send(payload)
        return response

    def insert_message_template_status(
        self, message_template_status_dict: dict
    ) -> None:
        payload = {
            "name": REDSHIFT_MESSAGE_TEMPLATE_STATUS_METRIC,
            "contact_urn": message_template_status_dict["contact_urn"],
            "status": message_template_status_dict["status"],
            "message_id": message_template_status_dict["message_id"],
            "template_type": message_template_status_dict["template_type"],
            "channel": message_template_status_dict["channel"],
            "data": message_template_status_dict["data"],
        }

        response = self.client.send(payload)
        return response
