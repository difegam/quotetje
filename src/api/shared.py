import logging
import logging.config
import logging.handlers
import os
import sys

from dotenv import load_dotenv

# from pathlib import Path

load_dotenv()

# API Information
API_VERSION = str(os.getenv('API_VERSION'))
API_VERSION_NUMBER = str(os.getenv('API_VERSION_NUMBER'))
DB_CONNECTION_STRING = str(os.getenv('DB_CONNECTION_STRING'))

#  LOGGING CONFIGURATION
formats = {
    'verbose': "[%(asctime)s | %(levelname)s] %(module)-2s : %(funcName)-2s : %(message)s",
    'default': "%(asctime)4s | %(message)s"
}
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format=formats.get("default", "%(asctime)s : %(message)s"),
                    datefmt="%Y-%m-%d %H:%M:%S")

# # -- filename
# Path(r'./logs').mkdir(parents=True, exist_ok=True)
# log_file = r"./logs/app-logger.log"
# logging.handlers.TimedRotatingFileHandler(filename=log_file, when="midnight", backupCount=3)

logger = logging.getLogger("quotes")
