---
name: engagelab-otp-verify
description: Verifies OTP codes that users entered, when EngageLab generated and stored the code (platform-generated mode). Use when checking whether a user-typed verification code matches the one EngageLab sent, completing the login/registration/2FA flow. This skill is only needed for platform-generated mode — if you generated the code yourself, verify it against your own database.
license: MIT
metadata:
  author: engagelab
  version: "1.0"
  docs: https://www.engagelab.com/zh_CN/docs/otp/REST-API/OTP-Check
---

# EngageLab OTP — Verify

Verifies a code the user entered against the one EngageLab generated and sent. **Only applies to platform-generated mode** (when you used `send()` not `sendCustom()`).

## When to use this skill

```
You called send()                    →  use this skill to verify
You called sendCustom()              →  do NOT use; verify against your own DB
```

## Quick decision

The user typed a code. You have the `message_id` you stored from the send step. Call verify, branch on `verified`.

## Endpoint

```
POST https://otp.api.engagelab.cc/v1/verifications

{
  "message_id":  "<from send() response>",
  "verify_code": "<what the user typed>"
}
```

## Node.js

```js
const { OTPClient, EngagelabError } = require('engagelab-otp');
const otp = new OTPClient(process.env.ENGAGELAB_DEV_KEY, process.env.ENGAGELAB_DEV_SECRET);

try {
  const { verified } = await otp.verify(storedMessageId, userTypedCode);

  if (verified) {
    // ✓ Authentication passed — invalidate the message_id immediately
    await session.markAuthenticated();
    await deleteFromStore(storedMessageId);
  } else {
    // ✗ Wrong code — let the user try again (track attempts!)
    await incrementFailedAttempts();
  }
} catch (err) {
  if (err instanceof EngagelabError && err.code === 3003) {
    // Code has expired or was already used → ask user to request a new OTP
    await sendNewOtp();
  } else {
    throw err;
  }
}
```

## Python

```python
from engagelab_otp import OTPClient, EngagelabError

otp = OTPClient(os.environ["ENGAGELAB_DEV_KEY"], os.environ["ENGAGELAB_DEV_SECRET"])

try:
    check = otp.verify(stored_message_id, user_typed_code)
    if check["verified"]:
        # ✓ Passed
        mark_authenticated()
    else:
        # ✗ Wrong code
        increment_failed_attempts()
except EngagelabError as e:
    if e.code == 3003:
        send_new_otp()  # Expired or already verified
    else:
        raise
```

## REST

```bash
curl -X POST https://otp.api.engagelab.cc/v1/verifications \
  -H "Authorization: Basic $(echo -n $KEY:$SECRET | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id":  "1725407449772531712",
    "verify_code": "123456"
  }'
```

## Response

```json
{
  "message_id":  "1725407449772531712",
  "verify_code": "123456",
  "verified":    true
}
```

`verified` is the only field you should branch on.

## Critical rules

```
1. ALWAYS verify server-side. Never trust a client claim of "verified".

2. Invalidate message_id after a successful verify.
   Otherwise replay attacks succeed.

3. Limit retry attempts (typically 5).
   Otherwise brute force succeeds.

4. Don't tell the user whether the code or the message_id is wrong.
   Return a generic "verification failed" to attacker-facing surfaces.

5. After 3003 (expired), require user to request a new OTP — do not loop.
```

## Sandbox

Sandbox mode (`dev_key=sandbox_demo`):

| Sandbox message_id source | verify_code | Result |
|---------------------------|-------------|--------|
| Any message_id from sandbox sends to `+10000000005` | `123456` | `verified: true` |
| Any message_id from sandbox sends to `+10000000005` | anything else | `verified: false` |
| Any sandbox message_id used twice | any | code `3003` (already used) |
| Sandbox message_id older than 5 min | any | code `3003` (expired) |

## When NOT to use this skill

- You called `sendCustom()` (you generated the code) → check against your own DB
- You want to know IF a message was delivered → use `engagelab-otp-webhook` skill
- You want to send a new code → use `engagelab-otp-send` skill
