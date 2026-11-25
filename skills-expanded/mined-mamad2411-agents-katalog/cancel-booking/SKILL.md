---
name: cancel-booking
description: Cancel an existing hotel booking. Use this skill when the user explicitly wants to cancel their reservation — phrases like "cancel my booking", "cancel reservation BK_xxx", "I don't need the hotel anymore", "refund my booking". This is a destructive action; always confirm with the user before calling, and warn if the cancellation is past the free-cancellation deadline.
license: MIT
---

# cancel-booking

Cancel a hotel booking. **Destructive action — confirm first.**

## When to use

The user explicitly asks to cancel:

- "Cancel BK_2026_05_001"
- "I want to cancel my hotel"
- "Refund my booking"

For checking status only, use `manage-booking` instead.

## Prerequisites

1. `bookingId`
2. Last name on the booking
3. Email on the booking

If unsure whether the booking is still cancellable for free, run `manage-booking` first to see the `cancellationDeadline` and `isCancellable` flag.

## Pre-cancellation confirmation

Before cancelling, especially if the free-cancellation window has passed:

> About to cancel **BK_2026_05_001** — Park Hyatt Tokyo, May 1–5.
> ⚠️ Free cancellation expired on April 29. A cancellation fee may apply.
>
> Are you sure you want to cancel? (yes/no)

If still inside the free window, a lighter confirmation is fine:

> About to cancel **BK_2026_05_001** — Park Hyatt Tokyo, May 1–5.
> You're inside the free cancellation window — no fee.
>
> Confirm? (yes/no)

Only proceed after the user says yes.

## How to call

```bash
npx @tvl-justin/travel-cli@latest cancel \
  --booking-id "<bookingId>" \
  --last-name "<lastName>" \
  --email "<email>"
```

## Output

```json
{
  "bookingId": "BK_2026_05_001",
  "status": "CANCELLED",
  "refundAmountUSD": 1800,
  "refundEta": "5-7 business days",
  "cancellationFeeUSD": 0
}
```

## Presenting to the user

> ✅ Booking **BK_2026_05_001** cancelled.
> Refund of **$1,800 USD** will appear on your card in 5–7 business days.
> No cancellation fee.

If a fee was charged:

> ✅ Booking cancelled.
> Refund: $1,440 USD (a $360 cancellation fee was applied because we're past the free-cancellation deadline).

## Errors

- `404 Not Found` — Booking ID not found, or last name / email mismatch.
- `409 Already Cancelled` — Booking was already cancelled. Tell the user, don't retry.
- `Network error` — Tell the user the cancellation didn't go through and ask whether to retry.
