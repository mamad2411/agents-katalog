---
description: Use when the operator's site does something unexpected — a challenge, a login failure, a page that will not load, a suspended market — to decide between retrying, reporting, and stopping.
---

# Handling blockers

## Stop immediately, always

These are not obstacles to work around. They are the system asking for a person.

- A CAPTCHA or "verify you are human" page of any kind
- A verification code, one-time password, authenticator prompt or two-factor step
- "Confirm it's you", a device check, or a security question
- An account that is suspended, restricted, locked, or under review
- An identity or age verification request
- A self-exclusion or responsible-gambling block

Report it as `needs_human` with what you saw. Then stop that line of work
entirely.

Do not: solve it, wait for it to disappear, reload hoping for a different page,
try a different URL to the same destination, try the mobile site, or ask for
another attempt. Every one of those is an attempt to bypass a protection, and
the system does not do that — not because it would fail, but because it is not
ours to bypass.

## Retry once, then report

These are ordinary flakiness. One retry is reasonable; a second is not.

- A page that timed out or failed to load
- A blank page where content was expected
- A cookie or promo dialog covering the page — dismiss it and continue
- An element that was not there yet — take a snapshot and look again

If the retry fails, report what happened and move on to the next piece of work.
One broken page does not cancel everything else you were asked to do.

## Report and continue

These are answers, not errors:

- The operator does not offer this match
- The market is not offered for this event
- The selection is suspended or greyed out
- The price is below the approved minimum

Report the specific reason and move to the next item. Do not substitute a
different market, a different selection or a different match.

## Never retry

- A submission whose outcome was unknown. It may have worked. Report `unknown`.
- A bet whose claim already exists. It was already attempted.
- Anything at all after a protection challenge.

## Login trouble

If the login form is not where it should be, or the fields cannot be found, the
site's labels have probably changed. Report exactly what you saw on the page —
the visible label text near the fields — so the configuration can be corrected.
Do not try to guess your way in with different values.

If the credentials are rejected, report that once. Do not try again: a second
failed attempt on a betting account is how a lockout starts.
