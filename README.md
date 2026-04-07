# 🦀 OpenClaw Projects by HarshClaw

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-20+-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)](https://nodejs.org)
[![Built with OpenClaw](https://img.shields.io/badge/Built%20with-OpenClaw-FF6B35?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJ3aGl0ZSI+PHBhdGggZD0iTTEyIDJMMyA3djEwbDkgNSA5LTV2LTEweiIvPjwvc3ZnPg==)](https://github.com/solankiharsh/openclaw-projects)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

A collection of automation tools and workflows built with [OpenClaw](https://github.com/solankiharsh/openclaw-projects), demonstrating practical use cases for engineering leaders who want to automate their daily operations.

---

## Projects

### 📞 [Twilio Caller](./twilio-caller)

A Node.js script that makes outbound phone calls using the Twilio API with text-to-speech messages. Perfect for automated morning wake-up calls, reminders, or alerts that need to cut through notification noise and reach you by voice.

| | |
|---|---|
| **Tech Stack** | Node.js, Twilio SDK, dotenv |
| **Use Case** | Automated phone call reminders and alerts |
| **Setup** | [Instructions →](./twilio-caller/README.md) |

<!-- Screenshot placeholder: ![Twilio Caller](./assets/twilio-caller-screenshot.png) -->

---

### 📋 [Daily Briefing Generator](./daily-briefing)

A Python CLI tool that aggregates data from Google Calendar, GitHub, ClickUp, and Gmail into a single formatted morning briefing. It pulls your schedule, open PRs, priority tasks, and email snapshot — then uses smart heuristics to highlight the three most important items for your day. Optionally delivers the briefing straight to Telegram.

| | |
|---|---|
| **Tech Stack** | Python, Click, Google APIs, PyGithub, Telegram Bot API |
| **Use Case** | Automated daily executive briefing |
| **Setup** | [Instructions →](./daily-briefing/README.md) |

<!-- Screenshot placeholder: ![Daily Briefing](./assets/daily-briefing-screenshot.png) -->

---

### 🔍 [Stale PR Scanner](./stale-pr-scanner)

A Python tool that scans your GitHub repositories for pull requests that have been open longer than 48 hours, categorizes them by review status (waiting, changes requested, approved but unmerged, in progress), and sends a formatted report via Telegram. Designed to run as a weekday cron job so nothing slips through the cracks.

| | |
|---|---|
| **Tech Stack** | Python, PyGithub, PyYAML, Telegram Bot API |
| **Use Case** | Automated PR hygiene and review tracking |
| **Setup** | [Instructions →](./stale-pr-scanner/README.md) |

<!-- Screenshot placeholder: ![Stale PR Scanner](./assets/stale-pr-scanner-screenshot.png) -->

---

### 🕵️ [Competitive Intelligence Monitor](./competitive-intel)

A Python scraper that monitors competitor engineering blogs (via RSS), careers pages, and product changelogs. It compares each scan against a local cache to surface only what's new, then generates a structured weekly intelligence brief with observations on hiring trends, technical direction, and product velocity. Delivers via Telegram.

| | |
|---|---|
| **Tech Stack** | Python, BeautifulSoup4, feedparser, PyYAML, Telegram Bot API |
| **Use Case** | Automated competitive landscape monitoring |
| **Setup** | [Instructions →](./competitive-intel/README.md) |

<!-- Screenshot placeholder: ![Competitive Intel](./assets/competitive-intel-screenshot.png) -->

---

## Getting Started

Each project is self-contained with its own dependencies, configuration, and documentation. To get started with any project:

1. Navigate to the project directory
2. Copy `.env.example` to `.env` and fill in your API keys
3. Install dependencies (`npm install` for Node.js, `pip install -r requirements.txt` for Python)
4. Follow the project-specific README for detailed setup

## Project Structure

```
openclaw-projects/
├── twilio-caller/          # Outbound phone call automation
├── daily-briefing/         # Morning briefing aggregator
├── stale-pr-scanner/       # GitHub PR hygiene monitor
├── competitive-intel/      # Competitor tracking scraper
└── README.md               # This file
```

## Author

**HarshClaw** — Engineering automation for leaders who ship.

---

<p align="center">Built with 🦀 OpenClaw</p>
