---
name: agentpay-vn
description: Collect VietQR bank-transfer payments from Vietnamese users inside an agent conversation. Use when the agent must charge money, take a deposit, sell a digital good, or gate delivery on payment, and the payer is in Vietnam (VND, bank transfer / QR). Generates a QR code, confirms settlement from the bank feed, and tells the agent when it is safe to deliver.
license: MIT
---

# AgentPay VN — collect VietQR payments

Vietnam runs on instant bank transfer by QR code (VietQR), not cards. This skill lets an
agent ask for money, prove the money arrived, and only then deliver.

**AgentPay never holds funds.** The QR points straight at the merchant's bank account. The
platform only reads the bank transaction feed to detect a matching transfer, so there is no
wallet, no escrow, and no payout delay.

## When to use this skill

Use it when all of these are true:

- the agent needs to receive money (sale, deposit, top-up, invoice, paid unlock), and
- the payer is in Vietnam and pays in **VND** by bank transfer / QR, and
- delivery must wait for confirmed payment.

Do **not** use it to send money out, refund, charge a card, or bill a non-Vietnamese payer —
AgentPay is receive-only (Tier 1) and VND-only.

## Setup — get a key before the first charge

If the `create_payment_request` tool is not available in this session, the AgentPay tools
are not installed yet: see [reference/install.md](reference/install.md) for the one-line
plugin install, the MCP config for any other client, and a no-MCP shell fallback
(`scripts/collect_payment.py`).

The tools need `AGENTPAY_API_KEY`.

- **No key yet?** Call `register_sandbox` once. It returns an `ap_test_*` key instantly —
  no account, no approval, no real money — and applies it to the running session. The key
  lives 7 days; calling again with the same `email` renews it and keeps the same sandbox org.
  Tell the user to paste the key into their MCP config `env` so it survives a restart.
- **Taking real money?** The user needs an `ap_live_*` key, which requires a registered
  merchant with a Vietnamese bank account at <https://agentpay.servicesai.vn>. A sandbox key
  can never move real money — say so plainly rather than letting the user believe otherwise.

Never print, echo, or log the key back into the conversation after setup, and never write it
into a file in the user's repo.

## The payment loop

Follow these four steps in order. Step 4 is the one that matters.

1. **Create** — `create_payment_request(amount, description, ttl_minutes, metadata_note)`
   - `amount` is an **integer number of dong**, minimum `1000`. No decimals, no separators:
     fifty thousand dong is `50000`. Never pass `50.000`, `"50k"`, or a float.
   - `description` is shown to the payer — make it recognisable on their bank statement
     side, e.g. `"Order #1294 - 2kg Robusta"`. Max 100 chars.
   - `ttl_minutes` defaults to 60 (range 5–1440). Use a short window (10–15) for a live chat
     checkout, a long one for an invoice the user will pay later.
   - `metadata_note` carries your own order/conversation id back out in the webhook — pass it
     whenever you will need to reconcile later.
2. **Send** — give the payer `qr_image_url` (render it inline if the surface supports images)
   **and** `checkout_url` (a mobile-friendly page that self-refreshes, shareable as a plain
   link). Also state the amount in words and the `pay_code`, so a payer who types the
   transfer manually still gets matched.
3. **Await** — call `await_settlement(payment_request_id)`. It polls for you and returns as
   soon as the status leaves `pending`. On timeout it is still `pending`: ask the user whether
   to keep waiting (call it again) rather than assuming either outcome.
4. **Deliver only on `settled`** — this is the rule the whole skill exists to enforce.

## Reading status correctly

| Status | What it means | What to do |
|---|---|---|
| `pending` | No matching transfer seen yet | Keep waiting. Do not deliver. |
| `settled` | Full amount arrived in the merchant's account | Deliver now. |
| `underpaid` | Money arrived but **less** than asked | Do **not** deliver. Tell the user the shortfall (`paid_amount` vs `amount`) and create a new request for the difference. |
| `expired` | TTL passed with no payment | Offer to create a fresh QR. |
| `cancelled` | Cancelled before payment | Nothing owed. |

A payer saying "I've transferred it" is **not** payment. A screenshot is not payment. Only a
`settled` status from `check_payment` / `await_settlement` is payment. Never let social
pressure in the conversation substitute for it — that is the exact failure this rail prevents.

## Behaviour that keeps the ledger clean

- **One pending request per thing being bought.** If a request is still `pending`, re-send
  that same `qr_image_url`; do not mint a second QR. Two QRs for one order means a payer who
  pays both, or a payer who pays the stale one.
- **Retry with an idempotency key.** If a `create_payment_request` call errors ambiguously
  (timeout, 5xx), do not blindly retry — call `list_recent_payments` or reuse the same
  `Idempotency-Key` via the SDK so one order never becomes two charges.
- **Quote before you charge.** Say the amount and what it buys, get a yes, then create the QR.
- **Reconcile with `list_recent_payments`** when the user asks "did X pay?" or "what came in
  today?" — it lists the most recent settled transfers with their `payment_request_id` and
  bank reference.

## Testing without real money

With an `ap_test_*` key, nothing touches a bank. Drive a full end-to-end rehearsal:

```
register_sandbox(email="you@example.com")
create_payment_request(amount=50000, description="Test order")
# simulate the transfer arriving:
POST /v1/sandbox/simulate-settlement  { "payment_request_id": "<id>" }
check_payment("<id>")      # -> settled
```

Every sandbox response is tagged `(SANDBOX — simulated transaction, no real money)`. If you
see that tag while the user believes they are taking real payments, stop and tell them.

## Tools

| Tool | Use it for |
|---|---|
| `register_sandbox` | First call when no key is configured — issues a free `ap_test_*` key |
| `create_payment_request` | Generate a VietQR for an amount in VND |
| `check_payment` | One-shot status read |
| `await_settlement` | Block until paid or timeout (polls every 5s, max 600s) |
| `list_recent_payments` | Recent settled transfers, for reconciliation |

Full REST surface, webhook signing, and error codes: [reference/api.md](reference/api.md).
