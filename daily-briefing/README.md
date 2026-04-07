# 📋 Daily Briefing Generator

A Python CLI tool that aggregates your calendar, GitHub PRs, ClickUp tasks, and Gmail into a single formatted morning briefing with AI-prioritized action items. Designed to run as a daily cron job with optional Telegram delivery.

## Prerequisites

- Python 3.11+
- API access for the services you want to include (all are optional — the tool gracefully skips unavailable sources)

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your credentials

# Configure repositories, ClickUp list, etc.
# Edit config.yaml
```

### Google Calendar Setup

1. Create a service account in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Google Calendar API
3. Download the service account JSON key
4. Share your calendar with the service account email
5. Set `GOOGLE_SERVICE_ACCOUNT_JSON` to the path of the key file

### Gmail Setup

1. Use the same service account with domain-wide delegation, or
2. Set up OAuth2 credentials for Gmail API access
3. Set `GMAIL_CREDENTIALS_JSON` to the credentials file path

### GitHub Setup

1. Create a [personal access token](https://github.com/settings/tokens) with `repo` scope
2. Set `GITHUB_TOKEN` in your `.env`
3. Add repos to monitor in `config.yaml`

### ClickUp Setup

1. Get your [API token](https://app.clickup.com/settings/apps)
2. Find your list ID (visible in the ClickUp URL)
3. Set both in `.env` and `config.yaml`

### Telegram Setup

1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get your chat ID by messaging the bot and checking `/getUpdates`
3. Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`

## Usage

```bash
# Print briefing to stdout
python main.py

# Save to a file
python main.py --output briefing.md

# Send via Telegram
python main.py --telegram

# Both
python main.py --telegram --output briefing.md
```

## Cron Job Setup

Add to your crontab (`crontab -e`) to run every weekday at 7:30 AM:

```cron
30 7 * * 1-5 cd /path/to/daily-briefing && /usr/bin/python3 main.py --telegram >> /var/log/daily-briefing.log 2>&1
```

## Sample Output

See [sample_output.md](./sample_output.md) for an example of what the briefing looks like.

## How Prioritization Works

The "What's Most Important Today" section uses these heuristics:

1. **Upcoming meetings** — first 2 calendar events get prep reminders
2. **Stale PRs** — PRs open 3+ days are flagged for review
3. **Urgent/high tasks** — ClickUp tasks with urgent or high priority

No LLM API required — keeps the tool self-contained and fast.

## License

MIT
