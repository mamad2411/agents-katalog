---
name: channel-setup
description: How accounts, senders and channels relate in Zavu - what you connect, what bills, and how to find the sender to send from.
---

# Channel Setup

## When to Use

Use this skill when wiring a freshly connected channel (WhatsApp, Telegram, Instagram, Messenger, email, phone number) into code, or when deciding which sender ID to pass to the API.

## The two-layer model

Zavu has two objects that beginners often conflate:

| Layer | What it is | Where it lives |
|---|---|---|
| **Account** | The connection to a provider: a WhatsApp Business Account, a Facebook Page, an Instagram account, a Telegram bot, an email domain, a phone number | Connected in the dashboard (Accounts, Phone Numbers) or via partner invitations |
| **Sender** | The API handle that ROUTES accounts: what you pass as `Zavu-Sender`, what carries the webhook and the AI agent | `GET /v1/senders` |

**Billing:** accounts are what you pay for (a WhatsApp account, a channel connection, a phone number). **Senders are free** — they are the view that groups your accounts under one sending identity.

**Connecting always yields a ready sender.** When an account is connected and no sender references it, Zavu creates one automatically, named after the account (the WhatsApp verified name, the Page name, the @username). The first sender of a project becomes the default. Partner-invitation connects have always worked this way; every connect surface now does.

## Finding the sender to send from

`GET /v1/senders` is the answer to "what can I send with, and from where?". Each sender's `channels` array is the source of truth for capability — computed from its actual configuration, not inferred:

```json
{
  "id": "sender_12345",
  "name": "Acme Store",
  "channels": ["whatsapp", "sms", "voice"],
  "isDefault": true
}
```

- An empty `channels` array means the sender cannot send anything yet (a phone number alone does not enable SMS).
- `channels` lists only what is connected **and activated**. A connected account that is switched off is left out, because every send on it is refused.
- Omit `Zavu-Sender` to use the project's default sender.
- To target a specific one, pass its ID as a header inside the send params object: `'Zavu-Sender': "sender_12345"`.

## Activating a connected channel

Connecting an account does not switch it on: a newly connected WhatsApp account, Telegram bot, Instagram account, Messenger Page or email address starts **inactive**, and sends on it are refused until it is activated. Activation is what bills the connection (see Constraints). Do it in the dashboard (Accounts, **Activate**) or over the API, per sender and channel:

```bash
curl -X POST https://api.zavu.dev/v1/senders/sender_12345/channels/telegram/activate \
  -H "Authorization: Bearer $ZAVU_API_KEY"
```

```json
{
  "sender": { "id": "sender_12345", "channels": ["telegram"] },
  "channel": "telegram",
  "activated": true,
  "chargedCents": 300,
  "monthlyCents": 300
}
```

- `{channel}` is one of `whatsapp`, `telegram`, `instagram`, `messenger`, `email`. SMS, one-way SMS and voice are billed per message and have nothing to activate (`400`).
- `chargedCents` is what this call took from the balance: zero when the channel was already active, its month is already paid, or the plan includes it. Calling it twice never charges twice.
- Errors: `402 insufficient_balance`, `403 plan_limit_reached`, `409 channel_not_connected` (the sender has no account for that channel), `409 connection_not_ready` (connected but cannot carry messages yet).
- `POST /v1/senders/{senderId}/channels/{channel}/deactivate` switches it off without disconnecting the account. The month already paid is not refunded, and re-activating within it is free.
- Live API keys only.

## Per-channel wiring

| You connected... | The sender... | Send with |
|---|---|---|
| WhatsApp (embedded signup or invitation) | auto-created, `channels` includes `whatsapp` once the account is active | `channel: "whatsapp"` |
| Messenger Page / Instagram account | auto-created, named after the Page/@username | `channel: "messenger"` / `"instagram"` |
| Telegram bot | attached via `POST /v1/senders/{senderId}/telegram` (bot token from @BotFather) | `channel: "telegram"` |
| Email domain (verified) | attach with `emailAddress` on sender create/update | `channel: "email"` |
| Nothing yet (zero-setup start) | `enableSmsOneway: true` on `POST /v1/senders` or `PATCH /v1/senders/{senderId}` — no number, no credential, active immediately; recipients cannot reply. Sending to a US or Canadian (+1) number still needs an approved 10DLC campaign, as it does on `sms` | `channel: "sms_oneway"` |
| Phone number | route it to a sender (`PATCH /v1/phone-numbers/{id}` with `senderId`) — that is what turns SMS on; add `enableVoice` for calls | `channel: "sms"` / `"voice"` |

One sender can carry several channels at once — that is the point: one `Zavu-Sender`, every channel.

## Constraints

- A sender belongs to one project; an account is routed by at most one sender.
- Webhooks are configured per sender and apply to every channel that sender carries.
- An AI agent is attached per sender but answers only the channels its own `triggerOnChannels` names. A channel the sender receives on that the list omits is dropped before the agent sees it — no reply, no error, and the Playground still answers, because it bypasses the filter. The drop is recorded: `GET /v1/senders/{senderId}/agent/executions` returns it with `status: "filtered"` and the channel in `errorMessage`. Use `["*"]` unless you are deliberately excluding one.
- Free plans include two connection slots (one can be a WhatsApp account); paid plans add connections at a monthly fee per connection. Creating senders never costs anything.
