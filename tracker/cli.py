import argparse
import os
from datetime import date as dt_date

from tracker.service import add_expense
from tracker.utils import validate_date, validate_amount, normalize_category


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tracker", description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Default currency from env
    default_currency = os.getenv("TRACKER_DEFAULT_CURRENCY", "BDT")

    # add
    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("--date", help="Expense date (YYYY-MM-DD). Default: today")
    add_parser.add_argument("--category", required=True, help="Expense category (e.g., food)")
    add_parser.add_argument("--amount", required=True, type=float, help="Expense amount (must be > 0)")
    add_parser.add_argument("--note", default="", help="Optional note")
    add_parser.add_argument("--currency", default=default_currency, help=f"Currency (default: {default_currency})")

    # list 
    list_parser = subparsers.add_parser("list", help="List expenses")
    list_parser.add_argument("--month", help="Filter by month (YYYY-MM)")
    list_parser.add_argument("--from", dest="date_from", help="From date (YYYY-MM-DD)")
    list_parser.add_argument("--to", dest="date_to", help="To date (YYYY-MM-DD)")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--min", dest="min_amount", type=float, help="Minimum amount")
    list_parser.add_argument("--max", dest="max_amount", type=float, help="Maximum amount")
    list_parser.add_argument("--sort", choices=["date", "amount", "category"], default="date")
    list_parser.add_argument("--desc", action="store_true")
    list_parser.add_argument("--limit", type=int)
    list_parser.add_argument("--format", choices=["table", "csv"], default="table")

    # summary 
    summary_parser = subparsers.add_parser("summary", help="Show totals and breakdown")
    summary_parser.add_argument("--month", help="Filter by month (YYYY-MM)")
    summary_parser.add_argument("--from", dest="date_from", help="From date (YYYY-MM-DD)")
    summary_parser.add_argument("--to", dest="date_to", help="To date (YYYY-MM-DD)")
    summary_parser.add_argument("--category", help="Filter by category")

    return parser


def run(logger):
    """
    Parse args and route to the correct command.
    logger is passed from __main__.py
    """
    parser = build_parser()
    args = parser.parse_args()

    data_file = os.getenv("TRACKER_DATA_FILE", "data/expenses.json")

    try:
        if args.command == "add":
            # default date (today) if missing
            expense_date = args.date if args.date else dt_date.today().isoformat()

            # validatation
            expense_date = validate_date(expense_date)
            amount = validate_amount(args.amount)
            category = normalize_category(args.category)

            # call service
            expense = add_expense(
                data_file=data_file,
                date=expense_date,
                category=category,
                amount=amount,
                currency=args.currency,
                note=args.note,
            )

            print(
                f"Added: {expense.id} | {expense.date} | {expense.category} | "
                f"{expense.amount:.2f} {expense.currency} | {expense.note}"
            )

            logger.info(f"add command success: {expense.id}")

        elif args.command == "list":
            logger.info("list command called")

            from tracker.service import list_expenses  # import here to keep focus
            expenses = list_expenses(data_file)

            if not expenses:
                print("No expenses found")
                return

            # Print header
            print("ID | Date | Category | Amount | Note")
            print("-" * 70)

            # Print each expense
            for e in expenses:
                print(
                    f"{e['id']} | {e['date']} | {e['category']} | "
                    f"{e['amount']:.2f} {e['currency']} | {e['note']}"
                )

        elif args.command == "summary":
            print("Summary command not implemented yet (next step).")
            logger.info("summary command called")

    except ValueError as e:
        print(f"Error: {e}")
        logger.warning(f"validation/runtime error: {e}")
