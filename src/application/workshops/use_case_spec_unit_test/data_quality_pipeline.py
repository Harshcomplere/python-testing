from src.application.ports.iconfig_validator import IConfigValidator
from src.application.ports.iblob_storage_client import IBlobStorageClient
from src.application.ports.iaudit_tracker import IAuditTracker
from src.application.ports.idata_quality_checker import IDataQualityChecker
class DataQualityPipeline:
    def __init__(
        self,
        config_validator: IConfigValidator,
        blob_client: IBlobStorageClient,
        audit_tracker: IAuditTracker,
        dq_checker: IDataQualityChecker
    ):
        self.config_validator = config_validator
        self.blob_client = blob_client
        self.audit_tracker = audit_tracker
        self.dq_checker = dq_checker

    def run(self, config: dict, file_path: str) -> str:
        if not config.get("enabled", True):
            self.audit_tracker.log_run_message("Pipeline execution skipped: disabled in config")
            return "Pipeline skipped"

        errors = self.config_validator.validate(config)
        if errors:
            self.audit_tracker.log_run_message(f"Pipeline execution failed: config errors - {errors}")
            return "Invalid configuration"

        dq_result = self.dq_checker.check(file_path)
        if not dq_result.get("passed", False):
            self.audit_tracker.log_run_message(f"Pipeline execution failed: data quality issues - {dq_result['issues']}")
            return "Data quality check failed"

        uploaded = self.blob_client.upload_file(file_path, config["container"])
        if not uploaded:
            self.audit_tracker.log_run_message("Pipeline execution failed: file upload unsuccessful")
            return "Upload failed"

        self.audit_tracker.log_run_message("Pipeline execution succeeded")
        return "Pipeline completed successfully"