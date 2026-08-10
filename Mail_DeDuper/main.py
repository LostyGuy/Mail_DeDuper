from pathlib import Path

from src.mail_deduper.app.load_config import load_environmental_values
from src.mail_deduper.app.gather_emails import get_shared_email, get_users_inboxes, get_users_emails
from src.mail_deduper.app.find_duplicates import find_dupes
from src.mail_deduper.app.move_duplicates import start_move_sequence
from Mail_DeDuper.src.mail_deduper.app.load_config import assign_environmental_to_variables as lc
from src.mail_deduper.logs import log_error

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve()
    
    #TODO---- If crucial files are present ----
    
    load_environmental_values()
    
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
    