---
name: mailflat-send
description: Send DKIM-signed mail from a MailFlat address, with attachments and delivery tracking. Use when the agent has to reply, notify, or test an inbound pipeline.
---

# Sending mail with MailFlat

Mail leaves from your own inbox address, signed by our MTA. Useful in reverse too: point your inbound pipeline at a MailFlat address and check what it does with what arrives.

## Send

```python
# mail leaves from the inbox address, DKIM-signed by our own MTA
result = inbox.send(
    "someone@example.com",
    subject="Welcome",
    body="Plain text body",
    html="<p>Optional HTML body</p>",
    cc=["team@example.com"],          # written into the headers
    bcc=["archive@example.com"],      # in NO header, not even in its own copy
    attachments=["invoice.pdf"],      # a path: read and base64-encoded for you
)

# send() returns when the mail is ACCEPTED (HTTP 202), not when it is delivered:
# delivery runs on a queue. The response carries the id you follow it with.
print(result["message_id"], result["queued"])

from mailflat import SendFailedError, SendTimeoutError
try:
    sent = inbox.wait_until_sent(result["message_id"], timeout=120)
    print(sent.send_status)           # "sent" (or "unsigned" if DKIM was skipped)
except SendFailedError as e:
    print("permanently failed:", e)   # the queue gave up; it will not retry
except SendTimeoutError:
    # NOT a failure. The queue is still retrying. Sending again delivers it twice.
    print("still queued; check back or subscribe to the message.delivered webhook")

# attachments also take bytes you already hold
inbox.send("someone@example.com", attachments=[
    {"filename": "report.csv", "content": b"a,b\n1,2\n"},
])

# Attachment size and count depend on your plan. Free is deliberately small.
# Ask the API rather than hard-coding the numbers:
#   GET https://mailflat.net/api/plans → max_attachment_bytes · max_attachments
# Going over is rejected with the limit spelled out, not silently dropped.
```

```javascript
// mail leaves from the inbox address, DKIM-signed by our own MTA
const result = await inbox.send("someone@example.com", {
  subject: "Welcome",
  body: "Plain text body",
  html: "<p>Optional HTML body</p>",
  cc: ["team@example.com"],          // written into the headers
  bcc: ["archive@example.com"],      // in NO header, not even in its own copy
  attachments: [
    { filename: "invoice.pdf", content: pdfBytes },      // Uint8Array
    { filename: "note.txt", contentBase64: "aGVsbG8=" }, // or base64 you already have
  ],
});

// send() resolves when the mail is ACCEPTED (HTTP 202), not when it is delivered:
// delivery runs on a queue. The response carries the id you follow it with.
console.log(result.message_id, result.queued);

import { SendFailedError, SendTimeoutError } from "@mailflat/sdk";
try {
  const sent = await inbox.waitUntilSent(result.message_id, { timeout: 120_000 });
  console.log(sent.sendStatus);      // "sent" (or "unsigned" if DKIM was skipped)
} catch (err) {
  if (err instanceof SendFailedError) {
    console.log("permanently failed:", err.message);   // the queue gave up
  } else if (err instanceof SendTimeoutError) {
    // NOT a failure: the queue is still retrying. Sending again delivers it twice.
    console.log("still queued; or subscribe to the message.delivered webhook");
  }
}

// The SDK takes bytes, never a file path: it also runs in the browser, where there
// is no filesystem. In Node, read the file yourself:
//   attachments: [{ filename: "invoice.pdf", content: await readFile("invoice.pdf") }]
// Size and count depend on your plan. Read GET /api/plans instead of hard-coding.
```

## Core rules

- The call returns on **acceptance** (HTTP 202), not delivery. Delivery runs on a queue.
- Track the outcome with the returned `message_id`, or subscribe to the `message.delivered` and `message.failed` webhooks.
- A timeout while waiting for delivery is not a failure. Sending again is how you deliver the same mail twice.
- `bcc` appears in no header at all, not even in its own copy. `cc` is written into the headers.
- Attachment count and size depend on the plan. Read `max_attachments` and `max_attachment_bytes` from `GET /api/plans`; going over is refused with the limit named, never silently dropped.
- On the free plan, sending is limited to your own addresses until a domain is connected and verified. This is a sandbox rule, not a bug.
- Outgoing mail is scanned for spam signals. Nothing is blocked on our side today, but a message that scores badly will be treated badly by the receiver.
- MailFlat addresses are permanent; only the messages inside them expire. Nothing here is a throwaway address.

## API gotchas

1. **202 is success for the API, not for the recipient.** Treat it as queued.
2. **A permanent failure will not retry.** The queue gives up and says so; sending again is your decision, not ours.
3. **Headers you inject are validated.** A subject containing CRLF is refused rather than smuggled into the envelope.
4. **The free plan sandbox applies to agents too.** An agent key does not lift it; verifying a domain does.

## References

- [Testing your own inbound email handling](https://mailflat.net/docs/guides/sending-email)
- [Testing email attachments](https://mailflat.net/docs/guides/attachments)
- [Webhooks: push incoming email to your endpoint](https://mailflat.net/docs/webhooks)
- [Custom domains (BYOD): use your own domain](https://mailflat.net/docs/custom-domains)
- [Full documentation as one file](https://mailflat.net/llms-full.txt) - every page as plain markdown
- Any documentation page also serves raw markdown: add `.md` to its URL
