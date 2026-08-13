import subprocess as sp
import os
import shutil
import datetime as dt
import re
from pathlib import Path

from src.connection import connection as conn
from sqlalchemy import Select, Insert
import sqlite3

from src.app.load_config import assign_environmental_to_variables as lc
from src.logs.log_config import log_error
from src.connection import models
from src.app.paths import BASE_DIR 


DOMAIN_PATH = lc.DOMAIN_LOCATION
SHARED_INBOX_LOCATION = lc.SHARED_INBOX_LOCATION
MARK_OLDER_THAN = lc.MARK_OLDER_THAN
WAS_ENTIRE_SHARED_FOLDER_SCANNED = lc.WAS_ENTIRE_SHARED_FOLDER_SCANNED

USERS_INBOX_LOCATION = Path(BASE_DIR, "lists_of", "lists_of_duped_mails")
LIST_OF_INBOXES_PATH = Path(BASE_DIR, "lists_of", "list_of_inboxes.txt")
LIST_OF_SHARED_EMAILS = Path(BASE_DIR, "lists_of", "list_of_shared_emails.txt")

def get_users_inboxes() -> None:
    '''
    Creates list of inboxes in domain where directory name matches pattern: [a-z].*
    OR
    If the file exists it truncates it's content
    '''

    if os.path.exists(LIST_OF_INBOXES_PATH):
        open(LIST_OF_INBOXES_PATH, "w").close()
        
    sp.run(
        f"ls -d {DOMAIN_PATH}/?.* > {LIST_OF_INBOXES_PATH}", 
        shell=True
    )
    
def get_users_emails() -> None:
    '''
    Create one file for each mailbox with mails that are in `inbox` directory
    OR
    If the file exists it truncates it's content
    '''

    if os.path.exists(USERS_INBOX_LOCATION):
        shutil.rmtree(USERS_INBOX_LOCATION)
    os.mkdir(USERS_INBOX_LOCATION)
        
    with open(LIST_OF_INBOXES_PATH) as user_inbox:
        for inbox in user_inbox:
            inbox = inbox.strip()
            user = inbox[28:].replace(".", "_")
            sp.run(
                f"find {inbox} -path '*/inbox/*.imap' > {USERS_INBOX_LOCATION}/{user}.txt", 
                shell=True
            )

#TODO
def get_shared_email() -> None:
    '''
    Creates a sqlite file that contains every mail from shared directory
    '''
    
    if WAS_ENTIRE_SHARED_FOLDER_SCANNED == "FALSE":
        sp.run(
                f"find {SHARED_INBOX_LOCATION} -path '*/[0-9][0-9]_*/*.imap' > {LIST_OF_SHARED_EMAILS}",
                shell=True
            )
        
    elif WAS_ENTIRE_SHARED_FOLDER_SCANNED == "TRUE":
        sp.run(
                f"find {SHARED_INBOX_LOCATION} -path '*/[0-9][0-9]_*/*.imap' -mtime +{lc.SCAN_XYZ_DAYS_BACK} > {LIST_OF_SHARED_EMAILS}",
                shell=True
            )
        #TODO ---- Set Environmental Value to 'TRUE' ----
        
    else:
        log_error("gather_emails.py: ", "Invalid Value Has Been Passed. \n", f"WAS_ENTIRE_SHARED_FOLDER_SCANNED: {lc.WAS_ENTIRE_SHARED_FOLDER_SCANNED} \n")
        raise ValueError("Invalid Value Has Been Passed")
    
    with open(LIST_OF_SHARED_EMAILS) as shared_emails:
                for line in shared_emails:
                    date_match = re.search(r"(\d{4})(\d{2})(\d{2})\d*\.imap$", line)
                    if not date_match:
                        return None
                    
                    year, month, day = date_match.groups()
                    try:
                        mail_date = dt.datetime(int(year), int(month), int(day))
                    except ValueError:
                        return None
                    try:
                        with conn.get_db() as db:
                            db.add(
                                models.shared_emails(
                                    absolute_path = line,
                                    date_of_mail = mail_date,
                                )
                            )
                            db.commit()
                    except sqlite3.IntegrityError as error:
                        if error.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                            pass
                        else:
                            log_error("get_shared_email: ", error, " | ", error.sqlite_errorcode)
    # if os.path.exists(LIST_OF_SHARED_EMAILS):
    #     open(LIST_OF_SHARED_EMAILS, "w").close()
    
def extract_message_id(filepath: str) -> str | None:

    date_match = re.search(r"(\d{4})(\d{2})(\d{2})\d*\.imap$", filepath)
    if not date_match:
        return None
 
    year, month, day = date_match.groups()
    try:
        mail_date = dt.datetime(int(year), int(month), int(day))
    except ValueError:
        return None
 
    cutoff_date = dt.datetime.now() - dt.timedelta(days=int(MARK_OLDER_THAN))
    if mail_date > cutoff_date:
        return None
    
    try:
        with open(filepath, errors="ignore") as f:
            capturing = False
            header_value = ""

            for line in f:
                if line.strip() == "":
                    break

                if line.lower().startswith("message-id:"):
                    capturing = True
                    header_value = line
                    continue
                if capturing:
                    if line[0] in (" ", "\t"):
                        header_value += line
                    else:
                        break

            match = re.search(r"<(.+?)>", header_value, re.DOTALL)
            return match.group(1) if match else None
    except FileNotFoundError:
        return None
    