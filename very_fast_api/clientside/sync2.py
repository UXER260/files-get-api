import datetime
import os
import sys
import time

import funcs

LOG_FILE = 'clientside/log.txt'
REQUEST_PATH = "http://localhost:8000/apis/files/"

with open(LOG_FILE, 'r') as F:
    Log = F.readlines()


def log(string, hour=None, minute=None, second=None, year=None, month=None, day=None
        ):
    now = datetime.datetime.now()
    if hour is None:
        hour = now.hour
    if minute is None:
        minute = now.minute
    if second is None:
        second = now.second
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    if day is None:
        day = now.day
    text = f"{string} | at: {hour}:{minute}:{second} | {year}-{month}-{day}"
    print(text)
    with open(LOG_FILE, 'a') as f:
        f.write('\n' + text)

    Log.append(text)


def sync(local_dir, freq=6):
    server_files = set(funcs.get_all_filenames(url=REQUEST_PATH + "all_names"))
    local_files = set([file for file in os.listdir(local_dir) if not file.startswith(".")])

    deleted_files = server_files - local_files
    added_files = local_files - server_files
    other_files = local_files - added_files - deleted_files

    # check 1: remove the deleted files from the server directory
    for file_name in deleted_files:
        log(f"File `{file_name}` was moved/renamed/deleted.")
        funcs.delete_file(url=REQUEST_PATH + "delete", filename=file_name)

    # check 2: add the added files to the server directory
    for file_name in added_files:
        log(f"File `{file_name}` was added.")
        path = os.path.join(local_dir, file_name)

        funcs.upload_file(url=REQUEST_PATH + "upload", filename=file_name, path=path)

    # check 3: edit the edited files in the server directory
    for file_name in other_files:
        path_local = os.path.join(local_dir, file_name)
        with open(path_local, 'rb') as f:
            content_local = f.read()
        content_server = funcs.get_file_data(url=REQUEST_PATH, filename=file_name)

        # print(file_name, "server:", content_server, "local:", content_local)
        if content_server != content_local:
            log(f"File `{file_name}` was edited.")
            funcs.replace_file_data(url=REQUEST_PATH + "edit", filename=file_name, path=path_local)

    time.sleep(freq)


if __name__ == '__main__':
    log('Waiting for changes...')
    local_directory = 'clientside/local_folder'

    while True:

        try:
            sync(local_directory)
        except FileNotFoundError as error:
            log(error)
            print('this most likely happend due to made change while syncing.'
                  '\ncontinuing...')
        except KeyboardInterrupt:
            log('Stop Syncing')
            sys.exit(0)
