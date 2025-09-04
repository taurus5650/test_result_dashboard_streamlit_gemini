import pandas
from database.postgresql_helper import PostgresSQLHelper
from database.config import SDETDatabase


class Business:
    def __init__(self):
        self.db = PostgresSQLHelper(config=SDETDatabase)

    def get_all_service_teams(self) -> pandas.DataFrame:
        sql = ("""
            SELECT DISTINCT service_team 
            FROM automation_test_result 
            ORDER BY service_team DESC;
        """)
        rows = self.db.execute(sql=sql, fetchall=True)
        return pandas.DataFrame(rows, columns=['service_team'])

    def get_failure_summary_grouped_by_service(self, start_date: str, end_date: str) -> pandas.DataFrame:
        sql = ("""
            SELECT
                service_team,
                COUNT(*) AS fail_count
            FROM automation_test_result,
                jsonb_array_elements(failure_records) AS failure_record
            WHERE create_time BETWEEN %s AND %s
            GROUP BY service_team
            ORDER BY fail_count DESC;
        """)

        result = self.db.execute(sql=sql, params=(start_date, end_date), fetchall=True)
        return pandas.DataFrame(result, columns=['service_team', 'fail_count'])

    def get_failure_details_by_team(self, service_team: str, start_date: str, end_date: str) -> pandas.DataFrame:
        sql = ("""
            SELECT
                service_team,
                service,
                failure_record ->> 'name' AS case_name,
                failure_record ->> 'error' AS error_message,
                failure_record ->> 'traceback' AS traceback,
                start_time AS timestamp
            FROM automation_test_result,
                jsonb_array_elements(failure_records) AS failure_record
            WHERE service_team = %s
                AND start_time BETWEEN %s AND %s
                AND jsonb_array_length(failure_records) > 0
            ORDER BY start_time DESC;
        """)
        result = self.db.execute(sql=sql, params=(service_team, start_date, end_date), fetchall=True)
        return pandas.DataFrame(result, columns=['service_team', 'service', 'case_name', 'error_message', 'traceback', 'timestamp'])

    def get_team_failure_ai_summary(self, service_team: str, start_date: str, end_date: str) -> dict:
        failure_df = self.get_failure_details_by_team(service_team, start_date, end_date)
        error_texts = failure_df['error_message'].tolist()

        timeout_count = sum('timeout' in e.lower() for e in error_texts)
        auth_count = sum('403' in e or '401' in e for e in error_texts)
        total = len(error_texts)

        return {
            "summary": f"{total} test cases failed in total during the selected period.",
            "root_cause_analysis": f"Timeout: {timeout_count} cases, Auth errors: {auth_count} cases.",
            "suggestions": [
                "Check backend service health and response times.",
                "Add retry logic or increase timeout threshold.",
                "Ensure valid auth token setup in test config."
            ]
        }


