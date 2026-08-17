import datetime as dt
from pathlib import Path

import logging as log

from src.app.load_config import assign_environmental_to_variables


config = assign_environmental_to_variables()

def logger_initialization():
    LOG_LEVEL = config.LOG_LEVEL
    if LOG_LEVEL == "INFO":
        LOG_LEVEL = log.INFO
    elif LOG_LEVEL == "ERROR":
        LOG_LEVEL = log.ERROR

    log.basicConfig(
        filename=Path("runtime_logs", f"{dt.datetime.now()}_log.txt"),
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