import os

# Define base path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Global configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'static', 'media')
MAX_CONTENT_SIZE = 16 * 1024 * 1024  # 16 MB
LOGS_FOLDER = os.path.join(BASE_DIR, '..', 'logs')
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
NUM_BACKUP_LOGS = 5  # Number of backup files

CONFIG = {
    'UPLOAD_FOLDER': UPLOAD_FOLDER,
    'MAX_CONTENT_SIZE': MAX_CONTENT_SIZE,
    'LOGS_FOLDER': LOGS_FOLDER,
    'MAX_LOG_SIZE': MAX_LOG_SIZE,
    'NUM_BACKUP_LOGS': NUM_BACKUP_LOGS
}

# Explicit export
__all__ = ['UPLOAD_FOLDER', 'MAX_CONTENT_SIZE', 'LOGS_FOLDER', 'MAX_LOG_SIZE', 'NUM_BACKUP_LOGS', 'CONFIG']
