"""Competitive Intelligence Monitor — track competitor blogs, careers, and changelogs."""

import sys
from pathlib import Path

from dotenv import load_dotenv
import yaml

from scrapers.rss import scrape_rss_feeds
from scrapers.careers import scrape_careers_pages
from scrapers.changelog import scrape_changelogs
from cache import load_cache, save_cache, diff_entries
from reporter import build_weekly_brief
from telegram import send_telegram_message


def main():
    load_dotenv()

    config_path = Path(__file__).parent / "config.yaml"
    if not config_path.exists():
        print("Error: config.yaml not found.")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    competitors = cfg.get("competitors", [])
    if not competitors:
        print("No competitors configured in config.yaml.")
        sys.exit(1)

    cache = load_cache()

    print(f"Scanning {len(competitors)} competitor(s)...\n")

    all_blog_posts = []
    all_jobs = []
    all_changelog_items = []

    for comp in competitors:
        name = comp.get("name", "Unknown")
        print(f"  Scanning {name}...")

        rss_feeds = comp.get("rss_feeds", [])
        for feed_url in rss_feeds:
            posts = scrape_rss_feeds(feed_url)
            new_posts = diff_entries(cache, f"rss:{feed_url}", posts, key="link")
            for p in new_posts:
                p["competitor"] = name
            all_blog_posts.extend(new_posts)

        careers_pages = comp.get("careers_pages", [])
        for career_cfg in careers_pages:
            url = career_cfg.get("url", "")
            selector = career_cfg.get("selector", "")
            jobs = scrape_careers_pages(url, selector)
            new_jobs = diff_entries(cache, f"careers:{url}", jobs, key="title")
            for j in new_jobs:
                j["competitor"] = name
            all_jobs.extend(new_jobs)

        changelog_pages = comp.get("changelog_pages", [])
        for cl_cfg in changelog_pages:
            url = cl_cfg.get("url", "")
            selector = cl_cfg.get("selector", "")
            items = scrape_changelogs(url, selector)
            new_items = diff_entries(cache, f"changelog:{url}", items, key="title")
            for item in new_items:
                item["competitor"] = name
            all_changelog_items.extend(new_items)

    brief = build_weekly_brief(all_blog_posts, all_jobs, all_changelog_items)
    print(brief)

    send_to_telegram = cfg.get("telegram", {}).get("enabled", False)
    if send_to_telegram:
        try:
            send_telegram_message(brief)
            print("\nBrief sent to Telegram.")
        except Exception as exc:
            print(f"\nFailed to send to Telegram: {exc}", file=sys.stderr)

    save_cache(cache)
    print("\nCache updated.")


if __name__ == "__main__":
    main()
