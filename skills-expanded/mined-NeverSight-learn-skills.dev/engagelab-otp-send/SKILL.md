---
name: engagelab-otp-send
description: Sends OTP verification codes via EngageLab using SDK or REST API. Use when implementing phone or email verification, login authentication, two-factor authentication, account registration, password reset flows, or any workflow that requires sending a one-time code. Supports both platform-generated codes and caller-generated codes, across SMS, WhatsApp, Voice, and Email channels with automatic fallback.
license: MIT
metadata:
  author: engagelab
  version: "1.0"
  docs: https://www.engagelab.com/zh_CN/docs/OTP/Product-Overview
allowed-tools: Bash Read
---

# EngageLab OTP — Send

Sends OTP codes to phone numbers or email addresses via EngageLab. Two send modes are supported; pick the right one based on whether the caller wants to control the code value.

## Quick decision

```
You want EngageLab to generate, send, and store the code
  → use platform mode: client.send(...)

You generate the code yourself (you store it in your DB)
  → use custom mode: client.sendCustom(...)
```

## Try without signing up

If the user wants to try before creating an account, use the public sandbox.

```
ENGAGELAB_DEV_KEY=sandbox_demo
ENGAGELAB_DEV_SECRET=sandbox_secret
Template ID: sandbox-otp-tpl
```

Sandbox does NOT send real messages. It returns realistic responses and triggers webhooks. See "Sandbox magic numbers" at the bottom of this file to test specific scenarios.

## Setup

```bash
# Node.js
npm install engagelab-otp

# Python
pip install engagelab-otp
```

Credentials live in environment variables — never hardcode:

```
ENGAGELAB_DEV_KEY=your_dev_key
ENGAGELAB_DEV_SECRET=your_dev_secret
```

Get production credentials at https://www.engagelab.com.

## Platform-generated code mode (recommended)

EngageLab generates a random code, sends it, and stores it for verification. You only call `verify()` later with what the user typed.

### Node.js

```js
const { OTPClient } = require('engagelab-otp');
const otp = new OTPClient(process.env.ENGAGELAB_DEV_KEY, process.env.ENGAGELAB_DEV_SECRET);

const { message_id, send_channel } = await otp.send(
  '+6591234567',           // E.164 phone or email
  'your-template-id',
  { name: 'Alice' },       // optional template variables
  'en'                     // language: default | zh_CN | zh_HK | en | ja | th | es
);
// Store message_id server-side (session, Redis, DB) for the verify step.
```

### Python

```python
from engagelab_otp import OTPClient
otp = OTPClient(os.environ["ENGAGELAB_DEV_KEY"], os.environ["ENGAGELAB_DEV_SECRET"])

result = otp.send(
    "+6591234567",
    "your-template-id",
    params={"name": "Alice"},
    language="en",
)
# result["message_id"], result["send_channel"]
```

### REST (any language)

```bash
curl -X POST https://otp.api.engagelab.cc/v1/messages \
  -H "Authorization: Basic $(echo -n $KEY:$SECRET | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+6591234567",
    "template": { "id": "your-template-id", "language": "en", "params": {} }
  }'
```

## Custom code mode (you supply the code)

Use when you need the code in your own database (e.g. for offline verification, custom expiry rules, multi-channel cross-validation).

### Node.js

```js
const crypto = require('crypto');
const code = String(crypto.randomInt(100000, 1000000));   // 6-digit

await otp.sendCustom(
  '+6591234567',
  'your-custom-template-id',
  { code, name: 'Alice' }
);
// Store `code` server-side, with TTL.
```

### Python

```python
import secrets
code = f"{secrets.randbelow(1_000_000):06d}"

otp.send_custom(
    "+6591234567",
    "your-custom-template-id",
    {"code": code, "name": "Alice"},
)
```

`to` accepts a string or a list for multi-recipient sends. For per-recipient codes, loop and call `sendCustom`/`send_custom` once per recipient.

## Phone number format

Always E.164: `+` followed by country code and subscriber number, no spaces or dashes.

| Country     | Example         |
|-------------|-----------------|
| Singapore   | +6591234567     |
| Malaysia    | +60123456789    |
| Indonesia   | +6281234567890  |
| Pakistan    | +923001234567   |
| China       | +8618601234567  |

Strip local prefixes (e.g. leading `0`) before sending. Invalid formats return error `5011`.

## Error handling

```js
const { EngagelabError } = require('engagelab-otp');

try {
  await otp.send('+6591234567', 'tpl-id', {});
} catch (err) {
  if (err.retryable) {
    // HTTP 429/5xx or API codes 1000 / 5001 / 5016 → backoff and retry
  } else {
    // Permanent: bad credentials, invalid number, blacklisted, etc.
  }
}
```

For the full error code → action mapping, see [references/ERRORS.md](references/ERRORS.md).

## Sandbox magic numbers

When using sandbox credentials, these recipient values trigger specific scenarios:

| Recipient                 | Behavior |
|---------------------------|----------|
| `+10000000000`            | Always succeeds, returns `delivered` webhook after 2s |
| `+10000000001`            | Fails with code `5011` (invalid number) |
| `+10000000002`            | Fails with code `5012` (unreachable) |
| `+10000000003`            | Succeeds but never delivers (simulates lost SMS) |
| `+10000000004`            | Triggers WhatsApp → SMS fallback sequence |
| `+10000000005`            | Succeeds; correct verify code is `123456` |
| `sandbox@example.com`     | Always succeeds via email channel |

Sandbox cost: free, no daily quota for the first 500 requests/day.

## Security checklist

- Always verify server-side — never trust a client-side "I verified" claim
- Set a retry limit (e.g. 5 attempts) before locking the user out
- Use HTTPS everywhere
- Expire `message_id` from your store after successful verification
- For platform mode, the code is never exposed to your backend — only `verified: true/false`

## When NOT to use this skill

- For sending marketing or transactional SMS that is not a verification code → use `engagelab-sms` skill instead
- For verifying a code the user entered → use `engagelab-otp-verify` skill
- For processing delivery callbacks → use `engagelab-otp-webhook` skill
