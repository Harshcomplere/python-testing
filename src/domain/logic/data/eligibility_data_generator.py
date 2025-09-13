class DummyEligibilityDataGenerator:
    def __init__(self, spark):
        self.spark = spark

    def generate(self, client_filter_view: str):
        return self.spark.sql(f"""
            SELECT CLIENT, GRP_CODE, '2023-08-01' AS EFF_DT, '2035-12-31' AS END_DT,
            CONCAT('TEST', REVERSE(CLIENT), 'X') AS FAMILY_ID, '' AS SSN, 'DUMMY' AS FIRST_NAME,
            '' AS MI, 'MEMBER' AS LAST_NAME, 'M' AS GND, '1975-01-01' AS BIRTH_DT,
            '1' AS REL_CODE, '155 Chestnut Ridge Rd' AS ADDR1, '' AS ADDR2, 'Montvale' AS CITY,
            'NJ' AS STATE, '07645' AS ZIP, '' AS ZIP_EXT, '' AS HOME_PHONE, '' AS CELL_PHONE,
            '' AS WORK_PHONE, 'No' AS MEDICARE_FLG,
            CONCAT('TEST', REVERSE(CLIENT), 'X', CLIENT) AS CLIENT_CARD_ID,
            '01' AS PERSON_CODE, 'I' AS COVERAGE_TYPE, '' AS CLIENT_INT_ID,
            '' AS EMAIL_ADR, '' AS ADNL_INFO, '' AS PLAN_SELECTION_TYPE,
            '' AS PLAN_SELECTION_TYPE_EFFECTIVE_DATE, '' AS OLD_PATIENT_NUMBER
            FROM (
                SELECT Client_ID AS CLIENT, Group_Number AS GRP_CODE,
                ROW_NUMBER() OVER(PARTITION BY Client_ID ORDER BY COALESCE(termination_date, '2999-12-31') DESC) AS rank
                FROM pbm_catalogstore.gold_ods.vw_master_eligibility
                WHERE client_id IN (SELECT clientId FROM {client_filter_view})
            ) x WHERE rank = 1
        """).fillna('')
