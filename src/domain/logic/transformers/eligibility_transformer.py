import pandas as pd
from pyspark.sql import DataFrame, Window
from pyspark.sql.functions import col, last
from src.utils.date_utils import infer_date_format

class EligibilityTransformer:
    def __init__(self, layout_cols: list[str]):
        self.layout_cols = layout_cols

    def transform(self, df: DataFrame) -> pd.DataFrame:
        win = Window.partitionBy("CLIENT_CARD_ID").orderBy("PERSON_CODE")
        df_filled = df.withColumn("COVERAGE_TYPE", last("COVERAGE_TYPE", ignorenulls=True).over(win))

        pdf = df_filled.replace("", None).toPandas()
        pdf["REL_CODE"] = pdf["REL_CODE"].replace({"9": "4", "98": "4", "99": "4"})
        pdf["Coverage Effective Date"] = pdf["Coverage Effective Date"].apply(infer_date_format)
        pdf["Coverage Termination Date"] = pdf["Coverage Termination Date"].apply(infer_date_format)
        pdf["Date of Birth"] = pdf["Date of Birth"].apply(infer_date_format)
        pdf["Coverage Type"] = pdf["Coverage Type"].str.slice(stop=1)
        return pdf.reindex(columns=self.layout_cols)