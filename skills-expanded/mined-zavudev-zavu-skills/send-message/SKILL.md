---
name: send-message
description: Send messages via SMS, WhatsApp, Email, Telegram, Instagram, Messenger, or Voice with channel selection logic.
---

# Send Message

## When to Use

Use this skill when building code to send messages through the Zavu API. Covers channel selection, the recipient (`to`) formats, message types, and error handling.

## Channels

`auto`, `sms`, `sms_oneway`, `whatsapp`, `telegram`, `email`, `instagram`, `messenger`, `voice`.

## Senders vs accounts (one paragraph)

A **Sender** is the API handle you pass as `Zavu-Sender`; **accounts** (a WhatsApp Business Account, a Facebook Page, a Telegram bot, a phone number) are the connections it routes — and what bills. Senders are free. Connecting an account in the dashboard auto-creates its sender; find it with `GET /v1/senders` and trust its `channels` array for what it can send. See the `channel-setup` skill for the full model.

## Channel Selection Decision Tree

```
Is recipient an email address?
  -> YES: channel = "email" (the sender needs an email channel: a verified domain)
Is message type non-text (image, video, buttons, list, template, etc.)?
  -> YES: channel = "whatsapp" (auto-selected)
Need voice call / TTS?
  -> YES: channel = "voice"
Recipient is a numeric chat ID (Instagram / Messenger / Telegram)?
  -> YES: channel = "instagram" | "messenger" | "telegram"
Need one-way SMS (no inbound replies)?
  -> YES: channel = "sms_oneway"
Need guaranteed delivery to a specific channel?
  -> YES: channel = "sms" | "whatsapp" | "telegram" | "instagram" | "messenger"
Want cost-optimized routing?
  -> YES: channel = "auto" (ML-powered smart routing)
Default?
  -> channel = "sms" (or omit for default)
```

## Recipient (`to`) formats

The universal `to` field accepts several identifier formats. Routing follows `channel` (or is auto-selected from the identifier when `channel` is omitted).

| Format | Example | Notes |
|--------|---------|-------|
| E.164 phone | `+14155551234` | SMS, WhatsApp, Voice, Telegram. |
| Email address | `user@example.com` | Defaults to `email`. |
| WhatsApp BSUID | `US.13491208655302741918` | Business-scoped user ID. Routed to WhatsApp; use to message a contact who adopted a username and hid their phone number. |
| Numeric chat ID | `123456789` | Telegram, Instagram, or Messenger chat/user ID. |

## Basic Messages

### SMS (default)

**TypeScript:**
```typescript
const result = await zavu.messages.send({
  to: "+14155551234",
  text: "Your verification code is 123456",
});
console.log(result.message.id);
```

**Python:**
```python
result = zavu.messages.send(
    to="+14155551234",
    text="Your verification code is 123456",
)
print(result.message.id)
```

**Go:**
```go
result, err := client.Messages.Send(context.TODO(), zavudev.MessageSendParams{
    To:   zavudev.String("+14155551234"),
    Text: zavudev.String("Your verification code is 123456"),
})
fmt.Println(result.Message.ID)
```

**Ruby:**
```ruby
result = client.messages.send(to: "+14155551234", text: "Your verification code is 123456")
puts result.message.id
```

**PHP:**
```php
$result = $client->messages->send([
    'to' => '+14155551234',
    'text' => 'Your verification code is 123456',
]);
echo $result->message->id;
```

### WhatsApp Text

```typescript
const result = await zavu.messages.send({
  to: "+14155551234",
  channel: "whatsapp",
  text: "Hello from Zavu!",
});
```

### Email

```typescript
const result = await zavu.messages.send({
  to: "user@example.com",
  channel: "email",
  subject: "Your order has shipped",
  text: "Hi John, your order #12345 has shipped.",
  htmlBody: "<h1>Order Shipped</h1><p>Your order #12345 has shipped.</p>",
  replyTo: "support@example.com",
});
```

### Voice (Text-to-Speech)

```typescript
const result = await zavu.messages.send({
  to: "+14155551234",
  channel: "voice",
  text: "Your verification code is 1 2 3 4 5 6",
  voiceLanguage: "en-US", // optional, auto-detected from country code
});
```

### One-Way SMS

Use `sms_oneway` when replies are not expected (no inbound path back to you).

```typescript
await zavu.messages.send({
  to: "+14155551234",
  channel: "sms_oneway",
  text: "Your appointment is confirmed for 3pm.",
});
```

