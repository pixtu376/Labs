import logging
from datetime import datetime

class AppLogger:
    def __init__(self, log_file='app.log'):
        self.log_file = log_file
        self._setup_logging()
        
    def _setup_logging(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        
    def log_info(self, message):
        logging.info(message)
        print(f"[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
        
    def log_error(self, message):
        logging.error(message)
        print(f"[ERROR] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
        
    def log_operation(self, operation, obj=None):
        msg = f"Операция: {operation}"
        if obj:
            msg += f" | Объект: {type(obj).__name__} {obj.name if hasattr(obj, 'name') else ''}"
        self.log_info(msg)

logger = AppLogger()
