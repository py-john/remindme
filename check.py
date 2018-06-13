"""check.py:

Check saved reminders for any the need to be sent.

This is the file that cron runs automatically and shouldn't need 
to be called manually. When a reminder's time has passed it will be
sent via Twilio and reminders.json updated with the reminder removed.
If there are no more reminders left the cron job is removed and this
file will no longer run until a new reminder is made.

"""
import os
import json
from datetime import datetime

from crontab import CronTab
from mysms import textmyself

PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))
JSON_FILE = f'{PACKAGE_DIR}/reminders.json'


def remove_cronjob():
    """Remove the cronjob when the reminder dict is empty"""
    cron = CronTab(user='john')
    cron.remove_all(comment='check reminders')
    cron.write()


def check_reminders(reminders):
    """Delete and send text for any reminders that are in the past.

    Update the json file with current reminders after all the past
    reminders are sent and deleted.
    """
    sent_reminders = []
    have_sent = False
    for timestamp, reminder in reminders.items():
        if timestamp < datetime.now().isoformat():
            textmyself(reminder)
            sent_reminders.append(timestamp)
            have_sent = True
    for r in sent_reminders:
        del reminders[r]

    if not reminders:
        remove_cronjob()

    if have_sent:
        with open(JSON_FILE, 'w') as f:
            json.dump(reminders, f, indent=4)


def main():
    """Run the reminder check after reading in the saved json data."""
    try:
        with open(JSON_FILE, 'r') as f:
            reminders = json.load(f)
    except FileNotFoundError:
        print('reminders.json not found')
        raise SystemExit

    check_reminders(reminders)


if __name__ == '__main__':
    main()
