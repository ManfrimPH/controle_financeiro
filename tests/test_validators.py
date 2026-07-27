from decimal import Decimal
from datetime import datetime
import sys
sys.path.insert(0, "/home/manfrim/projetos/controle_financeiro")

from validators import (
    validate_currency,
    validate_brazilian_date,
    validate_non_empty,
)


def test_validate_currency_valid():
    assert validate_currency("1500,50") == Decimal("1500.50")
    assert validate_currency("1500.50") == Decimal("1500.50")
    assert validate_currency("R$ 1.500,50") == Decimal("1500.50")
    assert validate_currency("0,01") == Decimal("0.01")


def test_validate_currency_invalid():
    assert validate_currency("") is None
    assert validate_currency("abc") is None
    assert validate_currency("-10") is None
    assert validate_currency("0") is None


def test_validate_brazilian_date_valid():
    result = validate_brazilian_date("15/03/2026")
    assert result is not None
    assert result.day == 15
    assert result.month == 3
    assert result.year == 2026


def test_validate_brazilian_date_invalid():
    assert validate_brazilian_date("") is None
    assert validate_brazilian_date("32/13/2026") is None
    assert validate_brazilian_date("15-03-2026") is None
    assert validate_brazilian_date("abc") is None


def test_validate_non_empty():
    assert validate_non_empty("abc") == "abc"
    assert validate_non_empty("  abc  ") == "abc"
    assert validate_non_empty("") is None
    assert validate_non_empty("   ") is None
