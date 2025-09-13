from src.application.ports.iconfig_validator import IConfigValidator
from src.application.ports.ifile_uploader import IFileUploader
from src.application.ports.iaudit_tracker import IAuditTracker
from datetime import datetime

class PipelineRunner:
    def __init__(
        self,
        config_validator: IConfigValidator,
        file_uploader: IFileUploader,
        audit_tracker: IAuditTracker
    ):
        self.config_validator = config_validator
        self.file_uploader = file_uploader
        self.audit_tracker = audit_tracker

    def run(self, config: dict, file_path: str) -> str:
        pipeline_id = config.get("pipeline_id", "unknown")
        timestamp = datetime.now()

        if not self.config_validator.validate(config):
            self.audit_tracker.log_run(pipeline_id, "FAILED_CONFIG", timestamp)
            return "Invalid pipeline configuration"

        upload_result = self.file_uploader.upload(file_path, {"pipeline_id": pipeline_id})

        if upload_result == "SUCCESS":
            self.audit_tracker.log_run(pipeline_id, "SUCCESS", timestamp)
            return "Pipeline executed successfully"
        else:
            self.audit_tracker.log_run(pipeline_id, "FAILED_UPLOAD", timestamp)
            return "Pipeline failed during file upload"