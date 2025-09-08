import pandas

from database.config import SDETDatabase
from database.postgresql_helper import PostgresSQLHelper


class BusinessLogic:
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
            WHERE create_time >= %s
                AND create_time < %s 
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
                AND start_time >= %s
                AND start_time < %s 
                AND jsonb_array_length(failure_records) > 0
            ORDER BY start_time DESC;
        """)
        result = self.db.execute(sql=sql, params=(service_team, start_date, end_date), fetchall=True)
        return pandas.DataFrame(result, columns=['service_team', 'service', 'case_name', 'error_message', 'traceback', 'timestamp'])

