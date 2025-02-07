from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json

def delete_event(creds, event_id):
    try:
        service = build("calendar", "v3", credentials=creds)
        service.events().delete(
            calendarId="primary",
            eventId=event_id
        ).execute()
        return True
    except Exception as e:
        print(f"Delete error: {e}")
        return False
    s
def fetch_all_events(creds):
    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.utcnow().isoformat() + "Z"
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        return events_result.get("items", [])
    except Exception as e:
        print(f"Fetch error: {e}")
        return []

def add_event_to_calendar(creds, event):
    try:
        service = build("calendar", "v3", credentials=creds)
        created_event = service.events().insert(
            calendarId="primary",
            body=event
        ).execute()
        return created_event
    except Exception as e:
        print(f"Add event error: {e}")
        return None