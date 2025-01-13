import logging
import os


def setup_logger(logger_file: str, log_dir: str = 'Logs', level=logging.INFO, 
                 format='%(asctime)s - %(levelname)s - %(message)s') -> logging.Logger:
    
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(logger_file)
    
    if not logger.hasHandlers():
        file_handler = logging.FileHandler(os.path.join(log_dir, f"{logger_file}.log"))
        file_handler.setLevel(level)

        formatter = logging.Formatter(format)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.setLevel(level)

    return logger



