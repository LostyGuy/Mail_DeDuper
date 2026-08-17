from pathlib import Path

from src.app.load_config import assign_environmental_to_variables
from src.app.gather_emails import get_shared_email, get_users_inboxes, get_users_emails
from src.app.find_duplicates import find_dupes
from src.app.move_duplicates import start_move_sequence
from src.connection.connection import database_initialization

if __name__ == "__main__":
      
    config = assign_environmental_to_variables()
    
    from src.logs.log_config import logger_initialization
    logger_initialization()
    from src.logs.log_config import log_error
    database_initialization()
    
    get_shared_email()
    get_users_inboxes()
    get_users_emails()
        
    find_dupes()
    
    if config.REMOVE_MODE == "TRUE":
        raise NotImplementedError
    elif config.MOVE_MODE == "TRUE":
        start_move_sequence()
    elif config.MOVE_MODE == "FALSE" or config.REMOVE_MODE == "FALSE":
        pass
    else:
        log_error("main.py: ", "Invalid Value Has Been Passed. \n", f"REMOVE_MODE: {config.REMOVE_MODE} \n", f"MOVE_MODE: {config.MOVE_MODE} \n")
        raise ValueError("Invalid Value Has Been Passed")
    