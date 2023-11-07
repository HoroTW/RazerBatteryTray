import logging
import os

logging.getLogger("PIL").setLevel(logging.WARNING)  # Silence PIL logging

def configure_logger():
    log_level = os.environ.get("LOG_LEVEL", "WARNING").upper()

    logging.basicConfig(
        level=log_level, format="%(levelname)s %(message)s", handlers=[logging.StreamHandler()]
    )
    logger.debug("Logging configured with log level: " + log_level)

    RESET_COLOR, RED, GREEN, YELLOW, BLUE = "", "", "", "", ""  # default no colors

    if os.isatty(1) and os.isatty(2):  # if stdout,stderr are ttys we use colors
        logger.debug("stdout and stderr are terminals --> setting up colors")
        RESET_COLOR = "\033[0m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"

    class ColorCapableFormatter(logging.Formatter):
        def format(self, record):
            if record.levelno == logging.WARNING:
                record.msg = YELLOW + record.msg + RESET_COLOR
            elif record.levelno == logging.ERROR:
                record.msg = RED + record.msg + RESET_COLOR
            elif record.levelno == logging.INFO:
                record.msg = GREEN + record.msg + RESET_COLOR
            elif record.levelno == logging.DEBUG:
                record.msg = BLUE + record.msg + RESET_COLOR
            return super().format(record)

    color_formatter = ColorCapableFormatter("%(levelname)s %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)
    logger.handlers.clear()
    logger.addHandler(console_handler)
    logger.debug("Logger is now configured")


# Configure logger
logger = logging.getLogger()
configure_logger()