### Instagram / Messenger

Target a numeric chat/user ID (from an inbound conversation).

```typescript
// Instagram Direct
await zavu.messages.send({
  to: "17841400000000000",
  channel: "instagram",
  text: "Hello from Zavu via Instagram!",
});

// Messenger (Facebook Page / Marketplace chat)
await zavu.messages.send({
  to: "24025631120151183",
  channel: "messenger",
  text: "Hello from Zavu via Messenger!",
});
```

## WhatsApp Rich Messages

### Image

```typescript
await zavu.messages.send({
  to: "+14155551234",
  messageType: "image",
  text: "Check out this product!", // caption
  content: { mediaUrl: "https://example.com/image.jpg" },
});
```

### Document

```typescript
await zavu.messages.send({
  to: "+14155551234",
  messageType: "document",
  content: {
    mediaUrl: "https://example.com/invoice.pdf",
    filename: "invoice.pdf",
  },
});
```

### Video / Audio

```typescript
// Video
await zavu.messages.send({
  to: "+14155551234",
  messageType: "video",
  text: "Watch this!",
  content: { mediaUrl: "https://example.com/video.mp4" },
});

// Audio
await zavu.messages.send({
  to: "+14155551234",
  messageType: "audio",
  content: { mediaUrl: "https://example.com/audio.mp3" },
});
```

### Sticker

```typescript
await zavu.messages.send({
  to: "+14155551234",
  messageType: "sticker",
  content: { mediaUrl: "https://example.com/sticker.webp" },
});
```

### Location

```typescript
await zavu.messages.send({
  to: "+14155551234",
  messageType: "location",
  content: {
    latitude: 37.7749,
    longitude: -122.4194,
    locationName: "San Francisco",
    locationAddress: "123 Main St, San Francisco, CA",
  },
});
```

### Contact Card

```typescript
await zavu.messages.send({
  to: "+14155551234",
  messageType: "contact",
  content: {
    contacts: [
      { name: "John Doe", phones: ["+14155551234", "+14155555678"] },
    ],
  },
});
```

### Interactive Buttons (max 3)

```typescript
await zavu.messages.send({
  to: "+14155551234",
  messageType: "buttons",
  text: "How would you rate your experience?",
  content: {
    buttons: [
      { id: "great", title: "Great!" },
      { id: "okay", title: "It was okay" },
      { id: "poor", title: "Not good" },
    ],
  },
});
```

### List Message

```typescript
await zavu.messages.send({
  to: "+14155551234",
  messageType: "list",
  text: "Select an option:",
  content: {
    listButton: "View Options",
    sections: [{
      title: "Products",
      rows: [
        { id: "prod_1", title: "Product A", description: "$10.00" },
        { id: "prod_2", title: "Product B", description: "$20.00" },
      ],
    }],
  },
});
```

### Template Message

`templateVariables` fill body placeholders (keyed by position `1`, `2`, ... for positional templates, or by name for named ones — do not mix). `templateButtonVariables` fill dynamic URL/OTP button placeholders (keyed by button index `0`, `1`, `2`). `templateHeaderVariables` set a text-header variable (keyed by `1`).

```typescript
await zavu.messages.send({
  to: "+14155551234",
  messageType: "template",
  content: {
    templateId: "tpl_abc123",
    templateVariables: { "1": "John", "2": "ORD-12345" },
    templateButtonVariables: { "0": "abc-report-token" }, // optional: dynamic URL/OTP buttons
  },
});
```

### CTA URL (Call-to-Action button)

```typescript
await zavu.messages.send({
  to: "+14155551234",
  messageType: "cta_url",
  text: "Check out our latest collection",
  content: {
    ctaDisplayText: "View Products",          // max 20 chars
    ctaUrl: "https://example.com/products",
    ctaHeaderType: "image",                    // optional: text | image | video | document
    ctaHeaderMediaUrl: "https://example.com/header.jpg",
    footerText: "Limited time offer",          // optional, max 60 chars
  },
});
```

### Location Request (ask the contact to share their location)

Sends a message with a fixed "Send location" button. WhatsApp-only. Takes **no** `content` object — the prompt goes in `text` (max 1024 chars).

Not yet generated in the SDK — use REST:

```bash
curl -X POST https://api.zavu.dev/v1/messages \
  -H "Authorization: Bearer $ZAVU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+14155551234",
    "channel": "whatsapp",
    "messageType": "location_request",
    "text": "To finish your order, share the delivery address."
  }'
```

