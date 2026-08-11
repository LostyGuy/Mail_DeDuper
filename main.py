from pathlib import Path

from src.app.load_config import load_environmental_values
from src.app.gather_emails import get_shared_email, get_users_inboxes, get_users_emails
from src.app.find_duplicates import find_dupes
from src.app.move_duplicates import start_move_sequence
from src.logs import log_error

if __name__ == "__main__":
    
    #TODO---- If crucial files are present ----
    
    load_environmental_values()
    from src.app.load_config import assign_environmental_to_variables as lc
    
    get_shared_email()
    get_users_inboxes()
    get_users_emails()
    
    find_dupes()
    
    if lc.REMOVE_MODE == "TRUE":
        raise NotImplementedError
    elif lc.MOVE_MODE == "TRUE":
        start_move_sequence()
    else:
        log_error("main.py: ", "Invalid Value Has Been Passed. \n", f"REMOVE_MODE: {lc.REMOVE_MODE} \n", f"MOVE_MODE: {lc.MOVE_MODE} \n")
        raise ValueError("Invalid Value Has Been Passed")
    