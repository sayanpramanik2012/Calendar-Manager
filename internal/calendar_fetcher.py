import datetime as dt
from googleapiclient.discovery import build
import os.path
from google.oauth2.credentials import Credentials


def fetch_all_events():
    if os.path.exists("./assets/token.json"):
        creds = Credentials.from_authorized_user_file("./assets/token.json")
    service = build("calendar", "v3", credentials=creds)
    now = dt.datetime.utcnow().isoformat() + "Z"
    event_results = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=12,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = event_results.get("items", [])

    if not events:
        print("No upcoming events found.")
        return []

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])

    return events
