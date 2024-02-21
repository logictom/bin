import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--id", required=True)
args = parser.parse_args()
calendar_id = args.id

from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA

from beautiful_date import Jan, Apr, Feb

calendar = GoogleCalendar(calendar_id)
event = Event(
    'Household Bin',
    start=(24 / Feb / 2024)[7:00]
)

calendar.add_event(event)

for event in calendar:
    print(event)
