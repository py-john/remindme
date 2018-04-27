#!/usr/bin/env python3
import os
import json
import logging
from datetime import datetime

from crontab import CronTab
from mysms import textmyself

PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))
JSON_FILE = f'{PACKAGE_DIR}/reminders.json'

#logging.basicConfig(filename=f'{PACKAGE_DIR}/log.txt',
#                    format='%(asctime)s: %(message)s',
#                    datefmt='%F %T')
#
#logger = logging.getLogger(__name__)
#logger.setLevel('INFO')


def remove_cronjob():
    """Remove the cronjob when the reminder dict is empty"""
    cron = CronTab(user='john')
    cron.remove_all(comment='check reminders')
    cron.write()


def check_reminders():
    """Delete and send text for any reminders that are in the past.
    
    Update the json file with current reminders after all the past
    reminders are sent and deleted.
    """
    sent_reminders = []
    for timestamp, reminder in reminders.items():
        if timestamp < datetime.now().isoformat():
            textmyself(reminder)
            sent_reminders.append(timestamp)
            logger.info(f'Reminder sent: {reminder}')
    for r in sent_reminders:
        del reminders[r]

    if not reminders:
        remove_cronjob()

    with open(JSON_FILE, 'w') as f:
        json.dump(reminders, f, indent=4)


def main():
    """Run the reminder check after reading in the saved json data."""
    global reminders

    try:
        with open(JSON_FILE, 'r') as f:
            reminders = json.load(f)
    except FileNotFoundError:
        print('reminders.json not found')
        raise SystemExit

    check_reminders()


if __name__ == '__main__':
    main()
