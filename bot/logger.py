import logging
import os

class Logger:
    def __init__(self, path: str, filename: str):
        self.logger = None
        self.path = path
        self.filename = filename
    
    
    def init_logger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        
        file_handler = logging.FileHandler(filename=f"{self.path}/logs/{self.filename}.log", encoding="utf-8", mode="w")
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter("[%(asctime)s] (%(levelname)s) %(name)s: %(message)s")

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        
    def log(self, msg: str, level: int):
        self.logger.log(level, msg)