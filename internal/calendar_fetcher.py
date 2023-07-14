import datetime as dt
from googleapiclient.discovery import build
import os.path
from google.oauth2.credentials import Credentials
import json


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
            maxResults=5,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = event_results.get("items", [])

    if not events:
        print("No upcoming events found.")
        return []

    upcoming_events = []

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        summary = event["summary"]
        event_data = {"date": f"{start} {summary}", "alert": "0"}
        upcoming_events.append(event_data)
        print(start, summary)

    # Save the events to a JSON file
    with open("./assets/upcoming.json", "w") as file:
        json.dump({"dates": upcoming_events}, file)

    return events
