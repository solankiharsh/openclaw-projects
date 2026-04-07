"""Stale PR Scanner — find and categorize open PRs older than 48 hours."""

import sys
from pathlib import Path

from dotenv import load_dotenv

from scanner import scan_repos
from reporter import build_report
from telegram import send_telegram_message


def main():
    load_dotenv()

    config_path = Path(__file__).parent / "config.yaml"
    if not config_path.exists():
        print("Error: config.yaml not found. Copy config.yaml.example and configure it.")
        sys.exit(1)

    import yaml

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    repos = cfg.get("repositories", [])
    if not repos:
        print("No repositories configured in config.yaml.")
        sys.exit(1)

    stale_hours = cfg.get("stale_threshold_hours", 48)
    send_to_telegram = cfg.get("telegram", {}).get("enabled", False)

    print(f"Scanning {len(repos)} repositories for PRs older than {stale_hours}h...")

    stale_prs = scan_repos(repos, stale_hours=stale_hours)
    report = build_report(stale_prs, stale_hours=stale_hours)

    print(report)

    if send_to_telegram:
        try:
            send_telegram_message(report)
            print("\nReport sent to Telegram.")
        except Exception as exc:
            print(f"\nFailed to send to Telegram: {exc}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
