import datetime
import os
import time
import sys

LOG_FILE = 'log.txt'

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


def sync(base_dir, local_dir, freq=3):
    base_files = set(os.listdir(base_dir))
    local_files = set(os.listdir(local_dir))

    deleted_files = base_files - local_files
    added_files = local_files - base_files

    # check 1: remove the deleted files from the base directory
    for file_name in deleted_files:
        log(f"File `{file_name}` was moved/renamed/deleted.")
        os.remove(os.path.join(base_dir, file_name))

    # check 2: add the added files to the base directory
    for file_name in added_files:
        log(f"File `{file_name}` was added.")
        with open(os.path.join(base_dir, file_name), 'wb') as f:  # file to write to
            with open(os.path.join(local_dir, file_name), 'rb') as f2:  # to write from
                f.write(f2.read())

    # check 3: edit the edited files in the base directory
    for file_name in local_files - added_files - deleted_files:
        with open(os.path.join(local_dir, file_name), 'rb') as f:
            file_data_local = f.read()
        with open(os.path.join(base_dir, file_name), 'rb') as f:
            file_data_base = f.read()

        if file_data_base != file_data_local:  # when file was edited
            log(f"File `{file_name}` was edited.")
            with open(os.path.join(base_dir, file_name), 'wb') as f:
                f.write(file_data_local)

    time.sleep(freq)


if __name__ == '__main__':
    log('Waiting for changes...')
    base_directory = 'server_side_folder'
    local_directory = 'local_folder'

    while True:

        try:
            sync(base_directory, local_directory)
        except FileNotFoundError as error:
            log(error)
            print('this most likely happend due to made change while syncing.'
                  '\ncontinuing...')
        except KeyboardInterrupt:
            log('Stop Syncing')
            sys.exit(0)
