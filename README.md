# Expense Tracker CLI

A command-line based Expense Tracker built with Python.  
This application allows users to add, list, filter, summarize, and export expenses using a clean and modular CLI design.

The project uses JSON for persistent storage and supports advanced filtering, sorting, and summary statistics.

---

## Features

### Add Expenses
- Add expenses with date, category, amount, currency, and note
- Auto-generated unique expense IDs
- Input validation (date format, positive amount)

### List Expenses
- View expenses in table format (default)
- View expenses in CSV format (printed in terminal)
- Filter by:
  - Month (`--month YYYY-MM`)
  - Date range (`--from`, `--to`)
  - Category (`--category`)
  - Amount range (`--min`, `--max`)
- Sort by:
  - Date
  - Amount
  - Category
- Descending sort option
- Limit number of results

### Summary
- Total number of expenses
- Grand total
- Totals by category
- Optional advanced metrics:
  - Highest expense
  - Average expense per day
  - Category percentage share

### Other
- Environment variable support
- Logging of commands and errors
- Modular and maintainable project structure

---

## Project Structure

```
expense-tracker/
│
├── tracker/
│ ├── init.py
│ ├── main.py       # Entry point: python -m tracker
│ ├── cli.py        # CLI argument parsing and output
│ ├── service.py    # Business logic
│ ├── storage.py    # JSON read/write and CSV output
│ ├── models.py     # Expense data model
│ ├── utils.py      # Validation and helper functions
│ └── logger.py     # Logging configuration
│
├── data/
│ └── expenses.json # Auto-created data file
│
├── logs/
│ └── tracker.log   # Auto-created log file
│
├── .env            # Environment variables (not committed)
├── .gitignore
└── README.md
```

---

## Requirements

- Python **3.10+**
- `pip` package manager

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Ali-ahsan35/Expense_Tracker_A6.git

cd expense-tracker
```
### 2. Create and Activate Virtual Environment

```
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows
```
---
## Environment Variables
#### Create a .env file in the project root:
```
TRACKER_DEFAULT_CURRENCY=BDT
TRACKER_DATA_FILE=data/expenses.json
TRACKER_LOG_FILE=logs/tracker.log
```
---
## Running the Application
#### All commands are run using:
```
python -m tracker <command> [options]
```
---
## Commands and Usage
### Add an Expense
```
python -m tracker add --date 2026-01-26 --category food --amount 250.5 --note "Lunch"
```
#### If --date is not provided, today’s date is used.
----
## List Expenses (Default Table Output)
```
python -m tracker list
```
#### List with Filters
```
python -m tracker list --month 2026-01
python -m tracker list --category food
python -m tracker list --from 2026-01-20 --to 2026-01-30
python -m tracker list --min 100 --max 500
```
#### Sorting and Limiting
```
python -m tracker list --sort amount
python -m tracker list --sort amount --desc
python -m tracker list --limit 5
```
#### CSV Output (Printed in Terminal)
```
python -m tracker list --format csv
```
---
### Summary
```
python -m tracker summary
python -m tracker summary --month 2026-01
python -m tracker summary --category food
```
---
#### The summary includes:
- Total expenses

- Grand total

- Totals by category

- Highest expense

- Average per day

- Category percentage share
---
### Notes
- Data is stored in data/expenses.json and created automatically on first run

- CSV output is printed to the terminal (file export is not required)

- Logs are written to logs/tracker.log

- This project is designed for learning, clarity, and maintainability
---
## Author
#### Syed Ali Ahsan