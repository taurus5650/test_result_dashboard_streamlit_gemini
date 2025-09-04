# database/config.py
import os, logging

class SDETDatabase:
    DB_HOST = os.getenv('POSTGRES_HOST') or os.getenv('DB_HOST') or '127.0.0.1'
    DB_USER = os.getenv('POSTGRES_USER') or os.getenv('DB_USER') or 'sdet'
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD') or os.getenv('DB_PASSWORD') or '1234'
    DB_NAME = os.getenv('POSTGRES_DB') or os.getenv('DB_NAME') or 'sdet_database'
    DB_PORT = int(os.getenv('POSTGRES_PORT') or os.getenv('DB_PORT') or 5432)