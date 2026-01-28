from dataclasses import dataclass, asdict


@dataclass
class Expense:
    id: str
    date: str
    category: str
    amount: float
    currency: str
    note: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)
