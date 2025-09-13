class DataQualityChecker:
    def has_required_columns(self, data: list[dict], required_columns: list[str]) -> bool:
        if not data:
            return False
        for row in data:
            for column in required_columns:
                if column not in row or row[column] is None:
                    return False
        return True