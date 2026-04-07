"""Careers page scraper using BeautifulSoup."""

import time

import requests
from bs4 import BeautifulSoup


REQUEST_DELAY = 3  # seconds between requests
USER_AGENT = "OpenClaw-CompetitiveIntel/1.0 (respectful-bot; weekly-scan)"


def scrape_careers_pages(url, selector):
    """Scrape a careers page and extract job postings.

    Args:
        url: The careers page URL.
        selector: CSS selector for individual job listing elements.

    Returns list of dicts: {title, team, location, url}
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

    jobs = []
    for el in elements[:30]:
        title = el.get_text(strip=True)
        link = el.get("href", "")
        if link and not link.startswith("http"):
            from urllib.parse import urljoin
            link = urljoin(url, link)

        team = ""
        location = ""

        team_el = el.select_one("[data-team], .team, .department")
        if team_el:
            team = team_el.get_text(strip=True)

        location_el = el.select_one("[data-location], .location")
        if location_el:
            location = location_el.get_text(strip=True)

        if title:
            jobs.append(
                {
                    "title": title,
                    "team": team,
                    "location": location,
                    "url": link,
                }
            )

    return jobs
