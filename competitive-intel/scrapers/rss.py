"""RSS/Atom feed scraper using feedparser."""

import time

import feedparser


REQUEST_DELAY = 2  # seconds between requests


def scrape_rss_feeds(feed_url):
    """Parse an RSS/Atom feed and return a list of post dicts.

    Each dict: {title, link, published, summary}
    """
    time.sleep(REQUEST_DELAY)

    feed = feedparser.parse(feed_url)
    posts = []

    for entry in feed.entries[:20]:
        summary = entry.get("summary", "")
        if len(summary) > 200:
            summary = summary[:197] + "..."

        posts.append(
            {
                "title": entry.get("title", "(untitled)"),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": summary,
            }
        )

    return posts
