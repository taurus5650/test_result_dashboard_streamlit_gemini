# database/config.py
import os, logging

class SDETDatabase:
    DB_HOST = os.getenv('POSTGRES_HOST') or os.getenv('DB_HOST') or '127.0.0.1'
    DB_USER = os.getenv('POSTGRES_USER') or os.getenv('DB_USER') or 'sdet'
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD') or os.getenv('DB_PASSWORD') or '1234'
    DB_NAME = os.getenv('POSTGRES_DB') or os.getenv('DB_NAME') or 'sdet_database'
    DB_PORT = int(os.getenv('POSTGRES_PORT') or os.getenv('DB_PORT') or 5432)

    @classmethod
    def normalize(cls):
        # 防呆：有人把 host 寫成 5432 時，幫忙交換
        if str(cls.DB_HOST).isdigit():
            logging.warning(f"[DB CONFIG] Detected DB_HOST='{cls.DB_HOST}' looks like a port. "
                            f"Swapping with DB_PORT={cls.DB_PORT}.")
            old_host, old_port = cls.DB_HOST, cls.DB_PORT
            cls.DB_HOST = 'localhost'  # 預設個安全值；若在容器內可改成 'postgres'
            cls.DB_PORT = int(old_host) if old_host.isdigit() else old_port

    @classmethod
    def debug_print(cls):
        logging.info(f"[DB CONFIG] host={cls.DB_HOST} port={cls.DB_PORT} "
                     f"name={cls.DB_NAME} user={cls.DB_USER} (password hidden)")
