---
name: mailflat-otp
description: Read one-time passcodes and verification links out of real email. Use when a signup, login or 2FA flow sends a code that the agent has to type back.
---

# One-time codes with MailFlat

The code is extracted as the message is stored and handed to you as a field. You wait for it; you do not parse it.

## Wait for a code

```python
# wait_for_otp polls /latest for you and raises instead of returning None
otp = inbox.wait_for_otp(timeout=30, poll_interval=1)

# need the whole message, not just the code?
msg = inbox.wait_for_message(timeout=30)
print(msg.subject, msg.sender, msg.text)

# both raise on timeout, so a missing email fails the test loudly
from mailflat import OTPTimeoutError
try:
    inbox.wait_for_otp(timeout=5)
except OTPTimeoutError as e:
    print("no code arrived:", e)

# Waiting for MANY codes at once? Use the async client. Twenty inboxes wait in
# one event loop instead of twenty parked threads.
import asyncio
from mailflat.aio import AsyncMailFlat

async def main():
    async with AsyncMailFlat() as mf:
        inboxes = await asyncio.gather(*(mf.create(label=f"run-{i}") for i in range(20)))
        codes = await asyncio.gather(*(i.wait_for_otp(timeout=60) for i in inboxes))
        print(codes)

asyncio.run(main())
```

```javascript
// timeout and pollInterval are MILLISECONDS here (the Python client uses seconds)
const otp = await inbox.waitForOtp({ timeout: 30000, pollInterval: 1000 });

// need the whole message?
const msg = await inbox.waitForMessage({ timeout: 30000 });
console.log(msg.subject, msg.sender, msg.text);

// both reject on timeout, so a missing email fails the test loudly
import { OTPTimeoutError } from "@mailflat/sdk";
try {
  await inbox.waitForOtp({ timeout: 5000 });
} catch (err) {
  if (err instanceof OTPTimeoutError) console.log("no code arrived");
}
```

## Core rules

- Always pass a timeout. Both clients raise or reject when it expires, which is what makes a missing email fail loudly instead of hanging.
- The Python client counts seconds, the JavaScript client counts milliseconds.
- Poll every 2-3 seconds. Faster does not make mail arrive sooner.
- Open the inbox **before** triggering the flow that sends the code. A code that arrives before you start waiting is still readable, but a race is easier to avoid than to debug.
- Need the whole message instead of just the digits? Use the wait-for-message call, then read `text`, `html` or `links`.
- Magic links are already parsed out: `links` holds every http(s) URL in order, de-duplicated, so you do not need a regex there either.
- An encrypted inbox cannot give you a code. The server holds ciphertext, so `otp_code` is `null` by design. Use a plain-text agent inbox for automation.
- MailFlat addresses are permanent; only the messages inside them expire. Nothing here is a throwaway address.

## API gotchas

1. **No code does not mean no mail.** If `otp_code` is `null` but a message arrived, the sender used a format we did not recognise as a code. Read `text` or `links` and treat it as a link flow.
2. **Timeouts are not retries.** Catching the timeout and immediately waiting again just doubles your deadline; find out why the mail is not arriving.
3. **One inbox per flow.** Two tests waiting on the same address can each read the other's code, and both will look correct until they do not.

## References

- [Extracting one-time codes from email](https://mailflat.net/docs/guides/otp-codes)
- [Waiting for email without flaky tests](https://mailflat.net/docs/guides/waiting-and-timeouts)
- [Extracting and testing links in email](https://mailflat.net/docs/guides/links)
- [Full documentation as one file](https://mailflat.net/llms-full.txt) - every page as plain markdown
- Any documentation page also serves raw markdown: add `.md` to its URL
