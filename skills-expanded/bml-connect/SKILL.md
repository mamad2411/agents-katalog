---
name: bml-connect
description: >
  BML Connect (Bank of Maldives) payment API integration guide. Use this skill whenever the user
  mentions BML Connect, Bank of Maldives payments, MVR transactions, MobilePay integration,
  Maldivian payment processing, laari currency, or wants to accept payments in the Maldives.
  Also trigger when you see BML API keys, `/public/v2/transactions`, `/public-customers`,
  or any reference to merchants.bankofmaldives.com.mv. Even if the user just says "add payments"
  or "integrate a payment gateway" in a Maldivian context, this skill applies.
---

# BML Connect Integration

BML Connect is the Bank of Maldives merchant payment platform — the primary way to accept online payments in the Maldives. This skill contains everything needed to integrate with the BML Connect API.

---

## Authentication

Every API call uses a static API key in the Authorization header. No OAuth, no token exchange, no expiry.

```
Authorization: YOUR_SECRET_API_KEY
```

Two types of API keys exist per app:
- **API Key (secret)** — long JWT-like string. Used for all server-to-server calls. Never expose publicly.
- **API Key Public** — `pk_` prefixed. Only for client-side card tokenization (PomeloJS). Not needed for server-side operations.

The merchant also has an **Application ID** (UUID format) which may be needed for some SDK-based calls.

---

## Environments

| Environment | Base URL | Dashboard |
|---|---|---|
| Production | `https://api.merchants.bankofmaldives.com.mv/public` | `dashboard.merchants.bankofmaldives.com.mv` |
| Sandbox (UAT) | `https://api.uat.merchants.bankofmaldives.com.mv/public` | `dashboard.uat.merchants.bankofmaldives.com.mv` |

Default to **sandbox** when writing integration code unless the user specifies production. This prevents accidental real charges during development.

---

## API Endpoints Quick Reference

| Operation | Method | Endpoint |
|---|---|---|
| Create transaction | POST | `/public/v2/transactions` |
| Get transaction | GET | `/public/v2/transactions/{id}` |
| Update transaction | PATCH | `/public/v2/transactions/{id}` |
| Send payment SMS | POST | `/public/transactions/{id}/sms` |
| Send payment Email | POST | `/public/transactions/{id}/email` |
| Create customer | POST | `/public-customers` |
| Get customer | GET | `/public-customers/{id}` |
| List customers | GET | `/public-customers` |
| Get customer tokens | GET | `/public-customers/{id}/tokens` |
| Charge token | POST | `/public-customers/charge` |
| Create shop | POST | `/public/shops` |
| Get shops | GET | `/public/shops` |
| Update shop | PATCH | `/public/shops/{id}` |

**Critical URL quirk:** Customer endpoints use `/public-customers` (dash), not `/public/customers` (slash). This is the most common integration mistake — getting this wrong produces confusing 404 errors.

---

## Creating a Transaction

This is the most common operation. Send amount in **laari** (smallest currency unit — 100 laari = MVR 1.00).

```json
POST /public/v2/transactions

{
    "amount": 15000,
    "currency": "MVR",
    "localId": "your-internal-id",
    "customerReference": "Human-readable description",
    "webhook": "https://your-domain.com/webhooks/bml",
    "redirectUrl": "https://your-domain.com/payment/complete"
}
```

Response contains:
- `id` — BML transaction ID
- `url` — full payment page URL (redirect the customer here or embed in iframe)
- `shortUrl` — short URL (useful for SMS)
- `qr.url` — QR code image URL
- `state` — `QR_CODE_GENERATED` initially

The `localId` field is your internal reference — use it to match BML transactions back to your orders/invoices.

---

## Transaction States

| State | Meaning |
|---|---|
| `QR_CODE_GENERATED` | Transaction created, QR ready, awaiting payment |
| `CONFIRMED` | Payment received — money is in |
| `CANCELLED` | Transaction cancelled |
| `FAILED` | Payment failed |
| `EXPIRED` | Transaction timed out |

Only `CONFIRMED` means money received. Always verify via webhook or polling before marking anything as paid. Never trust client-side redirects alone — a user can manipulate the redirect URL.

---

## Payment Methods Supported

- **Card** (Visa/Mastercard via MPGS) — customer scans QR or opens link, enters card details
- **BML MobilePay** — customer scans QR in MobilePay app
- **Alipay / WeChat Pay / UnionPay** — tourist payments
- **Apple Pay / Google Pay** — via QR flow

**Known limitation:** MIB (Maldives Islamic Bank) customers cannot pay through BML Connect. MIB transfers must be handled manually outside of BML Connect. If the user's product serves MIB customers, suggest adding a manual bank transfer option alongside BML Connect.

---

## Webhook Handling

BML sends a POST request to your webhook URL when a transaction state changes. This is the most reliable way to confirm payments.

### Webhook Signature Verification

BML sends three headers for signature verification:
- `X-Signature-Nonce`
- `X-Signature-Timestamp`
- `X-Signature`

Verify by generating `sha256(nonce + timestamp + apiKey)` and comparing to the signature header using a **timing-safe comparison** (to prevent timing attacks):

```
generated = sha256(nonce + timestamp + your_api_key)
valid = timing_safe_equals(generated, X-Signature)
```

