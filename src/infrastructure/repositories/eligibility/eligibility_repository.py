class EligibilityRepository:
    def __init__(self, spark):
        self.spark = spark

    def read_eligibility(self, client_filter_view: str, eff_dt: str, end_dt: str):
        return self.spark.sql(f"""
            SELECT a.client_id AS CLIENT, a.group_number AS GRP_CODE,
                   '{eff_dt}' AS EFF_DT, '{end_dt}' AS END_DT,
                   a.family_code AS FAMILY_ID, a.social_security_number AS SSN,
                   a.first_name AS FIRST_NAME, '' AS MI, a.last_name AS LAST_NAME,
                   a.gender AS GND, a.birthdate AS BIRTH_DT,
                   a.relationship_code AS REL_CODE, a.address_line_1 AS ADDR1,
                   a.address_line_2 AS ADDR2, a.city AS CITY, a.state AS STATE,
                   a.zip_code AS ZIP, '' AS ZIP_EXT, a.home_phone AS HOME_PHONE,
                   '' AS CELL_PHONE, '' AS WORK_PHONE, a.medicare_eligible AS MEDICARE_FLG,
                   a.cardholder_id AS CLIENT_CARD_ID, a.coverage_type AS COVERAGE_TYPE,
                   a.person_code AS PERSON_CODE, a.client_internal_member_id AS CLIENT_INT_ID,
                   a.email AS EMAIL_ADR, '' AS ADNL_INFO, '' AS PLAN_SELECTION_TYPE,
                   '' AS PLAN_SELECTION_TYPE_EFFECTIVE_DATE, b.Old_Card_ID AS OLD_PATIENT_NUMBER
            FROM pbm_catalogstore.datafeeds.master_eligibility a
            LEFT OUTER JOIN pbm_catalogstore.ods.ODS_CARD_ID_XWALK b
            ON a.cardholder_id = b.New_Card_ID AND a.person_code = b.New_Person_Code
            WHERE a.Client_ID IN (SELECT clientId FROM {client_filter_view})
        """)
