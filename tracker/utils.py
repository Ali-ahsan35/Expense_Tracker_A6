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
