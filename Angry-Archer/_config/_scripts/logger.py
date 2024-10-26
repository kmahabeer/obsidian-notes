import os
from datetime import datetime


class Logger:
    def __init__(self, log_file=None) -> None:
        if log_file is None:
            log_file = "logs/default.log"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.log_file = log_file

    def _write_log(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        with open(self.log_file, "a") as f:
            f.write(log_entry)
        # print(log_entry.strio())

    def debug(self, message):
        self._write_log("DEBUG", message)

    def info(self, message):
        self._write_log("INFO", message)

    def warning(self, message):
        self._write_log("WARNING", message)

    def error(self, message):
        self._write_log("ERROR", message)

    def critical(self, message):
        self._write_log("CRITICAL", message)
