"""Changelog / product updates page scraper."""

import time

import requests
from bs4 import BeautifulSoup


REQUEST_DELAY = 3
USER_AGENT = "OpenClaw-CompetitiveIntel/1.0 (respectful-bot; weekly-scan)"


def scrape_changelogs(url, selector):
    """Scrape a changelog page and extract update entries.

    Args:
        url: The changelog page URL.
        selector: CSS selector for individual changelog entry elements.

    Returns list of dicts: {title, date, description}
    """
    if not url or not selector:
        return []

    time.sleep(REQUEST_DELAY)

    resp = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=15,
    )
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    elements = soup.select(selector)

    items = []
    for el in elements[:20]:
        title = ""
        heading = el.select_one("h1, h2, h3, h4, [class*='title']")
        if heading:
            title = heading.get_text(strip=True)
        else:
            title = el.get_text(strip=True)[:100]

        date = ""
        date_el = el.select_one("time, [class*='date'], [datetime]")
        if date_el:
            date = date_el.get("datetime", "") or date_el.get_text(strip=True)

        description = ""
        desc_el = el.select_one("p, [class*='description'], [class*='summary']")
        if desc_el:
            description = desc_el.get_text(strip=True)[:200]

        if title:
            items.append(
                {
                    "title": title,
                    "date": date,
                    "description": description,
                }
            )

    return items
