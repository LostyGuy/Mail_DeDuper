import datetime as dt
from pathlib import Path

import logging as log

BASE_DIR = Path(__file__).resolve().parent

log.basicConfig(
    filename=Path(BASE_DIR, "Mail_DeDuper", "src", "mail_deduper", "logs", f"{dt.datetime.now()}_log.txt"),
    filemode='a',
    level=log.INFO,
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