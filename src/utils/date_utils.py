from dateutil.parser import parse

def infer_date_format(date_str: str) -> str | None:
    try:
        parsed_date = parse(date_str, fuzzy=True)
        return parsed_date.strftime("%Y-%m-%d")
    except Exception:
        return None