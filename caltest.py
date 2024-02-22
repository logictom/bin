from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA
import argparse
import json
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--id", required=True)
parser.add_argument("-f", "--file", required=True)
args = parser.parse_args()

calendar_id = args.id
f = open(args.file)

calendar = GoogleCalendar(
    calendar_id, credentials_path="./credentials.json", token_path="./token.pickle"
)

data = json.load(f)

date_format = "%Y-%m-%d %H:%M:%S"

for entry in data["bins"]:
    # print(f"{entry['bin']} on {entry['date']}")
    date_obj = datetime.strptime(entry["date"], date_format)
    # print(date_obj)
    event = Event(entry['bin'], start=date_obj, timezone="Europe/London")
    calendar.add_event(event)

print(f"Retrigger on {data['triggerdate']}")
date_obj = datetime.strptime(data["triggerdate"], date_format)
#print(date_obj)
event = Event("Trigger", start=date_obj, timezone="Europe/London")
calendar.add_event(event)

print(f"Processed on {data['processeddate']}")
date_obj = datetime.strptime(data["processeddate"], date_format)
#print(date_obj)
event = Event("Processed", start=date_obj, end=(date_obj + timedelta(minutes=1)), timezone="Europe/London")
calendar.add_event(event)

# Closing file
f.close()
