"""remindme.py:

Terminal reminder system using twilio.

Called from the remindme executable file with the arguments being 
a readable time frame, the word 'to', and the reminder itself:

remindme [time frame] to [reminder]

Examples:
    
    remindme in 30 minutes to call mark
    remindme on march 5th at 9:30am to go to the doctor appointment

Reminders are saved to a json filed and check automatically via cron.

"""
import os
import json
from sys import argv
from datetime import datetime

import dateparser
from crontab import CronTab

PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))
JSON_FILE = f'{PACKAGE_DIR}/reminders.json'
CRON_CMD = ('. /Users/john/.bash_profile; checkreminders'
            f' >> {PACKAGE_DIR}/crontab.log 2>&1')


def argv_is_valid():
    """Check if CL arg format is valid, returns boolean."""
    if len(argv) < 4:
        return False
    if 'to' not in argv[2:]:
        return False
    time_input, *reminder = ' '.join(argv[1:]).split(' to ')
    if not (time_input and reminder):
        return False
    return True


def save_reminder():
    """Split CL args and save reminder if it's in the future."""
    time_input, *reminder = ' '.join(argv[1:]).split(' to ')
    reminder_time = dateparser.parse(time_input)
    if reminder_time < datetime.now():
        print('Error: reminder time is in the past')
        raise SystemExit
    reminders[reminder_time.isoformat()] = ' to '.join(reminder)
    with open(JSON_FILE, 'w') as f:
        json.dump(reminders, f, indent=4)
    set_crontab()


def set_crontab():
    """Set the cron job if it doesn't already exist."""
    cron = CronTab(user='john')
    for job in cron:
        if job.comment == 'check reminders':
            return None
    job = cron.new(command=CRON_CMD, comment='check reminders')
    job.minute.every(1)
    cron.write()


if __name__ == '__main__':
    if not argv_is_valid():
        print("Usage: remindme (in time frame/at time) to (reminder)")
        raise SystemExit
    try:
        with open(JSON_FILE, 'r') as f:
            reminders = json.load(f)
    except FileNotFoundError:
        reminders = {}
    save_reminder()
