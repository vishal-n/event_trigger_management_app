### Database setup and configuration

import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv

DATABASE_URL = "postgresql://test_pg_1vk2_user:NlohnDw5va25sEEtwYzaQv6eMbBLckwm@dpg-cufm5ai3esus73e27ps0-a.oregon-postgres.render.com/test_pg_1vk2"


def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        print("✅ Database connection established")
        return conn
    except psycopg2.OperationalError as e:
        print(f"⚠️ Database not ready yet: {e}. Retrying in 5 seconds...")


def setup_database():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(open("migrations/init.sql", "r").read())
            conn.commit()
        print("✅ Database setup complete")
