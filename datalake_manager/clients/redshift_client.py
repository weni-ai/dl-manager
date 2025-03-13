import requests
from typing import Dict, Any

class RedshiftClient:
    def __init__(self, base_url: str, headers: Dict[str, str]):
        self.base_url = base_url
        self.headers = headers
    
    def send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}",
            json=payload,
            headers=self.headers
        )
        return response.json()
