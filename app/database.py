### Database setup and configuration

import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv


DB_SETTINGS = {
    "host": getenv("DB_HOST"),
    "database": getenv("DB_NAME"),
    "user": getenv("DB_USER", "postgres"),
    "password": getenv("DB_PASSWORD")
}


def get_db_connection():
    return psycopg2.connect(**DB_SETTINGS, cursor_factory=RealDictCursor)


def setup_database():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(open("migrations/init.sql", "r").read())
            conn.commit()
