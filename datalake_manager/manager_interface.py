from abc import ABC, abstractmethod
from typing import Any, List


class DatalakeManager(ABC):
    """
    Interface to implement a DataLake.
    """

    @abstractmethod
    def execute_query(self, query: str) -> List[Any]:
        pass

    @abstractmethod
    def insert(self, table: str, data: List[dict]) -> None:
        pass
