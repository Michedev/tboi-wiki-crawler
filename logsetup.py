import logging
import sys
from pathlib import Path


logpath = Path(__file__).parent / 'driver.log'
file_handler = logging.FileHandler(logpath)
console_handler = logging.StreamHandler(sys.stdout)
format = '%(asctime)s - %(levelname)s : %(message)s'

def config_log():
    logging.basicConfig(handlers=[file_handler, console_handler], format=format, level=logging.INFO)