import os
import logging
from contextlib import contextmanager
from decimal import Decimal
from datetime import date, datetime
from typing import Optional

from psycopg2 import pool
from psycopg2.extensions import AsIs
from dotenv import load_dotenv

from models import GainEntry, SpentEntry

load_dotenv()
logger = logging.getLogger("finance_bot.db")

VALID_TABLES = {"gain", "spent"}


class DatabasePool:
    _pool = None

    @classmethod
    def initialize(cls, minconn=1, maxconn=5):
        if cls._pool is not None:
            return
        cls._pool = pool.ThreadedConnectionPool(
            minconn, maxconn,
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_DATABASE", "financeiro"),
            user=os.getenv("DB_USER", "manfrim"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT", 5432)),
        )
        logger.info("Database pool initialized (min=%d, max=%d)", minconn, maxconn)

    @classmethod
    def close(cls):
        if cls._pool is not None:
            cls._pool.closeall()
            cls._pool = None
            logger.info("Database pool closed")


@contextmanager
def get_connection():
    if DatabasePool._pool is None:
        DatabasePool.initialize()
    conn = DatabasePool._pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        DatabasePool._pool.putconn(conn)


def add_gain(entry: GainEntry) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO financeiro.gain (category, value, description, date)
                   VALUES (%s, %s, %s, %s)""",
                (entry.category, entry.value, entry.description, entry.entry_date),
            )
            return cur.rowcount > 0


def add_spent(entry: SpentEntry) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO financeiro.spent (category, payment_method, value, description, date)
                   VALUES (%s, %s, %s, %s, %s)""",
                (entry.category, entry.payment_method, entry.value, entry.description, entry.entry_date),
            )
            return cur.rowcount > 0


def delete_last(table: str) -> bool:
    if table not in VALID_TABLES:
        raise ValueError(f"Invalid table: {table}")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM financeiro.%s WHERE id = (SELECT max(id) FROM financeiro.%s)",
                (AsIs(table), AsIs(table)),
            )
            return cur.rowcount > 0


def get_all(table: str):
    if table not in VALID_TABLES:
        raise ValueError(f"Invalid table: {table}")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM financeiro.%s ORDER BY id", (AsIs(table),))
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return rows, columns


def get_last(table: str, limit: int = 10):
    if table not in VALID_TABLES:
        raise ValueError(f"Invalid table: {table}")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM financeiro.%s ORDER BY id DESC LIMIT %s",
                (AsIs(table), limit),
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return rows, columns


def get_monthly_summary(table: str):
    if table not in VALID_TABLES:
        raise ValueError(f"Invalid table: {table}")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT category, SUM(value) as total, COUNT(*) as count
                   FROM financeiro.%s
                   WHERE date >= date_trunc('month', CURRENT_DATE)
                     AND date < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'
                   GROUP BY category
                   ORDER BY total DESC""",
                (AsIs(table),),
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return rows, columns


def get_monthly_totals():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COALESCE(SUM(value), 0) FROM financeiro.gain "
                "WHERE date >= date_trunc('month', CURRENT_DATE) "
                "AND date < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'"
            )
            total_gain = cur.fetchone()[0]
            cur.execute(
                "SELECT COALESCE(SUM(value), 0) FROM financeiro.spent "
                "WHERE date >= date_trunc('month', CURRENT_DATE) "
                "AND date < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'"
            )
            total_spent = cur.fetchone()[0]
            return total_gain, total_spent
