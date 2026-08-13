import datetime as dt
from pathlib import Path

import logging as log

from src.app.load_config import assign_environmental_to_variables as lc

BASE_DIR = Path(__file__).resolve().parent

LOG_LOCATION = lc.LOG_LOCATION
LOG_LEVEL = lc.LOG_LEVEL
if LOG_LEVEL == "INFO":
    LOG_LEVEL = log.INFO
elif LOG_LEVEL == "ERROR":
    LOG_LEVEL = log.ERROR

log.basicConfig(
    filename=Path(LOG_LOCATION, f"{dt.datetime.now()}_log.txt"),
    filemode='a',
    level=LOG_LEVEL,
    force=True,
)

def log_info(*message) -> None:
    log.info(20*'-')
    log.info(message)
    log.info(20*'-')

def log_error(*message) -> None:
    log.error(20*'-')
    log.error(message)
    log.error(20*'-')