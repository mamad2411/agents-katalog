---
name: webhook-setup
description: Configure webhooks to receive inbound messages and delivery updates with signature verification.
---

# Webhook Setup

## When to Use

Use this skill when setting up webhook endpoints to receive inbound messages, delivery status updates, or template approval notifications from Zavu.

## Senders vs accounts (one paragraph)

A **Sender** is the API handle you pass as `Zavu-Sender`; **accounts** (a WhatsApp Business Account, a Facebook Page, a Telegram bot, a phone number) are the connections it routes — and what bills. Senders are free. Connecting an account in the dashboard auto-creates its sender; find it with `GET /v1/senders` and trust its `channels` array for what it can send. See the `channel-setup` skill for the full model.

## Webhook Types

- **Sender Webhooks**: Message events (inbound, delivery status, templates) - configured per sender
- **Project Webhooks**: Project-level events (partner invitations) - one per project. A parent project does not receive its sub-accounts' events: configure the webhook with each sub-account's own API key (`POST /v1/invitations/webhook`).

## Available Events

| Event | Category | Description |
|-------|----------|-------------|
| `message.inbound` | Inbound | Customer sent you a message |
| `conversation.new` | Inbound | First message from a new contact |
| `message.unsupported` | Inbound | Unsupported message type received |
| `message.queued` | Outbound | Message queued for delivery |
| `message.sent` | Outbound | Message sent to carrier |
| `message.delivered` | Outbound | Message delivered to recipient |
| `message.read` | Outbound | Message read by recipient |
| `message.failed` | Outbound | Message delivery failed |
| `broadcast.status_changed` | Broadcasts | Broadcast status changed |
| `template.status_changed` | Templates | WhatsApp template approval status changed, or Meta recategorized it. `data` carries `templateId`, `name`, `previousStatus`, `currentStatus`, `rejectionReason`, `category` |
| `invitation.status_changed` | Invitations | Partner invitation status changed (in_progress, completed, failed, cancelled, or back to pending on resend). Never sent for expiry |
| `domain.verified` | Domains | Custom email domain passed verification |
| `domain.failed` | Domains | Custom email domain failed verification |

## Configure Webhook via SDK

### TypeScript - Create Sender with Webhook

```typescript
const sender = await zavu.senders.create({
  name: "My Sender",
  phoneNumber: "+15551234567",
  webhookUrl: "https://your-app.com/webhooks/zavu",
  webhookEvents: ["message.inbound", "message.delivered", "message.failed"],
});
// Store sender.webhook.secret securely - only shown once!
```

### Update Webhook

```typescript
await zavu.senders.update({
  senderId: "snd_abc123",
  webhookUrl: "https://new-url.com/webhooks",
  webhookEvents: ["message.inbound"],
  webhookActive: true,
});
```

### Regenerate Secret

```typescript
const result = await zavu.senders.webhookSecret.regenerate({
  senderId: "snd_abc123",
});
console.log(result.secret); // whsec_new_secret...
```

## Webhook Payload Structure

The top-level envelope is the same for every event; event-specific fields live in `data`. `timestamp` is when Zavu dispatched the webhook (Unix ms).

```json
{
  "id": "evt_1705312200000_abc123",
  "type": "message.inbound",
  "timestamp": 1705312200000,
  "senderId": "snd_abc123",
  "projectId": "prj_xyz789",
  "data": { }
}
```

## Inbound Message Data (`message.inbound`)

