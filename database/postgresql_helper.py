import psycopg2
import logging


class PostgresSQLHelper:
    def __init__(self, config: str):
        try:
            self.connection = psycopg2.connect(
                database=config.DB_NAME,
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                port=config.DB_PORT
            )
            self.connection.autocommit = False
        except Exception as e:
            logging.error(f'postgres connection failed: {e}')
            raise

    def execute(self, sql: str, fetchall: bool = False, params: tuple = None):
        """SELECT, INSERT, UPDATE, DELETE """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                if fetchall is True:
                    result = cursor.fetchall()
                elif fetchall is False:
                    result = cursor.fetchone()
                else:
                    result = None

                self.connection.commit()
                return result

        except Exception as e:
            self.connection.rollback()
            logging.error(f'postgres execute failed: {e}')
            raise

    def close(self):
        if self.connection:
            logging.info(f'postgres connction closed.')
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
