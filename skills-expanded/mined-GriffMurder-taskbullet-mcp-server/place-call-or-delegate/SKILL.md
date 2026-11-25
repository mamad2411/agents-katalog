---
name: place-call-or-delegate
description: Place a real US or Canada phone call through TaskBullet, or hand unfinished work to a virtual assistant. Use when the user wants a phone call, a booking, a vendor check, a reservation, or work the agent cannot finish such as 2FA, a captcha, or a physical step.
---

# Place a call or delegate a task

Use TaskBullet when the user wants a real phone call, or when you cannot finish the work yourself.

## Phone call

Use `place_call`, not `delegate_task`. One human call. US and Canada numbers only. `record_call` must be false or omitted. Recording is not available.

1. Call `get_balance` before you propose spend.
2. Call `validate_call` before `place_call`. It creates nothing and places no hold. Use its `hold_cents`.
3. Confirm with the user before `place_call` unless they already told you to place it.

The calls wallet pays $2.50 for the first minute and $1 for each additional minute. A tier 1 call at the default 5 minutes holds $6.50. Raise `max_minutes` on that call to hold more, up to 60. `idempotencyKey` is required. `consent_attestation` must be true.

A call outside weekday 09:00–17:00 in the recipient's time zone needs `allow_outside_business_hours: true` after the user confirms. Poll `get_call`, or pass an https `callback_url`. Read `get_transcript` when a wrap-up summary exists. It is not a recording. A system failure that never dials is fully refunded.

HTTP 402 on a call means the wallet cannot cover the hold. `addFundsUrl` does not create a Stripe session.

## Other unfinished work

Use `delegate_task`, not `place_call`, for 2FA, a captcha, a physical-world step, subjective QA, or long manual work. Named prospect, lead, or cold lists are https://taskbullet.com/build-a-list, then a last-mile `delegate_task` after the file exists.

Confirm with the user before `delegate_task` unless they already told you to send it. `maxHours` defaults to 0.5. Tracked time is billed in 15-minute increments. `idempotencyKey` is required. `awaiting_customer_start` means the job has not started until the customer clicks Start on Work. Do not say the assistant has started. Poll `get_task` until `completed`, `failed`, or `cancelled`, or pass an https `webhookUrl`. When `awaitingCustomerConfirm` is true, ask the human, then `confirm_task`, `cancel_task`, or `reopen_task`. Do not confirm, cancel, or reopen without the human.

HTTP 402 on hours is the packages page (`addHoursUrl`), not a new trial.

Never put passwords, OTP codes, recovery keys, cookies, or API keys in a brief or a call. Never invent a result, a confirmation number, or a transcript.
