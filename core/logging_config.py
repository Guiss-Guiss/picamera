from config.configuration import CONFIG
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def configure_logging():
    """Logging system configuration with file and console handlers."""
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s'
    )

    file_handler = RotatingFileHandler(
        os.path.join(CONFIG['LOGS_FOLDER'], 'app_camera.log'),
        maxBytes=CONFIG['MAX_LOG_SIZE'],
        backupCount=CONFIG['NUM_BACKUP_LOGS']
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    error_handler = RotatingFileHandler(
        os.path.join(CONFIG['LOGS_FOLDER'], 'errors.log'),
        maxBytes=CONFIG['MAX_LOG_SIZE'],
        backupCount=CONFIG['NUM_BACKUP_LOGS']
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    for handler in [file_handler, console_handler, error_handler]:
        root_logger.addHandler(handler)
