"""Local JSON cache for tracking previously seen content."""

import json
from pathlib import Path


CACHE_FILE = Path(__file__).parent / "cache.json"


def load_cache():
    """Load the cache from disk, or return an empty dict."""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    """Persist the cache to disk."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def diff_entries(cache, source_key, current_entries, key="title"):
    """Compare current entries against the cache and return only new ones.

    Also updates the cache in-place with the current entries.
    """
    previously_seen = set(cache.get(source_key, []))
    current_keys = [entry.get(key, "") for entry in current_entries if entry.get(key)]

    new_entries = [
        entry for entry in current_entries
        if entry.get(key, "") and entry.get(key, "") not in previously_seen
    ]

    cache[source_key] = list(set(list(previously_seen) + current_keys))

    return new_entries
