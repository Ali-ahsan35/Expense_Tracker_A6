import logging
import os


def setup_logger():
    """
    Configure and return a logger instance.
    """

    # Read log file path from environment variable
    log_file = os.getenv("TRACKER_LOG_FILE", "logs/tracker.log")

    # Create logs folder if it does not exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Create logger
    logger = logging.getLogger("expense_tracker")
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs
    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
