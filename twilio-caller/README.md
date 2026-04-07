# 📞 Twilio Caller

A Node.js script that makes outbound phone calls using the Twilio API with a text-to-speech message. Designed for automated morning reminders, alerts, or any scenario where a voice call beats a push notification.

## Prerequisites

- [Node.js](https://nodejs.org/) 20+
- A [Twilio account](https://www.twilio.com/try-twilio) with:
  - Account SID and Auth Token
  - A purchased Twilio phone number
  - The target number verified (required for trial accounts)

## Setup

```bash
# Install dependencies
npm install

# Configure credentials
cp .env.example .env
# Edit .env with your Twilio credentials
```

## Usage

```bash
# Using the npm script
npm run call -- +14155551234

# Or directly
node index.js +14155551234
```

The phone number must be in [E.164 format](https://www.twilio.com/docs/glossary/what-e164) (e.g., `+14155551234`).

## What It Does

When you run the script, it:

1. Validates your Twilio credentials are configured
2. Validates the target phone number format
3. Places an outbound call via the Twilio API
4. Plays a text-to-speech message using Amazon Polly (Matthew voice):

   > *"Good morning! This is HarshClaw, your AI assistant. Today is going to be a great day. Check your Telegram for today's briefing."*

5. Prints the Call SID and status for tracking

## Environment Variables

| Variable | Description |
|---|---|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID (starts with `AC`) |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | Your Twilio phone number in E.164 format |

## Customizing the Message

Edit the `MESSAGE` constant at the top of `index.js` to change the spoken text. You can also change the voice by modifying the `voice` attribute in the TwiML `<Say>` element. See [Twilio's voice options](https://www.twilio.com/docs/voice/twiml/say#voice) for available voices.

## License

MIT
