import os
import shutil
from pathlib import Path
import glob

from src.app.load_config import assign_environmental_to_variables as lc
from src.logs.log_config import log_error


def _parse_selected_inboxes(raw_value):
    if not raw_value:
        return set()
    return {item.strip() for item in str(raw_value).split(";") if item.strip()}

def run_move(mail_path, destination):
    try:
        if os.name == "nt":
            shutil.move(mail_path, str(destination))
        else:
            sp.run(["mv", mail_path, str(destination)], check=True)
        return True
    except Exception as exc:
        log_error("run_move", mail_path, destination, exc)
        return False
    
def start_move_sequence():
    FULL_MOVE = lc.FULL_MOVE
    USERS_INBOX_LOCATION = lc.USERS_INBOX_LOCATION
    MOVE_DUPES_TO_FOLDER = lc.MOVE_DUPES_TO_FOLDER

    if not MOVE_DUPES_TO_FOLDER:
        raise ValueError(f"{MOVE_DUPES_TO_FOLDER} must be set")

    target_root = Path(MOVE_DUPES_TO_FOLDER)
    target_root.mkdir(parents=True, exist_ok=True)

    inbox_paths = glob.glob(os.path.join(USERS_INBOX_LOCATION, "*.txt"))
    if FULL_MOVE == "FALSE":
        selected_inboxes = _parse_selected_inboxes(lc.SELECTED_INBOXES_TO_MOVE)
        inbox_paths = [path for path in inbox_paths if Path(path).stem in selected_inboxes]
    elif FULL_MOVE != "TRUE":
        return

    total_moved = 0
    for inbox_path in inbox_paths:
        inbox_name = Path(inbox_path).stem
        inbox_target = target_root / inbox_name
        inbox_target.mkdir(parents=True, exist_ok=True)

        with open(inbox_path, "r") as inbox_file:
            mail_paths = [line.strip() for line in inbox_file if line.strip()]

        moved_count = 0
        for mail in mail_paths:
            if run_move(mail, inbox_target):
                moved_count += 1

        total_moved += moved_count
        print(f"{moved_count} mails moved from {inbox_name} to {inbox_target}")

    print(f"Total mails moved: {total_moved}")