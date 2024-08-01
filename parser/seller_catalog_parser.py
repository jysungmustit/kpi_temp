from parser.base_parser import BaseParser


class SellerCatalogParser(BaseParser):
    def validate_json(self):
        # JSON 형식 검증
        for item in self.data:
            if not all(key in item for key in ["key", "doc_count", "catalog_count"]) or \
                    not isinstance(item["catalog_count"], dict) or \
                    "value" not in item["catalog_count"]:
                return False
        return True

    def parse(self):
        if not self.validate_json():
            raise ValueError("Input only seller catalog json file")

        for item in self.data:
            total_count = item["doc_count"]
            catalog_count = item["catalog_count"]["value"]
            matching_rate = (catalog_count / total_count) * 100 if total_count != 0 else 0

            self.parsed_data.append({
                "seller": item["key"],
                "total count": total_count,
                "catalog count": catalog_count,
                "matching rate": matching_rate
            })
        return self.parsed_data
