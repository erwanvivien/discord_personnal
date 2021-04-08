# Needed for requests
import requests
# Needed to reed json
import json

# Needed to open files
import os
# Needed to read date
import datetime


LOG_FILE = "db/log"

BOT_IDS = [828710667984306200, 828710723529867264]  # Normal, Dev
DEV_IDS = [289145021922279425]  # Me


def get_content(file):
    # Read file content
    try:
        file = open(file, "r")
        s = file.read()
        file.close()
    except Exception as error:
        log("get_content", error, f"error reading file {file}")
        return ""
    return s

# Logs every commands


def log(fctname, error, message):
    """
    Pretty printer for logs
    """

    now = datetime.datetime.now()
    log = f"[{now}]: " + \
        str(error) + '\n' + ('+' * 4) + (' ' * 4) + \
        fctname + (" " * (20-len(fctname))) + \
        ': ' + message + '\n'

    print(log)

    f = open(LOG_FILE, "a+")

    f.write(log)
    f.close()


def clean_dir(subpath, dir, db):
    try:
        res = db.mappings_get(int(dir))
    except:
        os.removedirs(subpath + dir)
        return

    cur_path = subpath + dir + os.sep

    mappings = [e[1].split("/")[-1] for e in res]

    for _, _, files in os.walk(cur_path):
        for f in files:
            if not f in mappings:
                os.remove(cur_path + f)
                print("removed", cur_path + f)


def cleanup():
    import database as db
    for subdir, dirs, _ in os.walk('assets'):
        for d in dirs:
            clean_dir(subdir + os.sep, d, db)


# Creates the db dir and the log file if needed
if not os.path.exists("db"):
    os.mkdir("db")
    f = open(LOG_FILE, "w")
    f.close()

# Create the assets dir if non-existent
if not os.path.exists("assets"):
    os.mkdir("assets")
