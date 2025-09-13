from datetime import datetime

class ClaimDataQualityChecker:
    REQUIRED_COLUMNS = ["claim_id", "member_id", "fill_date"]

    def validate(self, records: list[dict]) -> dict:
        """
        Accepts a list of dicts representing rows of claims.
        Returns: {
            "is_valid": bool,
            "errors": ["..."]
        }
        """
        errors = []

        if not records:
            return {"is_valid": False, "errors": ["No records provided"]}

        for column in self.REQUIRED_COLUMNS:
            if column not in records[0]:
                errors.append(f"Missing required column: {column}")

        for row in records:
            if row.get("claim_id") in [None, ""]:
                errors.append("Null or empty claim_id found")

            fill_date = row.get("fill_date")
            if fill_date and isinstance(fill_date, datetime):
                if fill_date > datetime.now():
                    errors.append(f"Future fill_date: {fill_date.isoformat()}")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }