from pathlib import Path
import os
import datetime as dt

import dotenv as de

BASE_DIR = Path(__file__).resolve().parents[3]


def _get_environmental_values(variable: str):
    return os.getenv(variable.upper(), "").upper()

def load_environmental_values() -> None :
    
    try:
        de.load_dotenv(dotenv_path=BASE_DIR / "src" / "config" / "find_config.env")
        de.load_dotenv(dotenv_path=BASE_DIR / "src" / "config" / "move_config.env")
        de.load_dotenv(dotenv_path=BASE_DIR / "src" / "config" / "remove_config.env")
        de.load_dotenv(dotenv_path=BASE_DIR / "src" / "config" / "main_config.env")
        de.load_dotenv(dotenv_path=BASE_DIR / "src" / "config" / "log_config.env")
    except Exception as e:
        print(e)
    
def load_excluded_users_from_deduplication() -> set[str]:
    '''Loads usernames that should be skipped during deduplication'''
    
    EXCLUDE_FROM_DEDUPLICATION_PATH = Path(BASE_DIR, "lists_of", "list_of_excluded_users_from_deduplication.txt")
    
    excluded = set()
    with open(EXCLUDE_FROM_DEDUPLICATION_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            excluded.add(line.replace(".", "_"))
    return excluded

def load_excluded_users_from_moving() -> set[str]:
    '''Loads usernames that should be skipped during moving'''
    
    EXCLUDE_FROM_MOVING_PATH = Path(BASE_DIR, "lists_of", "list_of_excluded_users_from_moving.txt")
        
    excluded = set()
    with open(EXCLUDE_FROM_MOVING_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            excluded.add(line.replace(".", "_"))
    return excluded

def load_excluded_users_from_removing() -> set[str]:
    '''Loads usernames that should be skipped during removing'''
    
    EXCLUDE_FROM_REMOVING_PATH = Path(BASE_DIR, "lists_of", "list_of_excluded_users_from_removing.txt")
        
    excluded = set()
    with open(EXCLUDE_FROM_REMOVING_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            excluded.add(line.replace(".", "_"))
    return excluded
    
class assign_environmental_to_variables():
    
    #---- master_config.env ----
    WAS_ENTIRE_SHARED_FOLDER_SCANNED = _get_environmental_values("WAS_ENTIRE_SHARED_FOLDER_SCANNED").upper()
    SCAN_XYZ_DAYS_BACK = _get_environmental_values("SCAN_XYZ_DAYS_BACK")
    
    #---- find_config.env ----
    SHARED_INBOX_LOCATION = _get_environmental_values("SHARED_INBOX_LOCATION")
    USERS_INBOX_LOCATION = _get_environmental_values("USERS_INBOX_LOCATION")
    DOMAIN_LOCATION = _get_environmental_values("DOMAIN_LOCATION")
    FULL_SCAN = _get_environmental_values("FULL_SCAN").upper()
    SCAN_USER = _get_environmental_values("SCAN_USER").lower()
    MARK_OLDER_THAN = int(_get_environmental_values("MARK_OLDER_THAN"))
    
    #---- move_config.env ----
    MOVE_MODE = _get_environmental_values("MOVE_MODE").upper()
    FULL_MOVE = _get_environmental_values("FULL_MOVE").upper()
    SELECTED_INBOXES_TO_MOVE = _get_environmental_values("SELECTED_INBOXES_TO_MOVE").lower()
    MOVE_DUPES_TO_FOLDER = _get_environmental_values("MOVE_DUPES_TO_FOLDER").lower()
    
    #---- remove_config.env ----
    REMOVE_MODE = _get_environmental_values("REMOVE_MODE").upper()
    FULL_REMOVE = _get_environmental_values("FULL_REMOVE").upper()
    SELECTED_INBOXES_TO_REMOVE = _get_environmental_values("SELECTED_INBOXES_TO_REMOVE").lower()
    
    #---- log_config.env ----
    LOG_LEVEL = _get_environmental_values("LOG_LEVEL").upper()
    LOG_LOCATION = _get_environmental_values("LOG_LOCATION")
    
class global_constants():
    
    TIMESTAMP = dt.datetime.now()