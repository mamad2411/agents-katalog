---
name: appotapay-payment
description: >-
  Integrate the AppotaPay standard payment flow: create a payment order, redirect the customer to the
  hosted checkout, receive and verify the IPN/redirect callback, check transaction status, and issue
  refunds. Use when the user wants to accept online payments via AppotaPay (ATM/Visa/Master/JCB/e-wallet/QR),
  build an AppotaPay checkout, handle AppotaPay payment notifications/callbacks, verify a payment result,
  poll transaction status, or refund an AppotaPay transaction. Requires appotapay-auth for the JWT.
license: MIT
metadata:
  version: "0.1.0"
  source: https://docs.appotapay.com/payment/
---

# AppotaPay standard payment flow

Always build the `X-APPOTAPAY-AUTH` JWT first — see the **appotapay-auth** skill.
Amounts are integers in **VND**; `currency` is always `"VND"`.

> **Verify against live docs.** The `references/*.md` here are an offline snapshot and may lag the
> real API. Before finalizing endpoints/fields/codes in generated code, fetch the current page and
> reconcile (live doc wins): create `…/llms-v2.0-payment-payment-full.txt`, result/IPN
> `…/llms-v2.0-payment-payment-result-full.txt`, status `…/llms-v2.0-payment-payment-status-full.txt`,
> refund `…/llms-v2.0-payment-refund-full.txt`, codes `…/llms-v2.0-payment-payment-code-full.txt`
> (base `https://docs.appotapay.com`). Index of all pages: `…/llms.txt`. See router `references/live-docs.md`.

## The flow (server-side)

```
1. Create order   →  POST /api/v2/orders/payment        → returns payment.url (+ qrCode)
2. Redirect       →  send customer to payment.url
3. Customer pays  →  on the AppotaPay hosted page
4. IPN (POST)     →  AppotaPay calls your notifyUrl with { data, signature, time }
                     → VERIFY signature, decode data, mark order, reply {"status":"ok"}
5. Redirect (GET) →  customer returns to your redirectUrl with the same { data, signature, time }
                     → VERIFY signature, show result (do NOT fulfill on this alone)
6. Reconcile      →  GET /api/v2/orders/transaction?referenceId=...  → confirm final status
   (optional)        Refund: POST /api/v2/transaction/refund
```

> **Trust model:** treat the IPN as the source of truth, but always re-check via the status API
> before fulfilling. The redirect is for UX only — it can be tampered with or replayed.

## 1) Create payment — `POST /api/v2/orders/payment`

Headers: `X-APPOTAPAY-AUTH`, `Content-Type: application/json` (optional `X-Request-ID`, `X-Language`).

Minimal body:
```json
{
  "transaction": {
    "amount": 10000,
    "currency": "VND",
    "bankCode": "VCB",
    "paymentMethod": "ATM",
    "action": "PAY"
  },
  "partnerReference": {
    "order": { "id": "5f61cf4f41e2b", "info": "test thanh toan", "extraData": "" },
    "notificationConfig": {
      "notifyUrl": "https://your.site/ipn",
      "redirectUrl": "https://your.site/redirect"
    }
  }
}
```

Success (`200`) returns `transaction.transactionId`, `transaction.status` (`pending`), and
`payment.url` (the hosted checkout link; may also include `payment.qrCode`). Send the customer to
`payment.url`. See `references/endpoints.md` for every request/response field, and `references/codes.md`
for `paymentMethod`, `action`, and `bankCode` values.

## 2) Verify the IPN / redirect callback — REQUIRED

Both callbacks send `{ data, signature, time }`. Verify before trusting:

```
expected = HMAC_SHA256(data, SECRET_KEY)        // data = the raw string, unchanged
if !constant_time_equals(expected, signature): reject (HTTP 400)
info = json_decode(base64_decode(data))         // the transaction object
```

Then check `info.transaction.status === "success"` **and** that `orderAmount` matches your order
before fulfilling. Respond to the IPN with HTTP `200` and body `{"status":"ok"}` — otherwise
AppotaPay retries up to 3 times, 5 minutes apart. IPN is sent only for successful transactions.

Runnable verifiers (read the one for the project's language):
- `scripts/verify-ipn.mjs` (Node), `scripts/verify_ipn.py` (Python), `scripts/verify-ipn.php` (PHP).

Full field list & status codes: `references/ipn.md`.

## 3) Check status — `GET /api/v2/orders/transaction`

Query: `referenceId` (required) and `type` = `TRANSACTION_ID` (AppotaPay id, default) or
`PARTNER_ORDER_ID` (your order id). Returns the transaction with `status` ∈
`pending | processing | success | error`. Use this to reconcile.

## 4) Refund — `POST /api/v2/transaction/refund`

Body: `partnerRefId` (unique), `transactionId`, `amount` (min 1000), `currency` `"VND"`, `reason`.
Refund `status` ∈ `pending | processing | success | error`. Not all providers support auto/partial
refunds — see the provider table in `references/endpoints.md`.

## Sandbox

Base URL `https://gateway.dev.appotapay.com`. Test credentials and test cards are in
`references/sandbox.md`.

## Checklist before go-live

- [ ] JWT built server-side, short `exp`, unique `jti` (appotapay-auth).
- [ ] `notifyUrl` is a public HTTPS endpoint that verifies `signature` and replies `{"status":"ok"}`.
- [ ] Order fulfillment gated on **status API = success** + amount match, not on the redirect.
- [ ] `SECRET_KEY` only in server env; not in client bundles or git.
- [ ] Switched base URL to production and confirmed IP allow-list with AppotaPay.
