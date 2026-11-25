---
name: book-hotel
description: Book a hotel package and pay with USDC via the x402 payment protocol. Use this skill when the user explicitly wants to confirm and pay for a hotel — phrases like "book it", "reserve hotel #2", "go ahead and book the Park Hyatt", "confirm my reservation", "pay for this hotel". This is a real-money on-chain action; always confirm with the user before calling, run search-hotel or search-room first to get a valid packageId, and ensure the user has an authenticated wallet with sufficient USDC.
license: MIT
---

# book-hotel

Create a hotel reservation and pay with USDC. The payment is handled automatically via the **x402 protocol** — your travel API responds with HTTP 402 Payment Required, the agent's wallet pays in USDC, and the booking confirms.

**This is a real on-chain financial transaction.** Proceed carefully.

## When to use

The user has chosen a specific package and explicitly asks to book it:

- "Book the Park Hyatt for me"
- "Reserve option 2"
- "Confirm and pay for this hotel"
- "Go ahead with this one"

Do NOT use this skill speculatively. Only when the user explicitly approves payment.

## Prerequisites

You need ALL of these before calling:

1. **A valid `packageId`** from `search-hotel` or `search-room`
2. **The `sessionId`** from that same search session
3. **Guest details**: first name, last name, email (the user must give these — never invent)
4. **An authenticated Coinbase wallet** — if not, run the `authenticate-wallet` skill first (from the `coinbase/agentic-wallet-skills` package)
5. **Sufficient USDC in the wallet** — if balance is too low, run the `fund` skill first
6. **Explicit user confirmation** of package, total price, and dates

If any of these are missing, ask the user or chain to the relevant skill — do not skip ahead.

## Wallet setup check

Before booking, verify wallet status. Quick check:

```bash
npx awal@latest balance
```

If the user is not authenticated, this returns an auth error → trigger `authenticate-wallet` skill.
If USDC balance is below the booking total, trigger `fund` skill.

## Pre-booking confirmation

Always summarize and confirm before paying. Example:

> About to book and pay:
> - **Park Hyatt Tokyo**, Park Deluxe King with breakfast
> - May 1–5 (4 nights), 2 adults
> - **Total: 1,800 USDC** (paid from your Coinbase wallet)
> - Free cancellation until April 29
> - Guest: Nguyen Van A, guest@example.com
>
> Confirm? (yes/no)

Only run the pay command after the user says yes (or equivalent). If the user already explicitly authorized booking with all the above info in the same turn, you can proceed without re-asking.

## How to call

Use `awal x402 pay` to call the booking endpoint. The CLI handles 402 → sign → retry automatically.

The booking endpoint splits inputs across two places:
- **Query string** (`-q` flag): `package_id`, `session_id` — the package the user picked and the search session it came from.
- **Request body** (`-d` flag): the `contact` object, plus the hardcoded `reward_wallet` and `agent_id` (see below).

```bash
npx awal@latest x402 pay https://qpgdy2kn7v.ap-southeast-1.awsapprunner.com/m2m-payment/book \
  -X POST \
  -q '{"package_id":"<packageId>","session_id":"<sessionId>"}' \
  -d '{
    "contact": {
      "given_name": "<first>",
      "sur_name": "<last>",
      "email": "<email>",
      "phone": "<phone>"
    },
    "reward_wallet": "0x8D91B9c9920BD2E056989C2E80F14a20557B4773",
    "agent_id": "1996"
  }'
```

Note the snake_case field names (`package_id`, `session_id`, `given_name`, `sur_name`, `reward_wallet`, `agent_id`) — the booking endpoint expects this exact shape. The `contact` object is required and `phone` is part of it. Do NOT put `package_id` / `session_id` in the body — they must be query params.

### `reward_wallet` and `agent_id` (hardcoded — do NOT change)

These two fields identify the **skill author** so the booking system can attribute rewards. Always send these exact values in every booking call:

- **`reward_wallet`**: `0x8D91B9c9920BD2E056989C2E80F14a20557B4773`
- **`agent_id`**: `"1996"`

Both fields are required at the top level of the request body (siblings of `contact`). Do NOT ask the user for them and do NOT substitute the user's wallet address.

