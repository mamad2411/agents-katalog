---
name: sendchamp-sms-send-message
description: Send transactional and bulk SMS via Sendchamp for African markets including Nigeria, Kenya, and Ghana. Covers E.164 formatting, Nigerian DND routes (dnd, non_dnd, international), sender ID registration, and wallet balance checks. Use when integrating Sendchamp SMS, sending OTP messages, order notifications, or bulk SMS in Africa.
---

# Sendchamp SMS — Send Message

## Overview

Sendchamp SMS API delivers transactional and promotional SMS across Africa. Unlike global providers, Sendchamp encodes **Nigerian DND routing** directly — critical for OTP and marketing compliance.

| Use case | Recommended route |
|----------|-------------------|
| OTP, alerts, order updates | `non_dnd` |
| Nigerian marketing/promo | `dnd` |
| International recipients | `international` |

## Prerequisites

- Sendchamp account with funded wallet — [my.sendchamp.com/signup](https://my.sendchamp.com/signup)
- Approved sender ID registered in dashboard
- Environment variable: `SENDCHAMP_ACCESS_KEY`

```bash
export SENDCHAMP_ACCESS_KEY=sendchamp_live_YOUR_KEY
```

## Quickstart

**curl**

```bash
curl -X POST https://api.sendchamp.com/api/v1/sms/send \
  -H "Authorization: Bearer $SENDCHAMP_ACCESS_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+2348012345678",
    "message": "Your order #1234 has shipped.",
    "sender_name": "MyBrand",
    "route": "non_dnd",
    "country_code": "NG"
  }'
```

**Node.js**

```javascript
const res = await fetch("https://api.sendchamp.com/api/v1/sms/send", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.SENDCHAMP_ACCESS_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    to: "+2348012345678",
    message: "Your order #1234 has shipped.",
    sender_name: "MyBrand",
    route: "non_dnd",
    country_code: "NG",
  }),
});
const data = await res.json();
```

**Python**

```python
import os, requests

resp = requests.post(
    "https://api.sendchamp.com/api/v1/sms/send",
    headers={
        "Authorization": f"Bearer {os.environ['SENDCHAMP_ACCESS_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "to": "+2348012345678",
        "message": "Your order #1234 has shipped.",
        "sender_name": "MyBrand",
        "route": "non_dnd",
        "country_code": "NG",
    },
)
```

## Key patterns

### Multiple recipients

Pass `to` as an array:

```json
{
  "to": ["+2348012345678", "+2348098765432"],
  "message": "Server maintenance at 2am.",
  "sender_name": "MyBrand",
  "route": "non_dnd"
}
```

### Check wallet before sending

```bash
curl -X GET https://api.sendchamp.com/api/v1/wallet-balance \
  -H "Authorization: Bearer $SENDCHAMP_ACCESS_KEY"
```

### Bulk SMS via contact list

Use `POST /api/v1/sms/send-bulk` with dashboard-managed IDs:

```json
{
  "message": "Flash sale ends tonight!",
  "contact_list_id": "contact-list-uid",
  "sender_id": 1,
  "route_id": 1
}
```

Bulk routes: `dnd`, `non_dnd`, `international`.

## Africa routing

For detailed route and compliance rules, see [references/africa-routes.md](references/africa-routes.md).

**Rule of thumb:** OTP and transactional → `non_dnd`. Marketing in Nigeria → `dnd`.

## Response fields

| Field | Description |
|-------|-------------|
| `reference` | Message tracking reference |
| `status` | `sent`, `pending`, `failed`, `delivered` |
| `phone_number` | Recipient number |

## Common errors

| Message | Cause | Fix |
|---------|-------|-----|
| `Low balance, fund your wallet` | Empty wallet | Top up at my.sendchamp.com |
| `insufficient fund` | Balance too low | Check `/wallet-balance` |
| Invalid sender | Unapproved sender_name | Register sender in dashboard |
| `Message failed to send` | Bad route or number | Verify E.164 and route |

## CANNOT

- **Cannot send without approved sender_name** — register in dashboard first
- **Cannot use promo content on non_dnd for DND-registered numbers** — use `dnd` route for marketing
- **Cannot send without E.164 format** — always include country code with `+`
- **Cannot send with empty message** — `message` is required and non-empty
- **Cannot skip wallet funding** — all sends debit wallet in real-time

## Next steps

- OTP verification: use skill `sendchamp-verify-send-otp`
- Africa route details: [references/africa-routes.md](references/africa-routes.md)
- API reference: https://sendchamp.readme.io
- Docs MCP: connect `https://mcp.sendchamp.com/docs` for live API search
