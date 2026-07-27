from dataclasses import dataclass, field, asdict
from decimal import Decimal
from datetime import date, datetime
from typing import Optional


@dataclass
class GainEntry:
    category: str
    value: Decimal
    description: str
    entry_date: date
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        result = asdict(self)
        result["value"] = str(result["value"])
        result["entry_date"] = self.entry_date.isoformat()
        if self.created_at:
            result["created_at"] = self.created_at.isoformat()
        return result


@dataclass
class SpentEntry:
    category: str
    payment_method: str
    value: Decimal
    description: str
    entry_date: date
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        result = asdict(self)
        result["value"] = str(result["value"])
        result["entry_date"] = self.entry_date.isoformat()
        if self.created_at:
            result["created_at"] = self.created_at.isoformat()
        return result
