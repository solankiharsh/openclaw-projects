"""Fetch priority tasks from ClickUp."""

import requests


CLICKUP_API_BASE = "https://api.clickup.com/api/v2"


def fetch_priority_tasks(cfg):
    """Return a list of dicts with top tasks from the configured ClickUp list.

    Each dict: {name, status, priority, url}
    """
    token = cfg.get("clickup_api_token", "")
    list_id = cfg.get("clickup_list_id", "")

    if not token or not list_id:
        return []

    headers = {"Authorization": token}
    params = {
        "order_by": "priority",
        "reverse": "true",
        "subtasks": "true",
        "statuses[]": ["to do", "in progress"],
    }

    resp = requests.get(
        f"{CLICKUP_API_BASE}/list/{list_id}/task",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    tasks = []
    for task in data.get("tasks", [])[:10]:
        priority = task.get("priority")
        priority_label = priority.get("priority", "none") if priority else "none"
        tasks.append(
            {
                "name": task.get("name", ""),
                "status": task.get("status", {}).get("status", ""),
                "priority": priority_label,
                "url": task.get("url", ""),
            }
        )

    return tasks
