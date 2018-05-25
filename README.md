# remindme

Command line reminder system using twilio messaging and dateparser.

Inspired by the RemindMe bot on reddit, type reminders in the command line using English sentences of the form:\
`remindme [readable time/time frame] to [reminder]`

### Examples:\
`remindme in 2 hours to call mark`\
`remindme tomorrow to check the weekend forecast`\
`remindme on march 1st to pay the rent`

Reminders are saved to a json file which is checked by a dymically created cron job. The job is removed when there are no reminders left.
