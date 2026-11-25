---
name: wiring-webhooks
description: Use when a system rather than a person needs to know what a jury decided — releasing an escrow when a case closes, updating a record on each vote, replacing a polling loop, or integrating Tribeunal into a service. Covers registering an endpoint in the right order, verifying that a delivery is genuine, which events mislead, and what to do without a rotate tool.
---

# Wiring webhooks

A webhook turns waiting into being told. The cost is that you now have to prove each delivery is
really from Tribeunal, and the signing secret you need for that is shown exactly once.

## When to use

When something automated must react to a case. A person watching an outcome wants
`acting-on-verdicts` instead; long-polling is simpler and needs no public address.

## Checklist

- [ ] Register the endpoint **before** the case exists
- [ ] Store the secret from the create response immediately
- [ ] Subscribe to the events you actually handle
- [ ] Verify signature and timestamp on every delivery
- [ ] Deduplicate on the delivery id
- [ ] Answer 2xx fast, then do the work
- [ ] Change the event list or pause delivery with `tribeunal_update_webhook`, never by deleting

## Order matters

Create the endpoint first, then the case. The secret is returned once, at creation, and cannot be
read back — `tribeunal_list_webhooks` shows the endpoint but never the secret again. Register after
the case has opened and the first events either arrive unverifiable or arrive before you were
listening.

So: `tribeunal_create_webhook`, capture the secret, *then* `tribeunal_create_case`.

Tell whoever asked that the secret is shown once and must be stored now. An agent that reports "set
up" without surfacing the secret has produced an endpoint nobody can verify.

## Signature

Each delivery carries a timestamp and a signature header. The signature is
`hmac_sha256(secret, "{X-Tribeunal-Timestamp}.{raw body bytes}")`, hex, prefixed `v1=`.

Three details decide whether a verifier works:

- **Raw bytes.** Verify against the body exactly as received. Parsing the JSON and re-serialising it
  reorders keys and changes whitespace, so a genuine delivery fails — this is the usual cause of "my
  receiver rejects everything".
- **Constant-time comparison.** A byte-by-byte early exit turns the verifier into an oracle.
- **Check the timestamp.** A signature stays valid forever, so a replayed delivery passes the digest
  check. Reject anything outside a few minutes.

`scripts/verify-signature.js` does all three. Run it against a real delivery to confirm your
plumbing before writing your own:

```
node scripts/verify-signature.js --secret "$SECRET" \
  --timestamp 1788428724 --signature "v1=3f1b86…" --body ./delivery.json
```

It prints `VALID` or `INVALID` and exits 0 or 1.

## Events

`references/events.md` lists every event, the headers, and the receiver contract. Two are worth
knowing before you read it:

- **`ping` ignores your subscriptions.** It proves reachability and signing, never that your event
  list is right. A perfect ping on an endpoint subscribed to nothing still succeeds.
- **A vote's rationale rides inside `vote.cast`.** It does not also raise `comment.created`, so a
  receiver watching only comments silently misses every reason anyone gave.

## Deliveries repeat

Delivery is at-least-once: the same event can arrive twice. Record the delivery id before acting and
ignore an id you have already seen. Without that, "release the escrow" runs twice.

Answer 2xx quickly and do the work afterwards. A receiver that finishes first looks slow, gets
treated as failed, and is retried — creating the duplicate it was trying to avoid.

## Changing an endpoint

`tribeunal_update_webhook` changes `events` and/or `active` on an existing endpoint — pause delivery
without losing the subscription list, or narrow/widen which events fire, at least one field. That is
all it touches: the URL and the signing secret are not editable through this tool, on any transport,
by design (repointing the URL or minting a fresh secret is a bigger capability than this tool grants).
To change either, delete the endpoint and create a new one — see below for what that costs you.

## No rotate tool

There is no rotate and no ping over these tools — deliberately, since both are ways to escalate a
read into a write. If a secret is compromised, or the URL needs to move:

1. The REST API can rotate it, keeping the endpoint and its subscriptions.
2. Or delete the endpoint and create a new one, which mints a fresh secret.

The second option has a gap: between the delete and the create, events are dropped and not retried.
Say so rather than silently losing deliveries. Deleting also destroys the old secret, so anything
mid-flight becomes unverifiable.

## Local receivers

URLs must be https and publicly resolvable — the server rejects private, loopback and CGNAT
addresses, so a laptop receiver needs a tunnel with a public hostname. There is no bypass, and the
guard is protecting the platform from being pointed at internal networks rather than inconveniencing
you.

## Gotchas

| Trap | What is true |
| --- | --- |
| The secret can be fetched later | Shown once at creation, never again |
| A successful ping means events will flow | `ping` ignores subscriptions entirely |
| `case.closed` means a decision was made | It can carry no ruling at all |
| One event, one delivery | At-least-once; deduplicate on the delivery id |
| Verifying the parsed JSON is equivalent | Re-serialising breaks the digest; use raw bytes |
| A vote comment raises `comment.created` | It rides inside `vote.cast` |
| `tribeunal_update_webhook` can repoint the URL or mint a new secret | It only changes `events` and `active`; delete and recreate for either |
