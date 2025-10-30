import json
import os
import logging
from typing import Dict, Any
logger = logging.getLogger("storage")
class Storage:
    def __init__(self, path: str):
        self.path = path
    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            logger.debug(f"Storage file {self.path} does not exist; returning empty dict")
            return {}
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(f"Loaded storage from {self.path}")
                return data
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load storage from {self.path}: {e}")
            return {}
    def save(self, data: Dict[str, Any]):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                logger.debug(f"Saved storage to {self.path}")
        except IOError as e:
            logger.error(f"Failed to save storage to {self.path}: {e}")
