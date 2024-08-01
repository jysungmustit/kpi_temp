import pandas as pd
import json

class BaseParser:
    def __init__(self, data):
        self.data = data
        self.parsed_data = []

    def validate_json(self):
        for item in self.data:
            if not all(key in item for key in ["key", "doc_count", "catalog_count"]) or \
               not isinstance(item["catalog_count"], dict) or \
               "value" not in item["catalog_count"]:
                return False
        return True

    def parse(self):
        raise NotImplementedError("Subclasses should implement this method!")
