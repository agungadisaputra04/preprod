import os
import psycopg
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "api_lab"),
    "user": os.getenv("DB_USER", "api_lab_app"),
    "password": os.getenv("DB_PASSWORD"),
}


def get_connection():
    return psycopg.connect(**DB_CONFIG)
