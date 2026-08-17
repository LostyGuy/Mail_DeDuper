import subprocess as sp
import os
import shutil
import datetime as dt
import re
from pathlib import Path
import pathlib
import glob

from src.connection import connection as conn
from sqlalchemy import Select, Insert, text
from sqlalchemy.exc import IntegrityError
import sqlite3

from src.app.load_config import assign_environmental_to_variables
from src.logs.log_config import log_error
from src.connection import models
from src.app.paths import BASE_DIR 

config = assign_environmental_to_variables()

DOMAIN_PATH = config.DOMAIN_LOCATION
SHARED_INBOX_LOCATION = config.SHARED_INBOX_LOCATION
MARK_OLDER_THAN = config.MARK_OLDER_THAN
# WAS_ENTIRE_SHARED_FOLDER_SCANNED = config.WAS_ENTIRE_SHARED_FOLDER_SCANNED

# USERS_INBOX_LOCATION = Path(BASE_DIR, "lists_of", "lists_of_duped_mails")
# LIST_OF_INBOXES_PATH = Path(BASE_DIR, "lists_of", "list_of_inboxes.txt")
# LIST_OF_SHARED_EMAILS = Path(BASE_DIR, "lists_of", "list_of_shared_emails.txt")

def get_users_inboxes() -> None:
    '''
    Creates insert query of inboxes in domain where directory name matches pattern: [a-z].*
    '''
    
    #TODO -- Insert inbox with unique constrain --
    user_inboxes = Path(DOMAIN_PATH).glob('?.*')
    
    for inbox in user_inboxes:
        new_inbox = models.user_inboxes(
            inbox_name = inbox.name
        )
        try:
            with conn.get_db() as db:
                db.add(new_inbox)
                db.commit()
        except IntegrityError as error:
            original_error = error.orig

            if (
                isinstance(original_error, sqlite3.IntegrityError)
                and original_error.sqlite_errorcode
                == sqlite3.SQLITE_CONSTRAINT_UNIQUE
            ):
                continue

            log_error("get_users_inboxes: ", error)
            raise
            
def get_users_emails() -> None:
    '''
    Create one file for each mailbox with mails that are in `inbox` directory
    OR
    If the file exists it truncates it's content
    '''
    try:
        with conn.get_db() as db:
            db.execute(text("DELETE FROM user_emails "))    
            
            list_of_inboxes = db.execute(
                Select(
                    models.user_inboxes.inbox_name   
                )
            ).scalars().all()
    except Exception as e:
        log_error("Get user emails: ", e)
        raise ConnectionError
        
    for inbox in list_of_inboxes:
        emails = Path(f"{DOMAIN_PATH}/{inbox}/inbox").glob("*.imap")
        for email in emails:
            
            date_match = re.search(
                r"(\d{4})(\d{2})(\d{2})\d*\.imap$",
                os.path.basename(email),
            )
            
            if date_match is None:
                continue
    
            date_of_mail = dt.date(
                year=int(date_match.group(1)),
                month=int(date_match.group(2)),
                day=int(date_match.group(3)),
            )
            
            email_id = extract_message_id(
                filepath= Path(f"{DOMAIN_PATH}/{inbox}/{email}"),
                date_of_mail= date_of_mail,
            )
            
            try:
                with conn.get_db() as db:
                    user_inbox_id = db.execute(
                        Select(
                            models.user_inboxes
                        ).filter(
                            models.user_inboxes.inbox_name == inbox
                        )
                    ).scalar()
                    
                    new_entry = models.user_emails(
                        user_inbox_id = user_inbox_id,
                        email_id = email_id,
                    )
                    
                    db.add(new_entry)
                    db.commit()
            except Exception as e:
                log_error("new_entry at get user emails: ", e)
                raise ConnectionError

def get_shared_email() -> None:
    '''
    Creates a sqlite file that contains every mail from shared directory
    '''
    
    shared_emails = Path(SHARED_INBOX_LOCATION).rglob("*.imap")
    
    for email in shared_emails:
        basename = email.name
        absolute_path = str(email)
        date_match = re.search(
                r"(\d{4})(\d{2})(\d{2})\d*\.imap$",
                basename,
            )

        if date_match is None:
            continue

        try:
            date_of_mail = dt.date(
                year=int(date_match.group(1)),
                month=int(date_match.group(2)),
                day=int(date_match.group(3)),
            )
        except ValueError as error:
            log_error("Invalid date in filename: ", basename, " | ", error)
            continue
        message_id = extract_message_id(email, date_of_mail)
        try:
            with conn.get_db() as db:
                db.add(
                    models.shared_emails(
                        basename = basename,
                        absolute_path = absolute_path,
                        date_of_mail = date_of_mail,
                        message_id = message_id,
                        )
                    )
                db.commit()
        except sqlite3.IntegrityError as error:
            if error.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                pass
            else:
                log_error("get_shared_email: ", error, " | ", error.sqlite_errorcode)   
                db.rollback()
                raise Exception('Integrity Error')
    
def extract_message_id(filepath: Path, date_of_mail: dt.date) -> str | None:

    cutoff_date = dt.datetime.now() - dt.timedelta(days=int(MARK_OLDER_THAN))
    if date_of_mail > cutoff_date:
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
    