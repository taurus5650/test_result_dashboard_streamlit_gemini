import psycopg2
import logging


class PostgresHelper:
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

    def query(self, command: str, fetchall: bool = False, params: tuple = None):
        """SELECT."""
        try:
            with self.connection.cursor() as cur:
                cur.execute(command, params)
                return cur.fetchall() if fetchall else cur.fetchone()
            return record
        except Exception as e:
            logging.error(f'postgres query failed: {e}')

    def execute(self, command: str, params: tuple = None):
        """INSERT, UPDATE, DELETE."""
        try:
            with self.connection.cursor() as cur:
                cur.execute(command, params)
            self.connection.commit()
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
