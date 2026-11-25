---
name: browser-session
description: Lease one ordinary remote browser with standard CDP access for 10, 30, or 60 minutes through Ausca.
---

# Ausca Browser Session

Use this service when an agent already knows how to drive CDP, Playwright, or
Puppeteer and needs a short-lived remote browser without creating an account.
It is browser infrastructure, not a browser agent.

## What the purchase includes

One purchase creates one browser lease. Choose the duration; the prices are:

- 10 minutes (`duration_seconds: 600`): $0.05 USD
- 30 minutes (`1800`): $0.10 USD
- 60 minutes (`3600`): $0.20 USD

Status, CDP connection creation, and close do not charge again.

The service does not provide actions, extraction, crawling, recording,
persistent profiles, proxies, stealth, CAPTCHA solving, or a target-success
promise.

## Buy a session

The create input names one lease:

```json
{
  "duration_seconds": 600
}
```

Invoke `ausca/browser-session` with its `create` runner through your skill
runtime. The runtime prices the call from this skill's offer, asks for
approval, and pays Ausca. Ausca provisions the session and returns its public
lease: `session_id`, `state`, `created_at` and `expires_at`. There are no
other browser options.

Your skill runtime keeps the session's capability for whoever bought it: it
never appears in a result, a prompt or a receipt. A lost answer is recovered by running the
same purchase again under its run id; never start a new purchase to recover
one.

A purchase whose run fails, or never starts, is refunded; the purchase then
reports `failure.code` and `failure.message`.

## Close the session

Run `ausca/browser-session close` with `{ "session_id": ... }` to close a
session you hold early; the runtime then holds nothing for it. It is free, and close
is idempotent, including after a terminal state. Otherwise the hard expiry
cleans the session up.

## Drive the browser

CDP connections are minted with the capability. A buyer with no account
names a `buyer_key` with its purchase, and that key owns the session: once
the purchase is fulfilled, the key claims the capability from the runtime that
sold it, signed over the purchase receipt's digest. A buyer through ausca.com
receives it in the paid answer. Keep the capability in host-controlled secret
state: never in a prompt, log, receipt, query string, or later model-authored
tool argument. Then supply `Authorization: Bearer <capability>` from the host
boundary:

1. `GET /v1/browser-sessions/{session_id}` for status and hard expiry.
2. `POST /v1/browser-sessions/{session_id}/connections` with a stable
   `Idempotency-Key` to mint a short-lived CDP WebSocket ticket.
   This HTTP request has **no JSON body**, not even `{}`. The capability and
   idempotency key are headers, not body fields.
3. Read `connection.websocket_url` and connect to that
   `wss://browser.ausca.com/...` URL using an ordinary
   CDP client.
4. `DELETE /v1/browser-sessions/{session_id}` to close early, or allow the hard
   expiry to clean it up.

Only one CDP connection may be live at once. Connection tickets last 60 seconds,
are single-use, and at most 64 unexpired tickets may coexist. Expired records
are compacted, so reconnects do not consume a lifetime quota. Use a stable
connection `Idempotency-Key` to recover the same intended ticket; a different
key means a new ticket issue. Each CDP message is capped at 32 MiB. Status can
report a terminal lease, but connect requires `ready`.

`ticket_issued` means a credential was issued, not that Chromium connected.
Only a successful CDP handshake proves connection. Use
`chromium.connectOverCDP(connection.websocket_url)` with Playwright, or
`puppeteer.connect({ browserWSEndpoint: connection.websocket_url })` with
Puppeteer. That URL contains a secret: never log it or include it in reports.

Cloudflare treats 10 minutes as an inactivity timeout, not the session's hard
lifetime. For a 30- or 60-minute lease, issue a CDP command at least once inside
each 10-minute idle window. Provider eviction, Chromium failure, or an idle
timeout can still end a browser before Ausca's maximum lease expiry; reconnect
failure never allocates or charges for a replacement silently.

A browser lease cannot be extended. Choose the required duration before
purchase. More browser time means a separately approved new session with new
state and authority; no cookies, storage, tabs, or profile data carry over.

Reuse the purchase idempotency identity only for the same intended lease. If the
paid response is uncertain, replay that exact purchase; never mint a second
payment identity. Changed duration or terms under an existing identity are a
conflict. Expiry, exhausted ticket issues, unavailable capacity, invalid
authority, and an unverifiable provider result or receipt are stop conditions,
not permission to bypass the lease path. A failed invocation reports
`failure.code` and `failure.message`; the payment is refunded.

Successful paid state returns `receipt_ref.public_url`, an immutable hash-only
proof of the service, public price, completion time, and receipt digest. It
contains no browser state, connection ticket, lease capability, or content
digest and is readable by anyone holding the unguessable URL, so share it
deliberately.

The active catalog revision and linked schemas are the machine authority. x402
uses its external V2 semantics; Ausca's internal contracts remain V1.

The [executable purchase and recovery examples](https://github.com/auscahq/ausca/tree/main/examples)
cover this offer. CLI requires `--idempotency-key`; local paid MCP tools require
`ausca_idempotency_key`. Save one unique key before purchase and reuse unchanged
input on recovery. A new key buys a new lease, even for identical input.
