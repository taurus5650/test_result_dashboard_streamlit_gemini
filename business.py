# business.py
import pandas as pd
from database.postgres_helper import PostgresHelper
from database.config import SDETDatabase

class Business:
    def __init__(self):
        self.db = PostgresHelper(config=SDETDatabase)

    def fetch_failure_summary_grouped_by_service(self):
        query = """
            SELECT service_team,
                   COUNT(*) AS fail_count
            FROM automation_test_result,
                 jsonb_array_elements(failure_records) AS failed_case
            GROUP BY service_team
            ORDER BY fail_count DESC;
        """
        with self.db.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return pd.DataFrame(rows, columns=['service_team', 'fail_count'])

    def fetch_recent_failures(self, limit=50):
        query = """
            SELECT
                service_team,
                service,
                failed_case ->> 'name' AS test_name,
                failed_case ->> 'error' AS error_message,
                failed_case ->> 'traceback' AS traceback,
                start_time AS timestamp
            FROM automation_test_result,
                 jsonb_array_elements(failure_records) AS failed_case
            ORDER BY start_time DESC
            LIMIT %s;
        """
        with self.db.connection.cursor() as cursor:
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            return pd.DataFrame(rows, columns=['service_team', 'service', 'test_name', 'error_message', 'traceback', 'timestamp'])
