import logging
from decimal import Decimal, InvalidOperation
from datetime import datetime

from models import GainEntry, SpentEntry
import db

logger = logging.getLogger("finance_bot.data_base")


def _parse_date(raw: str) -> datetime | None:
    try:
        return datetime.strptime(raw.strip(), "%d/%m/%Y").date()
    except (ValueError, AttributeError):
        return None


def _parse_value(raw: str) -> Decimal | None:
    try:
        cleaned = raw.strip().replace(",", ".").replace("R$", "").strip()
        value = Decimal(cleaned)
        if value <= 0:
            return None
        return value
    except (InvalidOperation, ValueError):
        return None


def add_gain(dados: dict) -> bool:
    entry = GainEntry(
        category=dados.get("category", ""),
        value=_parse_value(dados.get("value", "0")) or Decimal("0"),
        description=dados.get("description", ""),
        entry_date=_parse_date(dados.get("date", "")) or datetime.now().date(),
    )
    return db.add_gain(entry)


def add_spent(dados: dict) -> bool:
    entry = SpentEntry(
        category=dados.get("category", ""),
        payment_method=dados.get("payment_method", ""),
        value=_parse_value(dados.get("value", "0")) or Decimal("0"),
        description=dados.get("description", ""),
        entry_date=_parse_date(dados.get("date", "")) or datetime.now().date(),
    )
    return db.add_spent(entry)


def delete(dados: dict) -> bool:
    return db.delete_last(dados.get("local", ""))


def get_all(table: str):
    return db.get_all(table)
