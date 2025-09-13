import os

def get_config():
    return {
        "env": os.getenv("ENVIRONMENT", "dev"),
        "client_ids": ["19136"],
        "eff_dt": "2024-01-01",
        "end_dt": "2024-03-01",
        "add_dummy": True,
        "layout_cols": [
            "Carrier Code", "Group Number", "Patient Num", "Coverage Type", "Person Code",
            "Family Code", "Last Name", "First Name", "Middle Name", "Gender",
            "Date of Birth", "Relationship Code", "SSN", "Address (line 1)",
            "Address (line 2)", "City", "State", "Zip Code", "Home Phone",
            "Work Phone", "Email Address", "Coverage Effective Date",
            "Coverage Termination Date", "Cell Phone", "Old Patient Num"
        ],
        "container": "etl-load/Migration",
        "notifier_recipients": "data-alerts@pbmcompany.com;DataOperations@pbmcompany.com"
    }