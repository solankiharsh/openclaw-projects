# 🔍 Stale PR Scanner

A Python tool that scans your GitHub repositories for pull requests open longer than 48 hours, categorizes them by review status, and sends a formatted report via Telegram. Designed to run as a weekday cron job.

## Categories

Each stale PR is classified into one of four categories:

| Category | Meaning |
|----------|---------|
| **Waiting for review** | No reviews or comments yet |
| **Changes requested** | A reviewer has requested changes |
| **Approved, not merged** | Approved but still sitting open |
| **Review in progress** | Has comments or partial reviews |

## Prerequisites

- Python 3.11+
- A GitHub [personal access token](https://github.com/settings/tokens) with `repo` scope

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure credentials
cp .env.example .env
# Edit .env with your GitHub token and Telegram credentials

# Configure repositories
# Edit config.yaml with your repo list
```

## Usage

```bash
# Run the scanner
python main.py

# Enable Telegram delivery by setting telegram.enabled: true in config.yaml
```

## Configuration

Edit `config.yaml`:

```yaml
repositories:
  - "your-org/backend"
  - "your-org/frontend"
  - "your-org/infra"

stale_threshold_hours: 48

telegram:
  enabled: true
```

## Cron Job Setup

Add to your crontab (`crontab -e`) to run every weekday at 9:00 AM:

```cron
0 9 * * 1-5 cd /path/to/stale-pr-scanner && /usr/bin/python3 main.py >> /var/log/stale-pr-scanner.log 2>&1
```

## Rate Limiting

The scanner is rate-limit aware. It checks GitHub's `X-RateLimit-Remaining` header before each repository scan and automatically sleeps until the reset window if the limit drops below 50 remaining requests.

## Sample Output

See [sample_output.md](./sample_output.md) for an example report.

## License

MIT
