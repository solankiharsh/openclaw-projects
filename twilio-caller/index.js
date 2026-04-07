'use strict';

require('dotenv').config();

const twilio = require('twilio');

const MESSAGE =
  'Good morning! This is HarshClaw, your AI assistant. ' +
  "Today is going to be a great day. " +
  "Check your Telegram for today's briefing.";

function loadConfig() {
  const required = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER'];
  const missing = required.filter((key) => !process.env[key]);

  if (missing.length > 0) {
    console.error(`Missing required environment variables: ${missing.join(', ')}`);
    console.error('Copy .env.example to .env and fill in your Twilio credentials.');
    process.exit(1);
  }

  return {
    accountSid: process.env.TWILIO_ACCOUNT_SID,
    authToken: process.env.TWILIO_AUTH_TOKEN,
    fromNumber: process.env.TWILIO_PHONE_NUMBER,
  };
}

function validatePhoneNumber(number) {
  const e164 = /^\+[1-9]\d{1,14}$/;
  if (!e164.test(number)) {
    console.error(`Invalid phone number: "${number}"`);
    console.error('Phone number must be in E.164 format (e.g., +14155551234).');
    process.exit(1);
  }
  return number;
}

async function makeCall(config, toNumber) {
  const client = twilio(config.accountSid, config.authToken);

  const twiml = `<Response><Say voice="Polly.Matthew">${MESSAGE}</Say></Response>`;

  console.log(`Calling ${toNumber} from ${config.fromNumber}...`);

  const call = await client.calls.create({
    twiml,
    to: toNumber,
    from: config.fromNumber,
  });

  console.log(`Call initiated successfully.`);
  console.log(`  Call SID : ${call.sid}`);
  console.log(`  Status   : ${call.status}`);
  console.log(`  To       : ${call.to}`);
  console.log(`  From     : ${call.from}`);

  return call;
}

async function main() {
  const targetNumber = process.argv[2];

  if (!targetNumber) {
    console.error('Usage: npm run call -- +14155551234');
    console.error('       node index.js +14155551234');
    process.exit(1);
  }

  const config = loadConfig();
  const toNumber = validatePhoneNumber(targetNumber);

  try {
    await makeCall(config, toNumber);
  } catch (err) {
    if (err.code) {
      console.error(`Twilio error [${err.code}]: ${err.message}`);
    } else {
      console.error(`Unexpected error: ${err.message}`);
    }
    process.exit(1);
  }
}

main();
