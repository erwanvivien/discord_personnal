# Needed for requests
import requests
# Needed to reed json
import json

# Needed to open files
import os
# Needed to read date
import datetime


LOG_FILE = "db/log"

BOT_IDS = [828710667984306200, 828710723529867264]


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


# Creates the db dir and the log file if needed
if not os.path.exists("db"):
    os.mkdir("db")
    f = open(LOG_FILE, "w")
    f.close()
