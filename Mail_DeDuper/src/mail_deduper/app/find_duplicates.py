import os
import shutil
import glob
from pathlib import Path

from Mail_DeDuper.src.mail_deduper.app.load_config import assign_environmental_to_variables as lc
from Mail_DeDuper.src.mail_deduper.app.load_config import load_excluded_users_from_deduplication

from Mail_DeDuper.src.mail_deduper.app.progress_bar import print_progress
from Mail_DeDuper.src.mail_deduper.app.gather_emails import  extract_message_id
from Mail_DeDuper.main import BASE_DIR 

DOMAIN_LOCATION = lc.DOMAIN_LOCATION
USERS_INBOX_LOCATION = lc.USERS_INBOX_LOCATION
SHARED_INBOX_LOCATION = lc.SHARED_INBOX_LOCATION
MARK_OLDER_THAN = lc.MARK_OLDER_THAN

EXCLUDED_USERS = load_excluded_users_from_deduplication()

LIST_OF_INBOXES_PATH = Path(BASE_DIR, "Mail_DeDuper", "lists_of", "list_of_inboxes.txt")
LIST_OF_SHARED_EMAILS_PATH = Path(BASE_DIR, "Mail_DeDuper", "lists_of", "list_of_shared_emails.txt")
FOLDER_FOR_LISTS_OF_DUPES_LOCATION = Path(BASE_DIR, "Mail_DeDuper", "lists_of", "lists_of_duped_mails")
DUPED_MAILS_STATISTICS_FOLDER_LOCATION = Path(BASE_DIR)

def find_dupes() -> None:
    '''Finds duplicates by comparing Message-ID between `_wspolne` and user inboxes'''

    #---- Ensure the duplicates folder exists and is empty ----
    if os.path.exists(FOLDER_FOR_LISTS_OF_DUPES_LOCATION):
        shutil.rmtree(FOLDER_FOR_LISTS_OF_DUPES_LOCATION)
    os.mkdir(FOLDER_FOR_LISTS_OF_DUPES_LOCATION)

    #TODO---- Generate a file per operation ----
    #---- Truncate the statistics file ----
    open(DUPED_MAILS_STATISTICS_FOLDER_LOCATION, "w").close()

    with open(LIST_OF_SHARED_EMAILS_PATH) as wspolne:
        wspolne_paths = [line.strip() for line in wspolne if line.strip()]

    wspolne_ids = set()
    total = len(wspolne_paths)
    for index, path in enumerate(wspolne_paths, 1):
        msg_id = extract_message_id(path)
        if msg_id:
            wspolne_ids.add(msg_id)
        if index % 500 == 0 or index == total:
            print_progress(index, total, label="_wspolne")

    users_inboxes = glob.glob(f"{USERS_INBOX_LOCATION}/*.txt")

    for user_email in users_inboxes:
        username = os.path.basename(user_email)[:-4]

        if username in EXCLUDED_USERS:
            continue

        with open(user_email) as f:
            user_mail_paths = [line.strip() for line in f if line.strip()]

        dupes_found = 0
        total_user = len(user_mail_paths)
        user_dupes_path = os.path.join(FOLDER_FOR_LISTS_OF_DUPES_LOCATION, f"{username}.txt")

        with open(user_dupes_path, "w") as marked_file:
            for index, mail_path in enumerate(user_mail_paths, 1):
                msg_id = extract_message_id(mail_path)
                if msg_id and msg_id in wspolne_ids:
                    dupes_found += 1
                    marked_file.write(mail_path + "\n")
                if total_user and (index % 500 == 0 or index == total_user):
                    print_progress(index, total_user, label=username)

        if dupes_found:
            with open(DUPED_MAILS_STATISTICS_FOLDER_LOCATION, "a") as status_f:
                status_f.write(f"{username}: {dupes_found}\n")
            print(f"{username}: {dupes_found} duplicate(s) found")
        else:
            os.remove(user_dupes_path)
   