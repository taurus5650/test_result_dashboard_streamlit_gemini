from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator


class PostgresHelper:
    def __init__(self, config):
        self.engine = create_engine(
            f'postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}',
            pool_pre_ping=True
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Generator:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
