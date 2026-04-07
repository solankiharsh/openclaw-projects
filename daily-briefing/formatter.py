"""Format all fetched data into a clean markdown briefing."""

from datetime import datetime, timezone


def build_briefing(events, prs, tasks, email):
    """Build the full markdown briefing from fetched data sections."""
    now = datetime.now()
    lines = [
        f"# Daily Briefing — {now.strftime('%A, %B %d %Y')}",
        "",
    ]

    lines += _section_schedule(events)
    lines += _section_prs(prs)
    lines += _section_tasks(tasks)
    lines += _section_email(email)
    lines += _section_priorities(events, prs, tasks)

    return "\n".join(lines)


def _section_schedule(events):
    lines = ["## 📅 Today's Schedule", ""]
    if not events:
        lines.append("No meetings scheduled today. Deep work day!")
        lines.append("")
        return lines

    for ev in events:
        start = _format_time(ev.get("start", ""))
        end = _format_time(ev.get("end", ""))
        summary = ev.get("summary", "(No title)")
        lines.append(f"**{start} – {end}** | {summary}")

        attendees = ev.get("attendees", [])
        if attendees:
            names = ", ".join(attendees[:5])
            suffix = f" (+{len(attendees) - 5} more)" if len(attendees) > 5 else ""
            lines.append(f"  - Attendees: {names}{suffix}")

        location = ev.get("location", "")
        if location:
            lines.append(f"  - Location: {location}")

        lines.append("")

    return lines


def _section_prs(prs):
    lines = ["## 🔀 Open PRs Needing Attention", ""]
    if not prs:
        lines.append("No open PRs across configured repos.")
        lines.append("")
        return lines

    lines.append("| Repo | Title | Author | Age |")
    lines.append("|------|-------|--------|-----|")
    for pr in sorted(prs, key=lambda p: p.get("age_days", 0), reverse=True):
        repo = pr.get("repo", "")
        title = pr.get("title", "")
        author = pr.get("author", "")
        age = pr.get("age_days", 0)
        url = pr.get("url", "")
        title_link = f"[{title}]({url})" if url else title
        lines.append(f"| {repo} | {title_link} | {author} | {age}d |")

    lines.append("")
    return lines


def _section_tasks(tasks):
    lines = ["## ✅ Priority Tasks", ""]
    if not tasks:
        lines.append("No tasks fetched from ClickUp.")
        lines.append("")
        return lines

    for task in tasks:
        priority = task.get("priority", "none")
        icon = {"urgent": "🔴", "high": "🟠", "normal": "🟡", "low": "🟢"}.get(priority, "⚪")
        name = task.get("name", "")
        status = task.get("status", "")
        lines.append(f"- {icon} **{name}** ({status})")

    lines.append("")
    return lines


def _section_email(email):
    lines = ["## 📧 Email Snapshot", ""]
    if not email or (isinstance(email, dict) and email.get("unread_count", 0) == 0):
        lines.append("Inbox zero — nice work!")
        lines.append("")
        return lines

    if isinstance(email, dict):
        lines.append(f"**{email['unread_count']}** unread emails")
        lines.append("")
        for i, subject in enumerate(email.get("top_subjects", []), 1):
            lines.append(f"{i}. {subject}")
        lines.append("")
    return lines


def _section_priorities(events, prs, tasks):
    """Heuristic-based top-3 priorities for the day."""
    lines = ["## 🎯 What's Most Important Today", ""]
    items = []

    now = datetime.now(timezone.utc)

    if events:
        for ev in events[:2]:
            items.append(f"Prepare for **{ev.get('summary', 'meeting')}**")

    stale_prs = [p for p in (prs or []) if p.get("age_days", 0) >= 3]
    if stale_prs:
        items.append(f"Review {len(stale_prs)} stale PR(s) — oldest is {stale_prs[0].get('age_days', '?')} days old")

    urgent_tasks = [t for t in (tasks or []) if t.get("priority") in ("urgent", "high")]
    for t in urgent_tasks[:2]:
        items.append(f"Complete **{t.get('name', 'task')}** ({t.get('priority')})")

    if not items:
        items.append("No critical items flagged — focus on deep work")

    for i, item in enumerate(items[:3], 1):
        lines.append(f"{i}. {item}")

    lines.append("")
    return lines


def _format_time(iso_str):
    """Extract HH:MM from an ISO datetime string, or return the date as-is."""
    if not iso_str:
        return "??:??"
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%H:%M")
    except ValueError:
        return iso_str