For the full rationale and instructions on changing these when forking the skill, see the [Configuration section in the README](../../README.md#configuration).

### Safety: cap maximum payment

To prevent unexpected overcharge (e.g. if the API returns a wrong amount), pass `--max-amount` in micro-USDC (1 USDC = 1,000,000 micro-units):

```bash
  --max-amount 1850000000   # caps payment at 1,850 USDC for an 1,800 USDC booking
```

Always set `--max-amount` to roughly the expected total + a small buffer (5%).

### Full example

```bash
npx awal@latest x402 pay https://qpgdy2kn7v.ap-southeast-1.awsapprunner.com/m2m-payment/book \
  -X POST \
  -q '{"package_id":"e47otEJtYeZYblF9","session_id":"6kVmPYwZhQJewNTp"}' \
  -d '{"contact":{"given_name":"Justin","sur_name":"Ta","email":"justin@example.com","phone":"+84336657091"},"reward_wallet":"0x8D91B9c9920BD2E056989C2E80F14a20557B4773","agent_id":"1996"}' \
  --max-amount 1850000000
```

## Output

On success, the CLI prints both the payment receipt and the booking confirmation. The booking response is in the body:

```json
{
  "bookingId": "BK_2026_05_001",
  "status": "CONFIRMED",
  "hotelName": "Park Hyatt Tokyo",
  "checkIn": "2026-05-01",
  "checkOut": "2026-05-05",
  "totalPriceUSD": 1800,
  "cancellationDeadline": "2026-04-29T23:59:00Z",
  "paymentTxHash": "0xabc...",
  "confirmationEmail": "guest@example.com"
}
```

The transaction hash (`paymentTxHash`) appears in the `X-PAYMENT-RESPONSE` header — `awal` will surface it in the output.

## Presenting confirmation

> ✅ Booked! Confirmation **BK_2026_05_001**.
> Park Hyatt Tokyo · May 1–5 · 1,800 USDC paid
> Tx: 0xabc...def (view on basescan)
> Free cancellation until **April 29, 2026**.
> Confirmation email sent to guest@example.com.
>
> Save your booking ID — you'll need it to manage or cancel.

## Error handling

- **`402 with amount > --max-amount`** — Booking total exceeds the safety cap. Stop, tell the user the actual amount, and ask whether to proceed with a higher cap.
- **`Insufficient USDC balance`** — Trigger the `fund` skill to top up, then retry.
- **`Wallet not authenticated`** — Trigger the `authenticate-wallet` skill, then retry.
- **`Payment was authorized but rejected by server`** / **`X402 submission failed`** / **any post-authorization timeout** — DO NOT retry the `pay` command blindly. The on-chain settle and booking may have already succeeded — the agent only lost the response. Run the recovery flow below.
- **`Package no longer available`** (before payment) — Re-run `search-hotel` or `search-room` to refresh; the `sessionId` may also have expired.
- **`Session expired`** — Re-run search to get a new `sessionId`.
- **Network error mid-payment** — Same as the post-authorization timeout case above: run the recovery flow before doing anything else.

## Recovery: payment authorized but agent reports failure

The most common false-failure mode: `awal x402 pay` signs the payment authorization, the server settles it on-chain AND completes the booking, but the response doesn't reach the agent in time → CLI throws `Payment was authorized but rejected by server`. Money is gone, booking exists, but the agent thinks it failed. Blindly retrying causes a **double charge**.

When you see any of the errors flagged above, do this **before** mentioning failure to the user:

### Step 1 — Run `travel-cli book-status`

Use the same `package_id` and `session_id` you just tried to book with. No x402, no payment, no auth required:

```bash
npx @tvl-justin/travel-cli@latest book-status \
  --package-id "<packageId>" \
  --session-id "<sessionId>"
```

The CLI always emits JSON of shape `{ httpStatus, body, interpretation }`.

### Step 2 — Interpret the response

Branch on `httpStatus`:

| `httpStatus` | `body` | Meaning | Action |
|---|---|---|---|
| `200` | `{ "status": "completed", "transaction": "0x…", "bookingId": "BK_…", … }` | Booking already succeeded. Agent timed out, but money was charged and the room is reserved. | Treat as success. Present confirmation to the user using this body (same shape as a normal happy-path response). **Do not retry payment.** |
| `202` | `{ "status": "in_progress", "retry_after_ms": <N> }` | Server is still settling/booking. | Wait `body.retry_after_ms` (cap at ~10s per poll), then re-run `book-status`. Poll up to ~6 times. If still in_progress, tell the user a confirmation email will follow and to check `awal wallet history`. |
| `404` | `{ "status": "not_found" }` | Nothing happened server-side — the failure is real. | Safe to retry the original `awal x402 pay` (or surface the original error to the user). |
| `5xx` | error | Recovery endpoint itself is down. | Tell the user "I can't confirm whether the booking went through. Please check your email — Travala always sends a confirmation on success — and check `awal wallet history` for the transfer. Do not retry yet." |

The `interpretation` field on the JSON output is a human-readable summary of the same mapping above — useful for surfacing to the user, but always branch your control flow on `httpStatus`.

### Step 3 — On 200 (recovered)

Present the result the same way as a normal success, but mention the recovery so the user understands what happened:

> ✅ Booked! Confirmation **BK_2026_05_001**.
> (The CLI initially reported a failure, but the booking actually went through — recovered from the server. No double charge.)
> Park Hyatt Tokyo · May 1–5 · 1,800 USDC paid
> Tx: 0xabc...def (view on basescan)
> Confirmation email sent to guest@example.com.

### What NOT to do

- ❌ Re-run `awal x402 pay` after a post-authorization error without first running `travel-cli book-status`.
- ❌ Tell the user "booking failed" before running `travel-cli book-status`. The booking is far more likely to have succeeded than not.
- ❌ Manually craft a refund request — the server has no refund flow for already-completed bookings (a successful booking is not a failure to refund).

## Critical rules

- Never invent guest details. If the user hasn't given them, ask.
- Never call `awal x402 pay` without explicit approval in this turn or a recent turn.
- Always set `--max-amount` to prevent runaway charges.
- If the user changes their mind ("wait, show me option 3"), do NOT pay — go back to `search-room`.
- Never expose private keys or wallet seed phrases. The agent only signs through `awal`; keys stay in Coinbase's secure infrastructure.
