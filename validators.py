import re
from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Optional


def validate_currency(raw: str) -> Optional[Decimal]:
    if not raw or not raw.strip():
        return None
    cleaned = raw.strip().replace("R$", "").replace(" ", "")
    if "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    try:
        value = Decimal(cleaned)
        if value <= 0:
            return None
        return value
    except (InvalidOperation, ValueError):
        return None


CURRENCY_HELP = "Use apenas números, ex: 1500,50 ou 1500.50"


def validate_brazilian_date(raw: str) -> Optional[datetime]:
    if not raw or not raw.strip():
        return None
    match = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", raw.strip())
    if not match:
        return None
    day, month, year = match.groups()
    try:
        return datetime(int(year), int(month), int(day))
    except ValueError:
        return None


DATE_HELP = "Use o formato DD/MM/AAAA, ex: 15/03/2026"


def validate_non_empty(raw: str) -> Optional[str]:
    if not raw or not raw.strip():
        return None
    return raw.strip()
