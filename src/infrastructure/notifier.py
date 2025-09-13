import os
import requests

class Notifier:
    def __init__(self, config):
        self.recipients = config['notifier_recipients']
        self.environment = config['env']

    def send_no_data_alert(self, client_ids: list[str]):
        subject = f"{self.environment} - Eligibility Extract - Failed"
        body = f"<b>Eligibility records are not available for client ID(s): {', '.join(client_ids)}</b><br><br>Thanks."
        requests.post(
            url=os.getenv("NOTIFY_URL"),
            headers={"Content-Type": "application/json"},
            json={
                "subject": subject,
                "body": body,
                "recipient": self.recipients
            }
        )