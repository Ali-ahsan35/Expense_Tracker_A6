from datetime import datetime


def validate_date(date_str: str) -> str:
    """
    Validate date format YYYY-MM-DD.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("date must be YYYY-MM-DD")
    return date_str


def validate_amount(amount: float) -> float:
    """
    Validate amount > 0.
    """
    if amount <= 0:
        raise ValueError("amount must be > 0")
    return amount


def normalize_category(category: str) -> str:
    """
    Normalize category.
    """
    return category.strip().lower()

def filter_by_month(expenses: list[dict], month: str | None) -> list[dict]:
    """
    Filter expenses by month (YYYY-MM). If month is None, returns original list.
    """
    if not month:
        return expenses

    #must look like YYYY-MM
    if len(month) != 7 or month[4] != "-":
        raise ValueError("month must be YYYY-MM")

    return [e for e in expenses if e.get("date", "").startswith(month)]


def filter_by_date_range(
    expenses: list[dict],
    date_from: str | None,
    date_to: str | None,
) -> list[dict]:
    """
    Filter expenses by date range (YYYY-MM-DD).
    Inclusive: from <= date <= to
    """

    if not date_from and not date_to:
        return expenses

    # strings to date objects
    def parse(date_str: str):
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    try:
        from_date = parse(date_from) if date_from else None
        to_date = parse(date_to) if date_to else None
    except ValueError:
        raise ValueError("from/to date must be YYYY-MM-DD")

    filtered = []

    for e in expenses:
        expense_date = parse(e["date"])

        if from_date and expense_date < from_date:
            continue
        if to_date and expense_date > to_date:
            continue

        filtered.append(e)

    return filtered

def filter_by_category(expenses: list[dict], category: str | None) -> list[dict]:
    """
    Filter expenses by exact category match (case-insensitive).
    """
    if not category:
        return expenses

    category = category.strip().lower()
    return [e for e in expenses if e.get("category", "").lower() == category]

def filter_by_amount_range(
    expenses: list[dict],
    min_amount: float | None,
    max_amount: float | None,
) -> list[dict]:
    """
    Filter expenses by amount range (inclusive).
    """
    if min_amount is None and max_amount is None:
        return expenses

    if min_amount is not None and min_amount < 0:
        raise ValueError("min amount must be >= 0")

    if max_amount is not None and max_amount < 0:
        raise ValueError("max amount must be >= 0")

    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise ValueError("min amount cannot be greater than max amount")

    filtered = []
    for e in expenses:
        amount = float(e.get("amount", 0))

        if min_amount is not None and amount < min_amount:
            continue
        if max_amount is not None and amount > max_amount:
            continue

        filtered.append(e)

    return filtered


def sort_expenses(
    expenses: list[dict],
    sort_by: str | None,
    desc: bool = False,
) -> list[dict]:
    """
    Sort expenses by date, amount, or category.
    """
    if not sort_by:
        return expenses

    if sort_by == "date":
        return sorted(
            expenses,
            key=lambda e: datetime.strptime(e["date"], "%Y-%m-%d"),
            reverse=desc,
        )

    if sort_by == "amount":
        return sorted(
            expenses,
            key=lambda e: float(e["amount"]),
            reverse=desc,
        )

    if sort_by == "category":
        return sorted(
            expenses,
            key=lambda e: e["category"],
            reverse=desc,
        )

    raise ValueError("invalid sort option")
