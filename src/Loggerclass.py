##
## PERSONAL PROJECT, 2024
## my_honeypot
## File description:
## class
##

import logging
import os
from datetime import datetime


def create_unique_log(ip: str) -> str:
    date = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    if not os.path.exists("./logs/" + ip):
        os.makedirs("./logs/" + ip)
    filepath = "./logs/" + ip + "/"
    filename = f"honeypot_{date}.log"
    return filepath + filename


class Logger:
    def __init__(self, ip: str):
        self.file = create_unique_log(ip)
        self.logger = logging.getLogger(self.file)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler(self.file)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def __repr__(self) -> str:
        return f"Logger({self.file})"

    def get_file(self) -> str:
        return self.file

    def get_size_file(self) -> float:
        return os.path.getsize(self.file)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)
