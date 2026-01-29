from datetime import datetime, date as dt_date

from tracker.models import Expense
from tracker.storage import load_expenses, save_expenses



def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _generate_id(expense_date: str, existing: list[dict]) -> str:
    """
    ID format: EXP-YYYYMMDD-0001
    Uses the last stored expense to generate next ID.
    """
    yyyymmdd = expense_date.replace("-", "")
    prefix = f"EXP-{yyyymmdd}-"

    if not existing:
        return f"{prefix}0001"

    last_id = existing[-1].get("id", "")

    try:
        # last_date_part = last_id.split("-")[1]
        last_number_part = last_id.split("-")[2]

        
        next_num = int(last_number_part) + 1

    except (IndexError, ValueError):
        # fallback if ID format is broken
        next_num = 1

    return f"{prefix}{next_num:04d}"


def add_expense(data_file: str, date: str, category: str, amount: float, currency: str, note: str) -> Expense:
    """
    Creates an Expense and stores it in JSON.
    """
    expenses = load_expenses(data_file)

    expense_id = _generate_id(date, expenses)
    created_at = _now_iso()

    expense = Expense(
        id=expense_id,
        date=date,
        category=category,
        amount=amount,
        currency=currency,
        note=note,
        created_at=created_at,
    )

    expenses.append(expense.to_dict())
    save_expenses(data_file, expenses)

    return expense

def list_expenses(data_file: str) -> list[dict]:
    """
    Returns all expenses from the JSON file.
    """
    return load_expenses(data_file)

def summary_expenses(data_file: str) -> dict:
    """
    Returns summary of count, grand_total, totals_by_category
    """
    expenses = load_expenses(data_file)

    totals_by_category: dict[str, float] = {}
    grand_total = 0.0

    for e in expenses:
        amount = float(e["amount"])
        category = e["category"]

        grand_total += amount
        totals_by_category[category] = totals_by_category.get(category, 0.0) + amount

    return {
        "count": len(expenses),
        "grand_total": grand_total,
        "totals_by_category": totals_by_category,
    }
