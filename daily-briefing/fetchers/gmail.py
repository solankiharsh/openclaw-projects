"""Fetch unread email count and top subject lines from Gmail."""

from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def fetch_email_snapshot(cfg):
    """Return a dict with unread_count and top_subjects list.

    Uses a service account with domain-wide delegation, or OAuth credentials.
    """
    creds_path = cfg.get("gmail_credentials_json", "")
    user_email = cfg.get("gmail_user_email", "me")

    if not creds_path:
        return {"unread_count": 0, "top_subjects": []}

    credentials = service_account.Credentials.from_service_account_file(
        creds_path, scopes=SCOPES
    )
    if user_email != "me":
        credentials = credentials.with_subject(user_email)

    service = build("gmail", "v1", credentials=credentials)

    unread = (
        service.users()
        .messages()
        .list(userId="me", q="is:unread", maxResults=1)
        .execute()
    )
    unread_count = unread.get("resultSizeEstimate", 0)

    messages = (
        service.users()
        .messages()
        .list(userId="me", q="is:unread", maxResults=3)
        .execute()
    )

    top_subjects = []
    for msg_meta in messages.get("messages", [])[:3]:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=msg_meta["id"], format="metadata", metadataHeaders=["Subject"])
            .execute()
        )
        headers = msg.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(no subject)")
        top_subjects.append(subject)

    return {"unread_count": unread_count, "top_subjects": top_subjects}
