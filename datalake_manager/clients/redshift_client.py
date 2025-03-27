import json
import requests
from typing import Dict, Any

from datalake_manager.config import DATALAKE_API_URL

class RedshiftClient:
    def __init__(self, base_url, headers):
        self.base_url = DATALAKE_API_URL
        self.headers = {"Content-Type": "application/json"}
    
    def send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        json_payload = json.dumps(payload, ensure_ascii=False)
        response = requests.post(
            url=self.base_url,
            data=json_payload,
            headers=self.headers,
        )

        return response
