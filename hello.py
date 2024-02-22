import traceback
import logging
import argparse
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA
from beautiful_date import Jan, Apr, Feb

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--id", required=True)
args = parser.parse_args()
calendar_id = args.id


try:
    print("Getting the calendar")
    calendar = GoogleCalendar(calendar_id,credentials_path='./credentials.json', token_path='./token.pickle')
    #calendar = GoogleCalendar(calendar_id)
    print("Creating event")
    event = Event(
        'Household hello.py Bin',
        start=(24 / Feb / 2024)[7:00]
    )
    print("Adding the event")
    calendar.add_event(event)
    print("done adding")
    for event in calendar:
        print(event)

except Exception as e:
    print(traceback.format_exc(),flush=True)
    logging.error(traceback.format_exc())
