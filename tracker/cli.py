import argparse


def build_parser() -> argparse.ArgumentParser:
    """
    Creates and returns the main argument parser with subcommands:
    add, list, summary
    """
    parser = argparse.ArgumentParser(
        prog="tracker",
        description="Expense Tracker CLI"
    )

    # subcommands: add, list, summary
    subparsers = parser.add_subparsers(dest="command", required=True)


    # add command
    add_parser = subparsers.add_parser("add", help="Add an expense")

    add_parser.add_argument("--date", help="Expense date (YYYY-MM-DD). Default: today")
    add_parser.add_argument("--category", required=True, help="Expense category (e.g., food)")
    add_parser.add_argument("--amount", required=True, type=float, help="Expense amount (must be > 0)")
    add_parser.add_argument("--note", default="", help="Optional note")
    add_parser.add_argument("--currency", default="BDT", help="Currency (default: BDT)")


    # list command
    list_parser = subparsers.add_parser("list", help="List expenses")

    list_parser.add_argument("--month", help="Filter by month (YYYY-MM)")
    list_parser.add_argument("--from", dest="date_from", help="From date (YYYY-MM-DD)")
    list_parser.add_argument("--to", dest="date_to", help="To date (YYYY-MM-DD)")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--min", dest="min_amount", type=float, help="Minimum amount")
    list_parser.add_argument("--max", dest="max_amount", type=float, help="Maximum amount")
    list_parser.add_argument("--sort", choices=["date", "amount", "category"], default="date",
                             help="Sort by (default: date)")
    list_parser.add_argument("--desc", action="store_true", help="Sort descending")
    list_parser.add_argument("--limit", type=int, help="Limit number of results")
    list_parser.add_argument("--format", choices=["table", "csv"], default="table",
                             help="Output format (default: table)")


    # summary command
    summary_parser = subparsers.add_parser("summary", help="Show totals and breakdown")

    summary_parser.add_argument("--month", help="Filter by month (YYYY-MM)")
    summary_parser.add_argument("--from", dest="date_from", help="From date (YYYY-MM-DD)")
    summary_parser.add_argument("--to", dest="date_to", help="To date (YYYY-MM-DD)")
    summary_parser.add_argument("--category", help="Filter by category")

    return parser


def run():
    """
    Parses command line arguments and runs the correct command.
    """
    parser = build_parser()
    args = parser.parse_args()

    # For now: just print what argparse captured (learning step)
    if args.command == "add":
        print("ADD command received")
        print(f"date     : {args.date}")
        print(f"category : {args.category}")
        print(f"amount   : {args.amount}")
        print(f"currency : {args.currency}")
        print(f"note     : {args.note}")

    elif args.command == "list":
        print("LIST command received")
        print(args)

    elif args.command == "summary":
        print("SUMMARY command received")
        print(args)
