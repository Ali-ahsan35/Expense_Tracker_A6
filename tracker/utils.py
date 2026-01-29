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

