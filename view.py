#!/usr/bin/env python3
import os
import json

import arrow
from crontab import CronTab

PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))
JSON_FILE = f'{PACKAGE_DIR}/reminders.json'


def format_timestamp(iso_str):
    """Return formatted timestamp from iso timestamp input."""
    dt = arrow.get(iso_str)
    return dt.format('ddd MM/DD/YYYY - hh:mm A')


def force_input(prompt, options):
    """Return user input that's forced to be within an options set."""
    choice = input(prompt)
    while choice not in options:
        print('Invalid Choice')
        choice = input(prompt)
    return choice.lower()


def print_reminders():
    """Print a numbered list of reminders with formated timestamps."""
    print()
    for index, iso_str in enumerate(sorted(reminders), 1):
        print(f'{index}) {format_timestamp(iso_str)} -> {reminders[iso_str]}')
    print()


def update_crontab():
    """Remove cron job if the reminders dict is empty."""
    if not reminders:
        cron = CronTab(user='john')
        cron.remove_all(comment='check reminders')
        cron.write()
        save_reminders()
        print('\n--Reminder List Empty--\n')
        input('(exit)')
        raise SystemExit


def get_index():
    """Get user input for index of reminder to be removed."""
    while True:
        try:
            choice = int(input(
                        'Number of reminder to delete (0 to go back): '))
        except ValueError:
            continue
        if 0 <= choice <= len(reminders):
            return choice
        else:
            print('Invalid Number')


def delete_reminder():
    """Removed the chosen reminder from the dict after confirming."""
    index = get_index()
    if index == 0:
        return None
    key = sorted(reminders)[index-1]
    time_str = format_timestamp(key)
    prompt = f'Delete {time_str} - {reminders[key]}? [y/n]: '
    choice = force_input(prompt, {'y', 'yes', 'n', 'no'})
    if choice in {'y', 'yes'}:
        del(reminders[key])
        print("Deleted")
    else:
        print('Not Deleted')


def save_reminders():
    """Save reminders dict to json file."""
    with open(JSON_FILE, 'w') as f:
        json.dump(reminders, f)


def run_menu():
    """Display reminders and prompt for user selected option."""
    if not reminders:
        print('\n--No Reminders--\n')
        raise SystemExit
    print_reminders()
    prompt = '(d)elete / (q)uit: '
    while True:
        choice = force_input(prompt, {'d', 'delete', 'q', 'quit'})
        if choice in {'d', 'delete'}:
            delete_reminder()
            update_crontab()
            print_reminders()
            save_reminders()
        else:
            raise SystemExit


def main():
    """Load reminders from json file or exit if no file found."""
    global reminders
    try:
        with open(JSON_FILE, 'r') as f:
            reminders = json.load(f)
    except FileNotFoundError:
        print('reminders.json not found')
        raise SystemExit
    run_menu()


if __name__ == '__main__':
    main()
