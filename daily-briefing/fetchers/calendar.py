"""Fetch today's events from Google Calendar using a service account."""

from datetime import datetime, timedelta, timezone

from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def fetch_calendar_events(cfg):
    """Return a list of dicts with today's calendar events.

    Each dict: {summary, start, end, attendees, location}
    """
    creds_path = cfg.get("google_service_account_json", "")
    calendar_id = cfg.get("calendar_id", "primary")

    if not creds_path:
        return []

    credentials = service_account.Credentials.from_service_account_file(
        creds_path, scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=credentials)

    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=start_of_day.isoformat(),
            timeMax=end_of_day.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = []
    for item in result.get("items", []):
        start = item.get("start", {}).get("dateTime", item.get("start", {}).get("date", ""))
        end = item.get("end", {}).get("dateTime", item.get("end", {}).get("date", ""))
        attendees = [
            a.get("email", "")
            for a in item.get("attendees", [])
            if not a.get("self", False)
        ]
        events.append(
            {
                "summary": item.get("summary", "(No title)"),
                "start": start,
                "end": end,
                "attendees": attendees,
                "location": item.get("location", ""),
            }
        )

    return events