For `message.inbound`, `data` carries the message. On inbound, `to` is your own number (the message's destination) and `from` is the sender.

| Field | Description |
|-------|-------------|
| `messageId` | Zavu message ID. |
| `conversationId` | Inbox thread id. `null` while the thread is still being created (use `conversation.new`'s id, or `GET /v1/messages/{id}`). See "Deep-linking to the inbox" below. |
| `from` | Sender: the contact for a 1:1, or the participant for a group message. Usually an E.164 phone number, but for WhatsApp contacts who adopted a username and hid their number it is their business-scoped user ID (BSUID, e.g. `US.13491208655302741918`) — treat it as opaque and pass it back as `to` when replying. |
| `to` | Your own number (the message's destination). |
| `channel` | Delivery channel (`sms`, `whatsapp`, `telegram`, `email`, `instagram`, `messenger`, `voice`). |
| `messageType` | `text`, `image`, `video`, etc. A reply to a `location_request` arrives as `location` (not a new type) with `content.replyToMessageId` set to the request — match on that to correlate. |
| `text` | Text body or media caption, when present. |
| `providerTimestamp` | The provider's original receive time (Unix ms) for WhatsApp, Telegram, Instagram, Messenger; `null` for SMS and email. Compare with the top-level `timestamp` to detect delayed deliveries. |
| `referral` | Click-to-WhatsApp ad attribution. WhatsApp only, and only on the first message of an ad-originated thread. See "Click-to-WhatsApp attribution" below. |

### Deep-linking to the inbox

Both `message.inbound` and `conversation.new` carry a `conversationId` in `data` — the id of the inbox thread. Build a direct link so your team can open the conversation in the Zavu dashboard:

```
https://dashboard.zavu.dev/{locale}/inbox?conv={conversationId}
```

`{locale}` is the dashboard UI language (e.g. `en`, `es`).

On `message.inbound`, `conversationId` is `null` while the conversation row is still being created — on the first message of a brand-new thread, and, if several messages from a never-seen address arrive near-simultaneously, on each of those (only one `conversation.new` is emitted). Recover the id from `conversation.new`, or fetch it any time from `GET /v1/messages/{messageId}`, whose `conversationId` is always populated.

### Reply / quote context

Present on `message.inbound` when the contact replied to (quoted) an earlier message, inside `data.content`.

| Field | Description |
|-------|-------------|
| `replyToMessageId` | Zavu message ID of the quoted message. Omitted if the quoted message is not stored in Zavu. |
| `replyToProviderMessageId` | Provider message ID (WhatsApp WAMID) of the quoted message. Present whenever it is a reply. |
| `replyToFrom` | Sender of the quoted message (E.164). |
| `replyToText` | Truncated snippet of the quoted message's text (empty for media). |
| `replyToMessageType` | Type of the quoted message (`text`, `image`, ...). |

### Click-to-WhatsApp attribution

When a contact reaches you by tapping a Click-to-WhatsApp (CTWA) ad or a post, `data.referral` carries where they came from. It is WhatsApp only, and it arrives on the **first** message of that conversation and on no message after it — persist it when it arrives, because there is no second delivery. Organic conversations never carry it.

| Field | Description |
|-------|-------------|
| `ctwaClid` | Click-to-WhatsApp click identifier. This is what Meta's Conversions API needs to credit a conversion back to the ad. Present on `ad` sources; a `post` has none. |
| `sourceId` | Identifier of the ad or post that produced the click. |
| `sourceType` | `ad` or `post`. |
| `sourceUrl` | Meta permalink to the ad or post. |
| `headline` | Headline of the ad or post. |
| `body` | Body copy of the ad or post. |
| `mediaType` | `image` or `video`, when the ad had media. |
| `imageUrl` / `videoUrl` / `thumbnailUrl` | Ad media. Only the one matching `mediaType` is present. |

```json
{
  "type": "message.inbound",
  "data": {
    "messageId": "jd7x2k3m4n5p6q7r8s9t0",
    "from": "+56912345678",
    "channel": "whatsapp",
    "messageType": "text",
    "text": "Hi, I saw your ad",
    "referral": {
      "sourceType": "ad",
      "sourceId": "120210000000000000",
      "headline": "Free first consultation",
      "mediaType": "image",
      "ctwaClid": "ARIzZm9vYmFyY3R3YWNsaWQ"
    }
  }
}
```

Fields that do not apply are omitted rather than sent empty, so check for presence before reading. `GET /v1/messages/{messageId}` returns the same object under `content.referral`.

### Email attachments

Inbound emails arrive as `message.inbound` with `channel: "email"` and `messageType: "text"`. The webhook payload carries only the body (`text`, and `htmlBody` on the fetched message) — it does **not** include attachment data. Attachments are stored separately and fetched on demand.

To retrieve them, call `GET /v1/messages/{messageId}/attachments` with the `messageId` from the webhook. It returns each attachment's metadata plus a short-lived signed `downloadUrl` (regenerated on every request — fetch promptly, don't cache the URL). This also works for outbound emails you sent with attachments. Messages without stored attachments return an empty list.

```bash
curl https://api.zavu.dev/v1/messages/MESSAGE_ID/attachments \
  -H "Authorization: Bearer $ZAVU_API_KEY"
```

```json
{
  "items": [
    {
      "id": "att_abc123",
      "filename": "invoice.pdf",
      "mimeType": "application/pdf",
      "size": 102400,
      "contentId": null,
      "isInline": false,
      "downloadUrl": "https://...signed-url...",
      "createdAt": "2024-01-15T10:00:00.000Z"
    }
  ]
}
```

Inline images embedded in the HTML body have `isInline: true` and a `contentId` referenced in `htmlBody` as `cid:<contentId>`.

## Partner Invitation Data (`invitation.status_changed`)

Fires on every stored status change of a partner invitation, delivered to the project webhook of the project that created it. A change to the same status sends nothing. Expiry is not a stored change: a `pending` invitation past `expiresAt` reads as `expired` but emits no event. `data` carries:

| Field | Description |
|-------|-------------|
| `invitationId` | Zavu invitation ID. |
| `clientName` / `clientEmail` | What you passed when creating the invitation, or `null`. |
| `connectionType` | What the client connects: `whatsapp_waba` or `messenger`. |
| `previousStatus` / `currentStatus` | The transition. |
| `senderId` | Present on `completed`: the sender created in your project. |
| `wabaAccountId` | Present on `completed` WhatsApp invitations: the WhatsApp Business Account ID. |
| `connectedAccount` | Present on `completed`: `{ channel, id, name }` — the WhatsApp number or the Facebook Page that was linked. |
| `failureReason` | Present on `failed`. Stable code: `fb_cancelled`, `fb_not_authorized`, `signup_abandoned`, `meta_no_pages`, `internal_error`, and others. Treat unknown codes as a generic failure. |

A `failed` invitation is not terminal: the same link stays usable, and it moves back to `in_progress` when the client retries. Only act on `completed` to provision.

```json
{
  "id": "evt_1736850000000_abc123",
  "type": "invitation.status_changed",
  "timestamp": 1736850000000,
  "projectId": "jx7xyz789ghi012",
  "data": {
    "invitationId": "jh7am5bng9p3v2x1k4r8",
    "clientName": "Acme Corp",
    "clientEmail": "contact@acme.com",
    "connectionType": "messenger",
    "previousStatus": "in_progress",
    "currentStatus": "completed",
    "senderId": "sender_12345",
    "connectedAccount": {
      "channel": "messenger",
      "id": "1077492835456839",
      "name": "Acme Store"
    }
  }
}
```

## Signature Verification

Header: `X-Zavu-Signature: t=<unix_seconds>[,v1=<hex>][,v2=<hex>]`

| Part | What it covers |
|------|----------------|
| `t` | Unix timestamp in **seconds** |
| `v1` | `HMAC_SHA256(secret, body)` |
| `v2` | `HMAC_SHA256(secret, "{t}.{body}")` — the current scheme |

**Hash the right payload or every delivery 401s.** `v1` covers the body alone.
Only `v2` covers `{t}.{body}`. Read `webhook.signatureVersion` on the sender
(`GET /v1/senders/{senderId}`) to know which one that receiver gets. New senders
default to `v2`; anything created earlier is on `v1` until moved.

Prefer `v2` when present and fall back to `v1`, so one implementation works
before, during and after a migration.

### The algorithm

```
1. read the RAW body (no JSON parser in front)
2. parse the header into { t, v1?, v2? }
3. reject if |now - t| > 300
4. signed = v2 present ? `${t}.${body}` : body
   expected = HMAC_SHA256(secret, signed)
5. constant-time compare against v2 ?? v1
```

### TypeScript (Express)

```typescript
import crypto from "crypto";
import express from "express";

const app = express();
// Raw body. NOT express.json() — the signature covers the exact bytes sent.
app.use("/webhooks/zavu", express.raw({ type: "application/json" }));

function verifyZavuSignature(rawBody: string, header: string, secret: string): boolean {
  if (!header) return false;

  const parts: Record<string, string> = {};
  for (const piece of header.split(",")) {
    const i = piece.indexOf("=");
    if (i > 0) parts[piece.slice(0, i)] = piece.slice(i + 1);
  }

  const t = Number(parts.t);
  if (!Number.isFinite(t)) return false;

  const age = Math.floor(Date.now() / 1000) - t;
  if (age > 300 || age < -60) return false;

  const received = parts.v2 ?? parts.v1;
  if (!received) return false;

  const signed = parts.v2 ? `${t}.${rawBody}` : rawBody;
  const expected = crypto.createHmac("sha256", secret).update(signed).digest("hex");

  // Length first: timingSafeEqual throws on a mismatch.
  if (expected.length !== received.length) return false;
  return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(received));
}

app.post("/webhooks/zavu", (req, res) => {
  const rawBody = req.body.toString("utf8");
  if (!verifyZavuSignature(rawBody, req.headers["x-zavu-signature"] as string, process.env.ZAVU_WEBHOOK_SECRET!)) {
    return res.status(401).send("Invalid signature");
  }

  // Answer fast, then work. Zavu retries non-2xx, so a slow handler turns one
  // event into five.
  res.status(200).send("OK");
  processEvent(JSON.parse(rawBody)).catch(console.error);
});
```

### Python (Flask)

```python
import hashlib, hmac, os, time
from flask import Flask, request

app = Flask(__name__)

def verify_zavu_signature(raw_body: bytes, header: str, secret: str) -> bool:
    if not header:
        return False

    parts = {}
    for piece in header.split(","):
        key, sep, value = piece.partition("=")
        if sep:
            parts[key] = value

    try:
        t = int(parts["t"])
    except (KeyError, ValueError):
        return False

    age = int(time.time()) - t
    if age > 300 or age < -60:
        return False

    received = parts.get("v2") or parts.get("v1")
    if not received:
        return False

    signed = f"{t}.".encode() + raw_body if "v2" in parts else raw_body
    expected = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, received)

@app.post("/webhooks/zavu")
def zavu_webhook():
    raw_body = request.get_data()  # bytes, before parsing
    header = request.headers.get("X-Zavu-Signature", "")
    if not verify_zavu_signature(raw_body, header, os.environ["ZAVU_WEBHOOK_SECRET"]):
        return "Invalid signature", 401
    enqueue(request.get_json())
    return "OK", 200
```

### Go

```go
func verifyZavuSignature(rawBody []byte, header, secret string) bool {
	if header == "" {
		return false
	}

	parts := map[string]string{}
	for _, piece := range strings.Split(header, ",") {
		if k, v, ok := strings.Cut(piece, "="); ok {
			parts[k] = v
		}
	}

	t, err := strconv.ParseInt(parts["t"], 10, 64)
	if err != nil {
		return false
	}
	age := time.Now().Unix() - t
	if age > 300 || age < -60 {
		return false
	}

	received, hasV2 := parts["v2"]
	if !hasV2 {
		received = parts["v1"]
	}
	if received == "" {
		return false
	}

	mac := hmac.New(sha256.New, []byte(secret))
	if hasV2 {
		mac.Write([]byte(strconv.FormatInt(t, 10) + "."))
	}
	mac.Write(rawBody)

	return hmac.Equal([]byte(hex.EncodeToString(mac.Sum(nil))), []byte(received))
}
```

### Ruby (Sinatra)

```ruby
def verify_zavu_signature(raw_body, header, secret)
  return false if header.nil? || header.empty?

  parts = {}
  header.split(',').each do |piece|
    key, _, value = piece.partition('=')
    parts[key] = value unless value.empty?
  end

  t = Integer(parts['t'], exception: false)
  return false if t.nil?

  age = Time.now.to_i - t
  return false if age > 300 || age < -60

  received = parts['v2'] || parts['v1']
  return false if received.nil?

  signed = parts['v2'] ? "#{t}.#{raw_body}" : raw_body
  expected = OpenSSL::HMAC.hexdigest('SHA256', secret, signed)

  OpenSSL.secure_compare(expected, received)
end
```

### PHP

```php
function verifyZavuSignature(string $rawBody, ?string $header, string $secret): bool {
    if (!$header) return false;

    $parts = [];
    foreach (explode(',', $header) as $piece) {
        $i = strpos($piece, '=');
        if ($i !== false) $parts[substr($piece, 0, $i)] = substr($piece, $i + 1);
    }

    if (!isset($parts['t']) || !ctype_digit($parts['t'])) return false;
    $t = (int) $parts['t'];

    $age = time() - $t;
    if ($age > 300 || $age < -60) return false;

    $received = $parts['v2'] ?? $parts['v1'] ?? null;
    if ($received === null) return false;

    $signed = isset($parts['v2']) ? "{$t}.{$rawBody}" : $rawBody;
    return hash_equals(hash_hmac('sha256', $signed, $secret), $received);
}
```

## Which scheme is a receiver on?

Read it off the sender. `webhook.signatureVersion` is always present when a
webhook is configured.

```bash
npx zavudev senders signature $SENDER_ID
```

```
endpoint   https://api.example.com/webhooks/zavu
signature  v1

Next step:
  npx zavudev senders update snd_abc --signature-version v1+v2

That sends both signatures at once, so your current receiver is unaffected.
```

`npx zavudev senders list` has a `signature` column, which is the fastest way to
see which receivers still have to move.

Over the API it is `GET /v1/senders/{senderId}` -> `webhook.signatureVersion`.

## Moving a webhook to v2

```bash
# 1. Both signatures, one shared t. Your v1 receiver notices nothing.
npx zavudev senders update $SENDER_ID --signature-version v1+v2

# 2. Deploy the verifier above. Confirm real deliveries land in YOUR logs.

# 3. Drop v1.
npx zavudev senders update $SENDER_ID --signature-version v2
```

Same thing over the API:

```bash
curl -X PATCH https://api.zavu.dev/v1/senders/$SENDER_ID \
  -H "Authorization: Bearer $ZAVUDEV_API_KEY" \
  -d '{"webhookSignatureVersion": "v1+v2"}'
```

A brand-new sender defaults to `v2`. If it points at an endpoint that already
serves an older sender still reading `v1`, create it on both:

```bash
npx zavudev senders create --name Support --phone +15551234567 \
  --webhook-url https://api.example.com/webhooks/zavu \
  --webhook-events message.inbound \
  --signature-version v1+v2
```

`v1` straight to `v2` returns `400`; set `v1+v2` first. Step 2 is the one that
matters: a receiver that answers `200` before verifying looks identical to a
working one from Zavu's side, so a passing test request proves nothing. Confirm
in the receiver's own logs.

Full guide: https://docs.zavu.dev/guides/receiving-messages/signature-migration

## Tool webhooks are a different format

When an agent calls a tool that has a `webhookUrl`, Zavu POSTs with the **same
header name and a different shape**:

```
X-Zavu-Signature: 2120e306a4ce...     bare hex, no t=, no v1=/v2=
X-Zavu-Timestamp: 1786113454812       separate header, MILLISECONDS
X-Zavu-Tool:      get_order_status
```

The digest is `HMAC_SHA256(secret, body)`, same as `v1`, but the envelope
differs, so the verifier above returns false on one of these. Write a second
one, or branch on whether the header contains `=`.

Two things to know:

- **Every tool call is signed.** Zavu generates a secret when the tool is
  created and returns it on that response only. Supply your own with `--secret`
  if you already have one. Lost it? Rotate:
  `POST /v1/senders/{senderId}/agent/tools/{toolId}/webhook/secret`. Reject when
  the header is missing; never "skip verification if unsigned".
- Its payload carries its own `timestamp`, inside the signed body. Do the
  freshness check against that one rather than the `X-Zavu-Timestamp` header.

A tool declared in a Zavu Function with `defineTool` needs none of this: the
handler runs inside the function, with no HTTP hop.

## Retry Policy

| Attempt | Delay |
|---------|-------|
| 1st retry | 1 minute |
| 2nd retry | 5 minutes |
| 3rd retry | 15 minutes |
| 4th retry | 1 hour |
| 5th retry | 4 hours |

After 5 retries, delivery is marked as failed.

## Best Practices

1. **Return 200 quickly** - respond within 30 seconds, process async
2. **Verify signatures** - always verify in production
3. **Idempotent handlers** - check `event.id` to skip duplicates
4. **Use raw body** - signature is computed on raw body, not parsed JSON
5. **Test with ngrok** - expose local server for development
