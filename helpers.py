import os
import logging
from functools import wraps


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file = os.path.join(os.path.dirname(__file__), 'processing.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def exceptions_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'{e = }')
    return wrapper
