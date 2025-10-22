import logging
from datetime import datetime

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def log_error(self, error_message):
        """Log error message"""
        self.logger.error(f"[{datetime.now().isoformat()}] {error_message}")
    
    def log_warning(self, warning_message):
        """Log warning message"""
        self.logger.warning(f"[{datetime.now().isoformat()}] {warning_message}")
    
    def log_info(self, info_message):
        """Log info message"""
        self.logger.info(f"[{datetime.now().isoformat()}] {info_message}")