The answer arrives as a normal inbound `location` message (not a new type) with
`content.replyToMessageId` set to the ID of the request. Match on that field to
correlate the coordinates with the order/ticket you asked about:

```typescript
if (
  event.type === "message.inbound" &&
  event.data.messageType === "location" &&
  event.data.content?.replyToMessageId === pendingRequestId
) {
  const { latitude, longitude } = event.data.content;
}
```

`content.name` and `content.address` are optional — present only when the contact
picks a saved place instead of dropping a pin. Always rely on lat/lng.

### Contact Info Request (ask the contact to share their phone number)

Sends a message with a fixed "Share Contact Info" button. WhatsApp-only. Takes **no** `content` object — the prompt goes in `text` (max 1024 chars). Essential for contacts who adopted a WhatsApp username and are only known by BSUID.

Not yet generated in the SDK — use REST:

```bash
curl -X POST https://api.zavu.dev/v1/messages \
  -H "Authorization: Bearer $ZAVU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "US.13491208655302741918",
    "channel": "whatsapp",
    "messageType": "request_contact_info",
    "text": "Share your phone number so our team can call you back."
  }'
```

The answer arrives as a normal inbound `contact` message with the shared number in
`content.contacts[0].phones`. When the sender was only known by BSUID, Zavu links
the shared phone to that contact automatically — no manual update needed.

Note: authentication templates with one-tap/zero-tap/copy-code buttons cannot be
sent to a BSUID (WhatsApp error `131062`) — recover the phone number first.
Broadcasts also reject BSUID/`@username` recipients.

### Reaction

```typescript
await zavu.messages.react({
  messageId: "msg_abc123",
  emoji: "\ud83d\udc4d",
});
```

## Typing Indicator

Mark an inbound WhatsApp message as read and show a typing indicator while you prepare a reply (`POST /v1/messages/{messageId}/typing`). It clears automatically when you send a reply or after 25 seconds. Only valid for inbound WhatsApp messages. Use it when a reply takes more than a couple of seconds (LLM agent, tool call, lookup).

```bash
curl -X POST https://api.zavu.dev/v1/messages/MESSAGE_ID/typing \
  -H "Authorization: Bearer $ZAVU_API_KEY" \
  -H "Zavu-Sender: sender_12345"
```

## Sender Override

```typescript
await zavu.messages.send({
  to: "+14155551234",
  text: "Hello!",
  'Zavu-Sender': "snd_abc123",
});
```

## Idempotency

```typescript
await zavu.messages.send({
  to: "+14155551234",
  text: "Payment confirmed",
  idempotencyKey: "payment_confirm_order_123",
});
```

## Disable Automatic Fallback

By default, WhatsApp messages auto-fallback to SMS on failure. To disable:

```typescript
await zavu.messages.send({
  to: "+14155551234",
  channel: "whatsapp",
  text: "WhatsApp only — no SMS fallback",
  fallbackEnabled: false,
});
```

## Get Status & List Messages

```typescript
// Get single message
const msg = await zavu.messages.get({ messageId: "msg_abc123" });
console.log(msg.message.status); // queued | sending | sent | delivered | read | failed

// List with filters + pagination
let cursor: string | undefined;
do {
  const result = await zavu.messages.list({ status: "delivered", limit: 50, cursor });
  for (const message of result.items) {
    console.log(message.id, message.status);
  }
  cursor = result.nextCursor ?? undefined;
} while (cursor);
```

