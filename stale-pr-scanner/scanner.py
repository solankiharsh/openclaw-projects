"""GitHub PR scanning and categorization logic."""

import os
import time
from datetime import datetime, timezone

from github import Github


CATEGORIES = {
    "waiting_for_review": "Waiting for review",
    "changes_requested": "Changes requested",
    "approved_not_merged": "Approved, not merged",
    "review_in_progress": "Review in progress",
}


def scan_repos(repos, stale_hours=48):
    """Scan repositories and return a list of stale PRs with category metadata.

    Returns list of dicts: {repo, title, author, age_hours, age_days, category, url, created_at}
    """
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is required.")

    g = Github(token)
    stale_prs = []

    for repo_name in repos:
        _check_rate_limit(g)

        try:
            repo = g.get_repo(repo_name)
        except Exception as exc:
            print(f"  Warning: could not access {repo_name} — {exc}")
            continue

        for pr in repo.get_pulls(state="open", sort="created", direction="asc"):
            created = pr.created_at.replace(tzinfo=timezone.utc)
            age_hours = (datetime.now(timezone.utc) - created).total_seconds() / 3600

            if age_hours < stale_hours:
                continue

            category = _categorize_pr(pr)
            stale_prs.append(
                {
                    "repo": repo_name,
                    "title": pr.title,
                    "number": pr.number,
                    "author": pr.user.login,
                    "age_hours": round(age_hours, 1),
                    "age_days": round(age_hours / 24, 1),
                    "category": category,
                    "url": pr.html_url,
                    "created_at": created.isoformat(),
                }
            )

        print(f"  Scanned {repo_name}")

    return sorted(stale_prs, key=lambda p: p["age_hours"], reverse=True)


def _categorize_pr(pr):
    """Determine the review status category for a PR."""
    reviews = list(pr.get_reviews())

    if not reviews and pr.get_comments() == 0 and pr.get_review_comments() == 0:
        return CATEGORIES["waiting_for_review"]

    latest_states = {}
    for review in reviews:
        if review.user and review.state != "COMMENTED":
            latest_states[review.user.login] = review.state

    states = set(latest_states.values())

    if "CHANGES_REQUESTED" in states:
        return CATEGORIES["changes_requested"]

    if "APPROVED" in states:
        return CATEGORIES["approved_not_merged"]

    if reviews or pr.get_comments() > 0 or pr.get_review_comments() > 0:
        return CATEGORIES["review_in_progress"]

    return CATEGORIES["waiting_for_review"]


def _check_rate_limit(g):
    """Sleep if GitHub API rate limit is running low."""
    rate = g.get_rate_limit().core
    if rate.remaining < 50:
        reset_time = rate.reset.replace(tzinfo=timezone.utc)
        wait_seconds = (reset_time - datetime.now(timezone.utc)).total_seconds() + 5
        if wait_seconds > 0:
            print(f"  Rate limit low ({rate.remaining} remaining). Sleeping {int(wait_seconds)}s...")
            time.sleep(wait_seconds)
