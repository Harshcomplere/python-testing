from datetime import datetime
from application.ports.iblob_storage_client import IBlobStorageClient
from application.ports.ireport_generator import IReportGenerator
from application.ports.inotification_service import INotificationService

class ReportUploader:
    def __init__(
        self,
        generator: IReportGenerator,
        storage: IBlobStorageClient,
        notifier: INotificationService
    ):
        self.generator = generator
        self.storage = storage
        self.notifier = notifier

    def upload_daily_report(self, data: list[dict], recipient: str) -> str:
        if not data:
            self.notifier.send("No claims data to process today.", recipient)
            return "No data to report"

        if not all("claim_id" in row for row in data):
            self.notifier.send("Malformed data: missing 'claim_id'.", recipient)
            return "Invalid data"

        csv = self.generator.generate(data)
        path = f"reports/claims/daily_report_{datetime.now().strftime('%Y%m%d')}.csv"
        uri = self.storage.upload(csv, path)

        self.notifier.send(f"Daily report uploaded: {uri}", recipient)
        return uri