## Common Errors

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `whatsapp_window_closed` | 24h window not open | Use template message instead |
| `a2p_limit_exceeded` | HTTP 429: the Free plan's monthly allowance is spent. WhatsApp, Telegram, Instagram and Messenger share 2,000 messages/month, **counted in both directions** — a message a contact sends you consumes a unit exactly like one you send, so a project that sent 300 and received 1,700 is at the cap. Messages sent from the WhatsApp Business App under coexistence do not count, nor do failed sends. At the cap inbound is refused too: not stored, not in the inbox, no `message.inbound` webhook. Separate from the daily ceiling below, which never prevents reaching this monthly figure | Upgrade to a paid plan (no caps) or wait for the monthly reset on the 1st |
| `insufficient_balance` | HTTP 402: prepaid balance cannot cover the send. Email is billed from balance in 1,000-message blocks ($0.40/1k transactional, $0.80/1k marketing); SMS and voice are billed per message | Add funds from the dashboard, then retry |
| `url_not_verified` | Message has unverified URLs | Submit URLs via `/v1/urls` first |
| `url_shortener_blocked` | URL shortener detected | Use full destination URL |
| `ten_dlc_required` | HTTP 403: the destination is a US or Canadian (+1) number and the project has no approved 10DLC campaign. A carrier requirement, not a Zavu one; registering a brand and campaign needs an approved business verification | Register a 10DLC brand and campaign in the dashboard, or send to that contact on another channel |
| `sending_suspended` | HTTP 403: this account's sending was suspended after Zavu's automated review refused several of its messages. Every channel is refused while it lasts, and `details.dashboardUrl` points at support. Same code on `POST /v1/calls` | Contact support; waiting does not clear it |
| `RISK_BLOCKED` / `RISK_REJECTED` / `RISK_REVIEW_EXPIRED` | On the failed message (async), not on the response: the automated review refused the message outright, a reviewer did not approve a held one, or the review window closed first. A failed SMS is not charged | Rewrite the message, or contact support with the message ID if the refusal looks wrong |
| `SENDING_SUSPENDED` | On the failed message (async): the account's sending was suspended while this message was queued | Contact support |
| `daily_limit_exceeded` | HTTP 429: the channel group's daily ceiling, `details.limit` says which. Verified nothing: 25/day across `sms` + `sms_oneway`, 5/day `voice`, 100/day across WhatsApp + Telegram + Instagram + Messenger. Past that floor: 200/day SMS, or 10,000 once identity or business verification is approved; on Free, 50/day voice and 250/day conversational. Paid plans have no voice or conversational ceiling. Email: the plan quota (100/day on Free). Counts reset at 00:00 UTC | Wait for the reset, or verify identity / add a payment method to raise it (upgrade the plan for email) |
| `EMAIL_INVALID_RECIPIENT` | Malformed email address (async, on the failed message) | Fix the address; pre-check lists with `POST /v1/introspect/email` |
| `EMAIL_DOMAIN_NOT_FOUND` | Recipient domain has no MX or A records (async) | Remove the address; the send would hard bounce |
| `EMAIL_RECIPIENT_SUPPRESSED` | Address bounced or complained before (async) | Remove it from your lists |

**What verification changes, and what it does not.** An account sends on every channel, to any destination, from its first minute. No channel asks for identity or business verification in order to send. What verification changes is the daily ceiling: identity verification (KYC), a saved payment method, a settled deposit or a paid plan each lift an account off the lowest rung, and identity or business verification is what takes SMS to 10,000 a day. Business verification (KYB) is still required to register a 10DLC brand and campaign, which every +1 SMS destination needs. Email has no verification gate: a sender with a verified domain sends from day one within the plan quota (100/day and 3,000/month on Free). Reference: https://docs.zavu.dev/concepts/sending-limits

**Every `sms`, `sms_oneway`, `email` and `voice` message is read before it is sent** — its content, and the pattern of sends around it. Three outcomes. It is sent, which is the normal one. It is **held** for a short review: the message stays `queued` (no new status, `MessageStatus` is unchanged), and it sends normally once approved; the window is a couple of hours. Or it is **refused**: the message fails with `RISK_BLOCKED`, `RISK_REJECTED` or `RISK_REVIEW_EXPIRED` in `errorCode` and fires `message.failed`, and a refused SMS is not charged. A call is never held — a call the review stops is failed rather than placed late. Repeated refusals suspend the account's sending (`403 sending_suspended`). A broadcast is read once, on its own text, not per recipient. Do not build retry logic that re-sends a message that failed with one of these codes: the content is what was refused, so an identical retry is refused identically.

Email sends are pre-validated automatically at dispatch: guaranteed hard bounces (bad syntax, dead domain, suppressed address) are failed with the codes above instead of being sent, so they never hurt your bounce rate. These surface asynchronously on the message (`status: "failed"` + `errorCode`) and in the `message.failed` webhook. Advisory signals (role addresses like `info@`, disposable domains) never block a send — check them upfront with `POST /v1/introspect/email`.

## Constraints

- Button titles: max 20 chars, max 3 buttons
- List row titles: max 24 chars, descriptions: max 72 chars, max 10 rows per section
- Location request body: max 1024 chars, no `content` object, WhatsApp only
- Email subject: max 998 chars
- Voice language codes: `en-US`, `es-ES`, `pt-BR`, etc. (auto-detected if omitted)
- Media messages auto-select WhatsApp channel
