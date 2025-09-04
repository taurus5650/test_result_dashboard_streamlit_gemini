import pandas
from database.postgresql_helper import PostgresSQLHelper
from database.config import SDETDatabase


class Business:
    def __init__(self):
        self.db = PostgresSQLHelper(config=SDETDatabase)

    def get_all_service_teams(self) -> pandas.DataFrame:
        sql = "SELECT DISTINCT service_team FROM automation_test_result ORDER BY service_team;"
        rows = self.db.execute(sql=sql, fetchall=True)
        return pandas.DataFrame(rows, columns=['service_team'])

    def get_failure_summary_grouped_by_service(self, start_date: str, end_date: str) -> pandas.DataFrame:
        sql = ("""
            SELECT service_team, COUNT(*) AS fail_count
            FROM automation_test_result, jsonb_array_elements(failure_records) AS failure_records
            WHERE create_time BETWEEN %s AND %s
            GROUP BY service_team
            ORDER BY fail_count DESC;
        """)

        result = self.db.execute(sql=sql, params=(start_date, end_date), fetchall=True)
        return pandas.DataFrame(result, columns=['service_team', 'fail_count'])


    # def fetch_recent_failures(self, limit=50):
    #     query = """
    #         SELECT
    #             service_team,
    #             service,
    #             failed_case ->> 'name' AS test_name,
    #             failed_case ->> 'error' AS error_message,
    #             failed_case ->> 'traceback' AS traceback,
    #             start_time AS timestamp
    #         FROM automation_test_result,
    #              jsonb_array_elements(failure_records) AS failed_case
    #         ORDER BY start_time DESC
    #         LIMIT %s;
    #     """
    #     with self.db.connection.cursor() as cursor:
    #         cursor.execute(query, (limit,))
    #         rows = cursor.fetchall()
    #         return pd.DataFrame(rows, columns=['service_team', 'service', 'test_name', 'error_message', 'traceback', 'timestamp'])
