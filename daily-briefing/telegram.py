"""Send messages via Telegram Bot API."""

import os

import requests


def send_telegram_message(text):
    """Send a markdown-formatted message to the configured Telegram chat."""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    if not bot_token or not chat_id:
        raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in environment.")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # Telegram has a 4096-char limit per message; split if needed
    chunks = _split_message(text, max_len=4096)

    for chunk in chunks:
        resp = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": chunk,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True,
            },
            timeout=15,
        )
        resp.raise_for_status()


def _split_message(text, max_len=4096):
    """Split a long message into chunks that fit Telegram's limit."""
    if len(text) <= max_len:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break
        split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            split_at = max_len
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")

    return chunks
