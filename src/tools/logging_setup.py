import logging


def logging_setup(logger_name):
    """
    Set up logging configuration for the application.
    This function configures a logger that writes DEBUG and above logs to a file,
    and INFO logs to the console.
    """
    # Create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Create a FileHandler to write all logs (DEBUG and above) to a file
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)

    # Create a StreamHandler to print INFO (and above) to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Custom filter to only allow INFO level logs in the console
    class InfoOnlyFilter(logging.Filter):
        def filter(self, record):
            return record.levelno == logging.INFO

    console_handler.addFilter(InfoOnlyFilter())

    # Create formatters and add them to the handlers
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    console_formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