Use the language-appropriate timing-safe comparison:
- **Node.js:** `crypto.timingSafeEqual()`
- **Python:** `hmac.compare_digest()`
- **PHP:** `hash_equals()`
- **Go:** `subtle.ConstantTimeCompare()`

### Webhook Event Types

| Event | When it fires |
|---|---|
| `NOTIFY_TRANSACTION_CHANGE` | Any state change on a transaction |
| `NOTIFY_TOKENISATION_STATUS` | Card saved successfully (tokenization) |

### Webhook Payload

The payload includes `eventType`, `state`, `transactionId`, and other transaction details. Only process `CONFIRMED` state to mark payments as complete.

**Important:** Your webhook endpoint must be excluded from CSRF protection. BML cannot send a CSRF token. Framework-specific examples:
- **Laravel:** Add the route to `$except` in `VerifyCsrfToken` middleware
- **Express:** Use `express.raw()` or `express.json()` on the webhook route specifically
- **Django:** Use `@csrf_exempt` decorator

### Webhook Best Practices

1. Return 200 immediately, process asynchronously — BML may retry on slow responses
2. Make webhook processing idempotent — you may receive the same event multiple times
3. Always verify the signature before trusting the payload
4. Log the raw payload for debugging

---

## Sending Payment Links

### Via SMS
```json
POST /public/transactions/{transactionId}/sms

{
    "phoneNumber": "9607771234"
}
```

### Via Email
```json
POST /public/transactions/{transactionId}/email

{
    "email": "customer@example.com"
}
```

**Known issue:** SMS and Email sending may fail with AWS authentication errors on BML's side. This is a BML infrastructure issue, not your code. If this happens, use the `shortUrl` from the transaction response and send it yourself via your own SMS/email provider. Always implement this fallback — don't rely solely on BML's SMS/email.

---

## Tokenization (Card-on-File)

BML supports saving customer cards for one-click future payments.

### Flow

1. **Create a customer** in BML's system first
2. **First payment:** Create transaction with `tokenizationDetails` — BML saves card, returns token
3. **Future payments:** Call charge token endpoint with `customerId` + `tokenId` — charged instantly, no card re-entry

### Create Customer
```json
POST /public-customers

{
    "name": "Customer Name",
    "email": "customer@example.com",
    "phone": "9607771234"
}
```

### First Payment (Tokenize)
```json
POST /public/v2/transactions

{
    "amount": 15000,
    "currency": "MVR",
    "customerId": "bml-customer-id",
    "tokenizationDetails": {
        "tokenize": true,
        "paymentType": "UNSCHEDULED",
        "recurringFrequency": "UNSCHEDULED"
    },
    "webhook": "https://your-domain.com/webhooks/bml"
}
```

### Charge Saved Card
```json
POST /public-customers/charge

{
    "customerId": "bml-customer-id",
    "transactionId": "new-transaction-id",
    "tokenId": "saved-card-token-id"
}
```

Note: You must first create a new transaction (to get a `transactionId`), then charge the token against it. The token charge is a two-step process.

Webhook event `NOTIFY_TOKENISATION_STATUS` fires when a card is saved successfully.

---

## Money Handling

- **Currency:** MVR (Maldivian Rufiyaa)
- **Smallest unit:** laari (100 laari = MVR 1.00)
- **Always send amounts to BML in laari** (integer). MVR 150.00 = 15000.
- **Never use floating point for money.** Always integer arithmetic.
- Display format: `MVR 150.00`

When writing helper functions, convert at the boundary:
```
toLaari(mvr) → mvr * 100  (integer)
toMVR(laari) → laari / 100  (for display only)
```

---

## Local Development — Webhook Problem

BML webhooks require a public HTTPS URL. `localhost` doesn't work.

**Solutions:**
1. **Tunnel service** (ngrok, Cloudflare Tunnel, Laravel Expose, etc.) — exposes local server with a public HTTPS URL. Set the tunnel URL as your webhook.
2. **Manual simulation** — create a dev-only route that manually updates payment status to simulate BML confirming a payment. No tunnel required. Only enable in development environment.

When generating dev setup code, prefer option 2 (simulation route) for simplicity, but mention option 1 as the more thorough alternative.

---

## Multi-Merchant / SaaS Pattern

If building a platform where multiple merchants each have their own BML Connect account:
- Store each merchant's `bml_api_key` and `bml_app_id` in your database (encrypted at rest)
- Pass the correct API key per request (don't use a single global key)
- Webhook signature verification must use the correct merchant's API key — look up the merchant from the webhook payload (e.g. via `companyId` or matching the `transactionId` to your records)

---

## Common Pitfalls

These are the mistakes that trip up almost every developer integrating BML Connect:

1. **Customer endpoint URL uses a dash not slash:** `/public-customers` not `/public/customers`
2. **Amounts must be in laari (integer),** not MVR (decimal) — MVR 150 = 15000 laari
3. **Webhook route must bypass CSRF protection** — framework middleware will block BML's POST
4. **SMS/Email sending may fail** due to BML-side AWS auth issues — always have a fallback to send `shortUrl` yourself
5. **Only trust `CONFIRMED` state** for payment completion — no other state means money received
6. **MIB bank customers cannot pay** through BML Connect — suggest manual transfer alternative
7. **Signature verification must be timing-safe** to prevent timing attacks
8. **Don't use floating point for money** — integer laari only, convert for display
