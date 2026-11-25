---
name: mailflat
description: Create real, permanent email inboxes from code and read what lands in them. Use when an agent needs its own email address, a verification code, or an end-to-end test of a signup flow.
---

# MailFlat

Real email inboxes you open from code. Mail actually travels: SMTP, DKIM, the lot, so a broken template or a misconfigured sender fails here exactly as it would in production.

The inbox and its address are permanent: they stay until you delete them. Only the messages inside expire, on a retention window set by the plan. This is not a throwaway address service.

## Install

```bash
pip install mailflat   # Python
npm i @mailflat/sdk    # JavaScript and TypeScript
```

## Quick start

```python
import os
from mailflat import MailFlat

mf = MailFlat(api_key=os.environ["MAILFLAT_API_KEY"])

# 1. a real, deliverable address
#    prefix = the local part of the address. label is a display name only.
inbox = mf.create(prefix="signup")
print(inbox.address)            # signup@a7f2c.mailflat.net

# 2. your app sends the code to that address
my_app.register(email=inbox.address)

# 3. read it back, no mocking anywhere
otp = inbox.wait_for_otp(timeout=30)
print(otp)                      # "482913"

# 4. done with it
inbox.delete()
```

```javascript
import { MailFlat } from "@mailflat/sdk";

const mf = new MailFlat({ apiKey: process.env.MAILFLAT_API_KEY });

// 1. a real, deliverable address
//    prefix = the local part of the address. label is a display name only.
const inbox = await mf.create({ prefix: "signup" });
console.log(inbox.address);          // signup@a7f2c.mailflat.net

// 2. your app sends the code to that address
await myApp.register({ email: inbox.address });

// 3. read it back, no mocking anywhere
const otp = await inbox.waitForOtp({ timeout: 30000 });
console.log(otp);                    // "482913"

// 4. done with it
await inbox.delete();
```

## Core rules

- Every call to `https://mailflat.net/api/v1` carries `X-API-Key: mf_live_...`. Keep the key in an environment variable, never in the repo.
- Getting a key needs a human once: MailFlat is in invited early access, so public sign-up is not open. Request access at https://mailflat.net/signup, then create the key under Agents -> API keys. An agent cannot issue itself a key today.
- The address comes from `prefix`, not `label`. `label` is a display name only, it never appears in the address.
- Poll no faster than every 2-3 seconds, and always pass a timeout. A poll loop without a deadline turns a missing email into a hung job.
- One-time codes are extracted server-side and handed to you as a field. Never write a regex over the message body.
- Open one inbox per test or per task. Parallel workers reading the same inbox will read each other's mail.
- Set `retention_hours` so an abandoned inbox cleans itself up even when your teardown never runs.
- Plan limits (quota, daily sends, attachment size) are not constants. Read them from `GET /api/plans` instead of hard-coding numbers.

## API gotchas

Each of these has bitten someone. They are not obvious from the method signatures.

1. **`prefix` builds the address, `label` does not.** `create(label="signup")` gives you a random local part and a display name. If you need `signup@...`, pass `prefix`.
2. **Timeout units differ by language.** The Python client takes seconds, the JavaScript client takes milliseconds. `timeout=30` and `timeout: 30` are not the same instruction.
3. **Sending answers 202, not 200.** The call returns when the mail is accepted, not when it is delivered. Follow `message_id`, or subscribe to the `message.delivered` webhook.
4. **A send timeout is not a send failure.** The queue is still retrying. Sending again delivers the message twice.
5. **Encrypted inboxes return `null` for body, headers and `otp_code`.** That is the design, not an outage: the server cannot read them. Inboxes created for agents are always plain text for this reason.
6. **On the free plan you can only send to your own addresses** until you connect and verify a domain. Sending anywhere else is refused, and the refusal says so.
7. **`spam` is `null` when a message was never scanned.** `null` is not the same as clean, and `0.0` is a real score.
8. **Attachments come back as metadata only.** The bytes live behind a separate endpoint, so listing an inbox never drags whole files through the response.
9. **Deleting a message is not deleting the inbox.** The address survives and stays yours; only its contents go.
10. **Do not mix credentials.** Account keys (`mf_live_...`) belong to `/api/v1`. The session API used by the web app takes a bearer token, and swapping them produces a confusing 401 on an otherwise correct request.

## What a message looks like

| Python | JavaScript | JSON field | What it is |
| --- | --- | --- | --- |
| `subject` | `subject` | `subject` | Subject line |
| `sender` | `sender` | `sender` | From address |
| `text` | `text` | `body_text` | Plain text body |
| `html` | `html` | `body_html` | HTML body |
| `otp` | `otp` | `otp_code` | One-time code, extracted by us |
| `to_address` | `toAddress` | `to_address` | The exact address it was sent to, tag included |
| `tag` | `tag` | `tag` | Plus-addressing tag, if the sender used one |
| `received_at` | `receivedAt` | `received_at` | When it landed |
| `is_encrypted` | `isEncrypted` | `is_encrypted` | True on end-to-end encrypted inboxes, where body and code are unavailable |

## References

- [Quickstart: create your first email inbox](https://mailflat.net/docs/quickstart)
- [Agent API and MCP reference](https://mailflat.net/docs/api/agent-api)
- [API keys and authentication](https://mailflat.net/docs/api-keys)
- [Troubleshooting email delivery, OTP and API errors](https://mailflat.net/docs/troubleshooting)
- [Full documentation as one file](https://mailflat.net/llms-full.txt) - every page as plain markdown
- Any documentation page also serves raw markdown: add `.md` to its URL
