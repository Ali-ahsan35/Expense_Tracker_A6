import os
from dotenv import load_dotenv

from tracker.logger import setup_logger
from tracker.cli import run


def main():
    load_dotenv()

    # Setup logging
    logger = setup_logger()
    logger.info("Expense Tracker started")

    run()


if __name__ == "__main__":
    main()
