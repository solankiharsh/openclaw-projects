"""Generate a structured weekly competitive intelligence brief."""

from datetime import datetime


def build_weekly_brief(blog_posts, jobs, changelog_items):
    """Build the full markdown weekly brief from scraped data."""
    now = datetime.now()
    lines = [
        f"# Competitive Intelligence Brief — Week of {now.strftime('%B %d, %Y')}",
        "",
    ]

    lines += _section_blog_posts(blog_posts)
    lines += _section_jobs(jobs)
    lines += _section_changelog(changelog_items)
    lines += _section_observations(blog_posts, jobs, changelog_items)

    return "\n".join(lines)


def _section_blog_posts(posts):
    lines = ["## 🆕 New Blog Posts", ""]
    if not posts:
        lines.append("No new blog posts detected this week.")
        lines.append("")
        return lines

    for post in posts:
        comp = post.get("competitor", "")
        title = post.get("title", "(untitled)")
        link = post.get("link", "")
        summary = post.get("summary", "")
        date = post.get("published", "")

        header = f"**{comp}**: [{title}]({link})" if link else f"**{comp}**: {title}"
        if date:
            header += f" ({date})"
        lines.append(f"- {header}")
        if summary:
            lines.append(f"  - {summary}")

    lines.append("")
    return lines


def _section_jobs(jobs):
    lines = ["## 💼 New Job Postings", ""]
    if not jobs:
        lines.append("No new job postings detected.")
        lines.append("")
        return lines

    for job in jobs:
        comp = job.get("competitor", "")
        title = job.get("title", "")
        team = job.get("team", "")
        location = job.get("location", "")
        url = job.get("url", "")

        parts = [f"**{comp}**"]
        if url:
            parts.append(f"[{title}]({url})")
        else:
            parts.append(title)
        if team:
            parts.append(f"({team})")
        if location:
            parts.append(f"— {location}")

        lines.append(f"- {' '.join(parts)}")

    lines.append("")
    return lines


def _section_changelog(items):
    lines = ["## 📦 Product Changes", ""]
    if not items:
        lines.append("No new changelog entries detected.")
        lines.append("")
        return lines

    for item in items:
        comp = item.get("competitor", "")
        title = item.get("title", "")
        date = item.get("date", "")
        desc = item.get("description", "")

        header = f"**{comp}**: {title}"
        if date:
            header += f" ({date})"
        lines.append(f"- {header}")
        if desc:
            lines.append(f"  - {desc}")

    lines.append("")
    return lines


def _section_observations(blog_posts, jobs, changelog_items):
    """Generate strategic observations based on simple pattern detection."""
    lines = ["## 🔍 Strategic Observations", ""]
    observations = []

    if len(jobs) >= 5:
        from collections import Counter
        teams = Counter(j.get("team", "unknown") for j in jobs if j.get("team"))
        if teams:
            top_team, count = teams.most_common(1)[0]
            observations.append(
                f"Heavy hiring detected: **{count}** new roles in **{top_team}** across competitors."
            )

    if len(blog_posts) >= 3:
        from collections import Counter
        comps = Counter(p.get("competitor", "") for p in blog_posts)
        top_comp, count = comps.most_common(1)[0]
        if count >= 3:
            observations.append(
                f"**{top_comp}** published **{count}** blog posts this week — may indicate a launch or campaign."
            )

    if len(changelog_items) >= 3:
        observations.append(
            f"**{len(changelog_items)}** product updates detected across competitors — high shipping velocity."
        )

    if not observations:
        observations.append("No strong patterns detected this week. Continue monitoring.")

    for obs in observations:
        lines.append(f"- {obs}")

    lines.append("")
    return lines
