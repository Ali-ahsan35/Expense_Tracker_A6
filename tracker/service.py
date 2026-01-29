from datetime import datetime, date as dt_date
from tracker.models import Expense
from tracker.storage import load_expenses, save_expenses
from tracker.utils import (
    filter_by_month,
    filter_by_date_range,
    filter_by_category,
    filter_by_amount_range,
    sort_expenses,
    apply_limit,
)


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _generate_id(expense_date: str, existing: list[dict]) -> str:
    """
    ID format: EXP-YYYYMMDD-XXXX
    Sequence is GLOBAL and always increments.
    """
    yyyymmdd = expense_date.replace("-", "")
    prefix = f"EXP-{yyyymmdd}-"

    max_number = 0

    for e in existing:
        eid = e.get("id", "")
        try:
            # EXP-YYYYMMDD-0007 → take last part
            number_part = int(eid.split("-")[-1])
            if number_part > max_number:
                max_number = number_part
        except (IndexError, ValueError):
            continue

    next_num = max_number + 1
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

def list_expenses(
    data_file: str,
    month=None,
    date_from=None,
    date_to=None,
    category=None,
    min_amount=None,
    max_amount=None,
    sort_by=None,
    desc=False,
    limit=None,
) -> list[dict]:


    expenses = load_expenses(data_file)
    expenses = filter_by_month(expenses, month)
    expenses = filter_by_date_range(expenses, date_from, date_to)
    expenses = filter_by_category(expenses, category)
    expenses = filter_by_amount_range(expenses, min_amount, max_amount)
    expenses = sort_expenses(expenses, sort_by, desc)
    expenses = apply_limit(expenses, limit)

    return expenses



def summary_expenses(
    data_file: str,
    month: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
     category: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
) -> dict:
    expenses = load_expenses(data_file)

    expenses = filter_by_month(expenses, month)
    expenses = filter_by_date_range(expenses, date_from, date_to)
    expenses = filter_by_category(expenses, category)
    expenses = filter_by_amount_range(expenses, min_amount, max_amount)

    # label = month if month else "custom range"
    if month:
        label = month
    elif date_from or date_to:
        label = f"{date_from or '...'} to {date_to or '...'}"
    else:
        label = "all"


    totals_by_category: dict[str, float] = {}
    grand_total = 0.0
    currencies = set()

    for e in expenses:
        amount = float(e["amount"])
        category = e["category"]
        currency = e.get("currency", "BDT")

        currencies.add(currency)
        grand_total += amount
        totals_by_category[category] = totals_by_category.get(category, 0.0) + amount

    currency_display = currencies.pop() if len(currencies) == 1 else "BDT"

    return {
        "count": len(expenses),
        "grand_total": grand_total,
        "totals_by_category": totals_by_category,
        "currency": currency_display,
        "label": label,
    }

