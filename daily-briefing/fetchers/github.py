"""Fetch open pull requests from configured GitHub repositories."""

from datetime import datetime, timezone

from github import Github


def fetch_open_prs(cfg):
    """Return a list of dicts with open PRs across configured repos.

    Each dict: {repo, title, author, url, created_at, age_days}
    """
    token = cfg.get("github_token", "")
    repos = cfg.get("github_repos", [])

    if not token or not repos:
        return []

    g = Github(token)
    prs = []

    for repo_name in repos:
        try:
            repo = g.get_repo(repo_name)
            for pr in repo.get_pulls(state="open", sort="created", direction="desc"):
                age = (datetime.now(timezone.utc) - pr.created_at.replace(tzinfo=timezone.utc)).days
                prs.append(
                    {
                        "repo": repo_name,
                        "title": pr.title,
                        "author": pr.user.login,
                        "url": pr.html_url,
                        "created_at": pr.created_at.isoformat(),
                        "age_days": age,
                    }
                )
        except Exception as exc:
            prs.append({"repo": repo_name, "title": f"(error: {exc})", "author": "", "url": "", "created_at": "", "age_days": 0})

    return prs
