---
name: sendchamp-verify-send-otp
description: Send and confirm one-time passcodes (OTP) via Sendchamp Verification API over SMS, email, WhatsApp, or voice. Covers Nigeria and African phone formats, token configuration, verification reference handling, and server-side confirm flow. Use when building phone login, 2FA, user verification, or OTP authentication with Sendchamp in Africa.
---

# Sendchamp Verify — Send OTP

## Overview

Sendchamp Verification API manages OTP generation, multi-channel delivery, and confirmation. One API covers SMS, email, WhatsApp, and voice — change only the `channel` parameter.

| Channel | Best for |
|---------|----------|
| `sms` | Phone verification, 2FA (widest reach in Africa) |
| `whatsapp` | Lower cost where WhatsApp is primary |
| `email` | Account verification |
| `voice` | Accessibility / SMS delivery issues |

For SMS routing rules in Nigeria, pair with skill `sendchamp-sms-send-message`.

## Prerequisites

- Sendchamp account with funded wallet
- Approved sender ID (for SMS/WhatsApp channels)
- `SENDCHAMP_ACCESS_KEY` environment variable

## Quickstart

### Step 1 — Send OTP

**curl**

```bash
curl -X POST https://api.sendchamp.com/api/v1/verification/send \
  -H "Authorization: Bearer $SENDCHAMP_ACCESS_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "sms",
    "customer_mobile_number": "+2348012345678",
    "sender": "MyBrand",
    "token_type": "numeric",
    "token_length": 6,
    "expiration_time": 10
  }'
```

**Node.js**

```javascript
const sendRes = await fetch("https://api.sendchamp.com/api/v1/verification/send", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.SENDCHAMP_ACCESS_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    channel: "sms",
    customer_mobile_number: "+2348012345678",
    sender: "MyBrand",
    token_type: "numeric",
    token_length: 6,
    expiration_time: 10,
  }),
});
const { data } = await sendRes.json();
// Save data.reference server-side — do NOT send data.token to client
```

### Step 2 — Confirm OTP

```bash
curl -X POST https://api.sendchamp.com/api/v1/verification/confirm \
  -H "Authorization: Bearer $SENDCHAMP_ACCESS_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "verification_code": "482910",
    "verification_reference": "MN-OTP-abc123"
  }'
```

```javascript
const confirmRes = await fetch("https://api.sendchamp.com/api/v1/verification/confirm", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.SENDCHAMP_ACCESS_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    verification_code: userCode,
    verification_reference: storedReference,
  }),
});
const confirm = await confirmRes.json();
if (confirm.data?.status === "verified") {
  // User verified — grant access
}
```

## Key patterns

### Supported channels

| Channel | Required fields |
|---------|-----------------|
| `sms` | `customer_mobile_number`, `sender` |
| `email` | `customer_email_address` |
| `whatsapp` | `customer_mobile_number`, `sender` |
| `voice` | `customer_mobile_number` |

### Token configuration

| Field | Values | Default |
|-------|--------|---------|
| `token_type` | `numeric`, `alphanumeric` | — |
| `token_length` | 4–10 | 6 |
| `expiration_time` | minutes | 10 |

### End-to-end auth flow

```
User enters phone → your server calls /verification/send
                  → store reference in session/DB
User enters code  → your server calls /verification/confirm
                  → if verified, create session/JWT
```

See [references/confirm-flow.md](references/confirm-flow.md) for details.

## Response fields (send)

| Field | Description |
|-------|-------------|
| `reference` | **Save this** — required for confirm (`MN-OTP-...`) |
| `status` | Delivery status |
| `channel.name` | Channel used |
| `token` | Generated code — **do not expose to client in production** |

## Status values

| Status | Meaning |
|--------|---------|
| `processing` | Sent, awaiting user input |
| `verified` | Code confirmed |
| `expired` | Past expiration_time |

## Common errors

| Message | Fix |
|---------|-----|
| `invalid token` | Wrong code or reference |
| `this otp has expired` | Send new OTP |
| `this otp has already been used` | Do not retry — send new OTP |
| `Low balance, fund your wallet` | Top up wallet |
| `invalid channel name` | Use sms, email, whatsapp, or voice |
| WhatsApp send failure | Fall back to SMS channel |

## CANNOT

- **Cannot confirm without reference** — always store `reference` from send response
- **Cannot reuse a verified OTP** — each code is single-use
- **Cannot extend expiry on an existing OTP** — send a new verification instead
- **Cannot skip server-side confirm** — never validate OTP client-side only
- **Cannot expose token to end users in production** — confirm server-side even if API returns token in dev

## Security

- Store `verification_reference` in server session or database
- Rate-limit `/verification/confirm` per user and IP
- Never log OTP codes in plain text
- Use HTTPS for all API calls

## Next steps

- SMS routing for Nigeria: skill `sendchamp-sms-send-message`
- Confirm flow details: [references/confirm-flow.md](references/confirm-flow.md)
- Full OTP guide: [guides/otp-flow.md](../../../guides/otp-flow.md)
- Docs MCP: `https://mcp.sendchamp.com/docs`
