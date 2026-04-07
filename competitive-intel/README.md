# 🕵️ Competitive Intelligence Monitor

A Python scraper that monitors competitor engineering blogs, careers pages, and product changelogs. It compares each scan against a local cache to surface only what's new, then generates a structured weekly intelligence brief. Designed to run weekly via cron with optional Telegram delivery.

## What It Monitors

| Source Type | Method | Example |
|------------|--------|---------|
| Engineering blogs | RSS/Atom feeds via `feedparser` | Blog posts, technical articles |
| Careers pages | HTML scraping via BeautifulSoup | New job postings, team growth |
| Product changelogs | HTML scraping via BeautifulSoup | Feature releases, updates |

## Prerequisites

- Python 3.11+

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure credentials (only needed for Telegram delivery)
cp .env.example .env

# Configure competitors to monitor
# Edit config.yaml with your competitor URLs and CSS selectors
```

## Usage

```bash
# Run the monitor
python main.py

# Enable Telegram delivery by setting telegram.enabled: true in config.yaml
```

On first run, all content is treated as "new" and cached. Subsequent runs only surface items not seen before.

## Configuration

Edit `config.yaml` to add competitors:

```yaml
competitors:
  - name: "CompetitorName"
    rss_feeds:
      - "https://competitor.com/blog/feed.xml"
    careers_pages:
      - url: "https://competitor.com/careers"
        selector: ".job-listing a"
    changelog_pages:
      - url: "https://competitor.com/changelog"
        selector: "article.changelog-entry"
```

The `selector` field is a CSS selector that targets individual items on the page. Inspect the competitor's page to find the right selector.

## Cron Job Setup

Add to your crontab (`crontab -e`) to run every Monday at 8:00 AM:

```cron
0 8 * * 1 cd /path/to/competitive-intel && /usr/bin/python3 main.py >> /var/log/competitive-intel.log 2>&1
```

## Rate Limiting and Respectful Scraping

This tool is designed to be a respectful scraper:

- **Rate limiting**: A built-in delay (2-3 seconds) between requests prevents hammering servers
- **User-Agent**: Requests include a descriptive User-Agent header identifying the bot
- **Frequency**: Designed for weekly runs, not continuous polling
- **Scope**: Only fetches the specific pages configured, no recursive crawling
- **Caching**: Local cache means previously seen content is never re-processed

Please respect `robots.txt` and terms of service for the sites you monitor. Adjust CSS selectors if a site's structure changes.

## Sample Output

See [sample_output.md](./sample_output.md) for an example weekly brief.

## License

MIT
