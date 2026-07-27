from decimal import Decimal
from datetime import date
import sys
sys.path.insert(0, "/home/manfrim/projetos/controle_financeiro")

from models import GainEntry, SpentEntry


def test_gain_entry_defaults():
    entry = GainEntry(
        category="Salario",
        value=Decimal("5000.00"),
        description="Salario mensal",
        entry_date=date(2026, 3, 15),
    )
    assert entry.id is None
    assert entry.created_at is None


def test_gain_entry_to_dict():
    entry = GainEntry(
        category="Salario",
        value=Decimal("5000.00"),
        description="Salario mensal",
        entry_date=date(2026, 3, 15),
    )
    d = entry.to_dict()
    assert d["category"] == "Salario"
    assert d["value"] == "5000.00"
    assert d["entry_date"] == "2026-03-15"


def test_spent_entry():
    entry = SpentEntry(
        category="Lazer",
        payment_method="Credito",
        value=Decimal("150.00"),
        description="Cinema",
        entry_date=date(2026, 3, 20),
    )
    assert entry.payment_method == "Credito"
    d = entry.to_dict()
    assert d["payment_method"] == "Credito"
