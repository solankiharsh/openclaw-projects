"""Configuration loader — reads config.yaml and environment variables."""

import os
from pathlib import Path

import yaml


def load_config():
    """Load config.yaml and merge with environment variables."""
    config_path = Path(__file__).parent / "config.yaml"
    cfg = {}

    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}

    cfg["github_token"] = os.environ.get("GITHUB_TOKEN", "")
    cfg["google_service_account_json"] = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    cfg["clickup_api_token"] = os.environ.get("CLICKUP_API_TOKEN", "")
    cfg["gmail_credentials_json"] = os.environ.get("GMAIL_CREDENTIALS_JSON", "")
    cfg["telegram_bot_token"] = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    cfg["telegram_chat_id"] = os.environ.get("TELEGRAM_CHAT_ID", "")

    return cfg
