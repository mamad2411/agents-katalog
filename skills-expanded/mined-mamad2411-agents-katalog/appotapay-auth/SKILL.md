---
name: appotapay-auth
description: >-
  Build the AppotaPay authentication JWT (the X-APPOTAPAY-AUTH header) and sign request parameters.
  Use when integrating AppotaPay and you need to authenticate API calls, create/refresh the JWT token,
  understand the HS256 JWT claims (iss, jti, api_key, exp), or compute the HMAC-SHA256 request signature
  from PARTNER_CODE / API_KEY / SECRET_KEY. Required by every other AppotaPay API call.
license: MIT
metadata:
  version: "0.1.0"
  source: https://docs.appotapay.com
---

# AppotaPay authentication (X-APPOTAPAY-AUTH JWT)

Every AppotaPay API request carries a JWT in the `X-APPOTAPAY-AUTH` header, signed with your
`SECRET_KEY` using **HS256**.

> **Verify against live docs.** The references below are an offline snapshot and may lag. Confirm the
> JWT claims and signing rules against the current docs before shipping:
> `https://docs.appotapay.com/llms-v2.0-security-full.txt` (JWT) and
> `https://docs.appotapay.com/llms-v2.0-payment-payment-signature-full.txt` (signature).
> See the router skill's `references/live-docs.md`. If live and snapshot differ, the live doc wins.

## JWT structure

**Header**
```json
{ "typ": "JWT", "alg": "HS256", "cty": "appotapay-api;v=1" }
```

**Payload (claims)**
```json
{
  "iss": "YOUR_PARTNER_CODE",
  "jti": "YOUR_API_KEY-<unix_time>",
  "api_key": "YOUR_API_KEY",
  "exp": 1614225624
}
```

| Claim     | Value                                                            |
|-----------|------------------------------------------------------------------|
| `iss`     | `PARTNER_CODE`                                                   |
| `api_key` | `API_KEY`                                                       |
| `jti`     | `API_KEY` + `"-"` + current unix timestamp (unique per request)  |
| `exp`     | expiry unix timestamp (keep short, e.g. now + 300s)              |

Sign with `SECRET_KEY` (HS256). Put the result in the `X-APPOTAPAY-AUTH` header.

> Generate a **fresh** token per request (or short-lived) — `jti` must be unique and `exp` short.
> Build the JWT **server-side only**; never ship `SECRET_KEY` to a browser/mobile client.

## Quick start

Ready-to-run generators are in `scripts/` (read the one matching the project's language):

- Node.js / TypeScript: `scripts/gen-jwt.mjs`
- Python: `scripts/gen_jwt.py`
- PHP: `scripts/gen-jwt.php`

```bash
# Node (uses the `jsonwebtoken` package)
APPOTAPAY_PARTNER_CODE=APPOTAPAY \
APPOTAPAY_API_KEY=FJcmF8uj2ISveL5FvvNk4pnp8xrhINz8 \
APPOTAPAY_SECRET_KEY=XAonJgy14YhtePEITXhyBS2unjfJLAV3 \
node scripts/gen-jwt.mjs
```

Use it as a header:
```
X-APPOTAPAY-AUTH: <jwt>
Content-Type: application/json
```

## Request parameter signature

Some AppotaPay flows and **all IPN/redirect callbacks** use an HMAC-SHA256 signature over a
canonical string. The rule: sort params alphabetically by key, join as `key=value` with `&`,
then `HMAC_SHA256(string, SECRET_KEY)`. See `references/signature.md` for the exact algorithm,
worked examples, and how it differs from IPN verification (which signs an opaque `data` string).

## References

- `references/jwt.md` — full JWT spec, library list, common pitfalls (clock skew, expired token = 401).
- `references/signature.md` — request param signing + how IPN/redirect signatures are computed/verified.
