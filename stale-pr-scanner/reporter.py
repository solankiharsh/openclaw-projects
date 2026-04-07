"""Markdown report generation for stale PRs."""

from collections import Counter
from datetime import datetime


def build_report(stale_prs, stale_hours=48):
    """Build a formatted markdown report from categorized stale PRs."""
    now = datetime.now()
    lines = [
        f"# Stale PR Report — {now.strftime('%A, %B %d %Y')}",
        "",
        f"PRs open longer than **{stale_hours} hours** across monitored repositories.",
        "",
    ]

    if not stale_prs:
        lines.append("No stale PRs found. All clear!")
        return "\n".join(lines)

    lines += _summary_section(stale_prs)
    lines += _table_section(stale_prs)

    return "\n".join(lines)


def _summary_section(stale_prs):
    lines = ["## Summary", ""]
    counts = Counter(pr["category"] for pr in stale_prs)

    lines.append(f"**{len(stale_prs)}** stale PRs found:")
    lines.append("")
    for category, count in counts.most_common():
        lines.append(f"- {category}: **{count}**")
    lines.append("")

    return lines


def _table_section(stale_prs):
    lines = ["## Details", ""]
    lines.append("| Repo | PR | Author | Age | Category |")
    lines.append("|------|-----|--------|-----|----------|")

    for pr in stale_prs:
        repo = pr["repo"].split("/")[-1]
        title = pr["title"][:50]
        if len(pr["title"]) > 50:
            title += "..."
        link = f"[#{pr['number']} {title}]({pr['url']})"
        age = f"{pr['age_days']}d"
        lines.append(f"| {repo} | {link} | {pr['author']} | {age} | {pr['category']} |")

    lines.append("")
    return lines
