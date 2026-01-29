from datetime import datetime,date
from tracker.models import Expense
import calendar
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

    # label
    label = month if month else "all"

    totals_by_category: dict[str, float] = {}
    grand_total = 0.0
    currencies = set()

    # bonus: highest expense
    highest_expense = None  # will store a dict expense

    for e in expenses:
        amount = float(e["amount"])
        cat = e["category"]
        cur = e.get("currency", "BDT")

        currencies.add(cur)
        grand_total += amount
        totals_by_category[cat] = totals_by_category.get(cat, 0.0) + amount

        if highest_expense is None or amount > float(highest_expense["amount"]):
            highest_expense = e

    currency_display = currencies.pop() if len(currencies) == 1 else "BDT"

    # bonus: average per day in month (only meaningful if month is provided)
    avg_per_day = None
    days_in_month = None
    try:
        if month:
            # use provided month
            y, m = map(int, month.split("-"))
        else:
            today = date.today()
            y, m = today.year, today.month

        days_in_month = calendar.monthrange(y, m)[1]
        avg_per_day = (grand_total / days_in_month) if days_in_month else 0.0

    except ValueError:
        avg_per_day = None
        days_in_month = None

    #category percentage share
    category_percent: dict[str, float] = {}
    if grand_total > 0:
        for cat, total in totals_by_category.items():
            category_percent[cat] = (total / grand_total) * 100

    return {
        "count": len(expenses),
        "grand_total": grand_total,
        "totals_by_category": totals_by_category,
        "currency": currency_display,
        "label": label,
        "highest_expense": highest_expense,
        "avg_per_day": avg_per_day,
        "days_in_month": days_in_month,
        "category_percent": category_percent,
    }

