from src.infrastructure.repositories.eligibility.eligibility_repository import EligibilityRepository
from src.infrastructure.notifier import Notifier
from src.infrastructure.blob_uploader import BlobUploader
from src.domain.logic.data.eligibility_data_generator import DummyEligibilityDataGenerator
from src.domain.logic.transformers.eligibility_transformer import EligibilityTransformer

print("hello")

class EligibilityService:
    def __init__(self, spark, config):
        self.spark = spark
        self.repo = EligibilityRepository(spark)
        self.notifier = Notifier(config)
        self.uploader = BlobUploader(config)
        self.generator = DummyEligibilityDataGenerator(spark)
        self.transformer = EligibilityTransformer(config['layout_cols'])
        self.config = config

    def run(self):
        client_view = "client_filter"
        client_ids = self.config['client_ids']
        eff_dt = self.config['eff_dt']
        end_dt = self.config['end_dt']

        # Load base data
        df = self.repo.read_eligibility(client_view, eff_dt, end_dt)

        if df.count() == 0:
            self.notifier.send_no_data_alert(client_ids)
            raise Exception("No eligibility data found.")

        # Optionally append dummy records
        if self.config.get("add_dummy"):
            dummy_df = self.generator.generate(client_view)
            df = df.unionByName(dummy_df)

        # Transform and upload
        pdf = self.transformer.transform(df)
        csv_content = pdf.to_csv(index=False).encode("utf-8")
        filename = f"Eligibility_{'_'.join(client_ids)}.csv"
        self.uploader.upload_csv(filename, csv_content)