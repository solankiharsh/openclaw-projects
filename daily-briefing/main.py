"""Daily Briefing Generator — aggregates calendar, PRs, tasks, and email into a morning briefing."""

import sys
from datetime import datetime

import click
from dotenv import load_dotenv

from config import load_config
from fetchers.calendar import fetch_calendar_events
from fetchers.github import fetch_open_prs
from fetchers.clickup import fetch_priority_tasks
from fetchers.gmail import fetch_email_snapshot
from formatter import build_briefing
from telegram import send_telegram_message


@click.command()
@click.option("--telegram", is_flag=True, help="Send the briefing via Telegram Bot API.")
@click.option("--output", "-o", type=click.Path(), help="Write the briefing to a file.")
def main(telegram, output):
    """Generate a formatted morning briefing from Calendar, GitHub, ClickUp, and Gmail."""
    load_dotenv()
    cfg = load_config()

    click.echo(f"Generating briefing for {datetime.now().strftime('%A, %B %d %Y')}...\n")

    events = _fetch_safe("Google Calendar", lambda: fetch_calendar_events(cfg))
    prs = _fetch_safe("GitHub PRs", lambda: fetch_open_prs(cfg))
    tasks = _fetch_safe("ClickUp Tasks", lambda: fetch_priority_tasks(cfg))
    email = _fetch_safe("Gmail", lambda: fetch_email_snapshot(cfg))

    briefing = build_briefing(events, prs, tasks, email)

    click.echo(briefing)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(briefing)
        click.echo(f"\nBriefing written to {output}")

    if telegram:
        try:
            send_telegram_message(briefing)
            click.echo("\nBriefing sent to Telegram.")
        except Exception as exc:
            click.echo(f"\nFailed to send to Telegram: {exc}", err=True)
            sys.exit(1)


def _fetch_safe(source_name, fetcher):
    """Run a fetcher and return an empty result on failure instead of crashing."""
    try:
        return fetcher()
    except Exception as exc:
        click.echo(f"  Warning: could not fetch {source_name} — {exc}", err=True)
        return []


if __name__ == "__main__":
    main()
