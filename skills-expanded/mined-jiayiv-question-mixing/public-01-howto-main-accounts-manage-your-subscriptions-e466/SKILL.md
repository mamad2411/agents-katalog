---
name: manage-your-subscriptions
domain: accounts
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 1h-2h
risk: medium
prerequisites: [have-payment-method, accounts/log-in]
status: draft
last_verified: 2026-07-20
---

## Goal

You have a complete inventory of every recurring charge tied to your cards and app-store accounts, have cancelled the ones you do not want, and have calendar reminders set so no renewal surprises you again.

## Preconditions

- Access to your bank/credit-card statements (online banking or PDF exports).
- Access to the app-store accounts that bill on your behalf (Apple, Google Play) and any PayPal account.
- A password manager or notes app to record what you find, and a calendar you check.

## Steps

1. **Pull the last 12 months of statements, not just last month.** Annual subscriptions only appear once a year and are the ones people forget. → *Expect:* a full year of transactions open or exported for every card and payment account.
2. **Scan for recurring merchants.** Search statements for the same merchant name at a regular interval; flag anything monthly or yearly. Watch for cryptic descriptors (a media brand may bill as its parent company). → *Expect:* a written list of merchant, amount, and cadence for each recurring charge.
3. **Check the app-store hubs separately.** Apple: Settings > your name > Subscriptions. Google Play: Payments & subscriptions. These bill many apps under one line and are invisible on the merchant's own website. → *Expect:* the store's subscription list reconciled against your statement list, no orphans.
4. **Decide keep / cancel / downgrade for each row.** Mark trials whose free period is about to convert. → *Expect:* every inventory row tagged with a decision.
5. **Cancel through the same channel that bills you.** If Apple bills it, cancel in Apple, not on the merchant site (the merchant cannot stop an app-store charge). → *Expect:* you are in the correct cancellation surface for each item.
6. **Complete the cancel flow to the final confirmation, resisting the dark patterns.** Retention flows bury the real cancel button, offer "pause" instead, or push a discount. Keep clicking the option that actually ends billing. ⚠️ *Irreversible:* some cancellations forfeit remaining paid time immediately; read whether access runs to period end before confirming. → *Expect:* an on-screen "your subscription is cancelled" state plus a cancellation email.
7. **Save the confirmation email and note the access-until date.** → *Expect:* each cancellation has a dated proof stored.
8. **Add a calendar reminder 2-3 days before every renewal you kept.** Title it with the amount so you re-decide before the charge, not after. → *Expect:* one reminder per kept subscription on the calendar.

## Decision points

- Charge you do not recognize and cannot map to a service → treat as possible fraud: contact the card issuer, do not just ignore it.
- Free trial ending → cancel now; access usually continues to the trial end date, so cancelling early costs nothing.
- "Pause" offered instead of cancel → pause only delays billing; choose it only if you genuinely want the service back later.

## Failure modes & recovery

- **F1 Cancel button hidden behind a retention maze:** detect endless "are you sure" screens → look for a plain-text link, or search the help center for "cancel"; the flow always has a real endpoint.
- **F2 Charged again after cancelling:** detect a new statement line post-cancel → forward your dated confirmation email and request a refund; if refused, dispute the charge with your card issuer.
- **F3 Cancelled the wrong channel:** detect the merchant site says "cancelled" but the app store keeps billing → cancel again inside the app store that actually charges you.
- **F4 Lost access to an old email that receives the receipts:** detect no confirmation arrives → recover that mailbox first (see accounts/recover-a-password) so proofs are not stranded.

## Verification

Every recurring charge on 12 months of statements maps to a keep-or-cancel decision; each cancelled item has a dated confirmation and no charge after its access-until date; each kept item has a pre-renewal calendar reminder.

## Variations

- `us`: some states legally require an easy online cancel path ("click to cancel"); look for it if a flow traps you.
- Family plans: cancelling the organizer's plan removes access for all members; confirm who depends on it first.

## Safety & privacy

Medium risk because payment credentials and identity are involved. Never enter card details on a "cancellation" page reached from an unsolicited email; navigate to the service yourself. Keep the inventory list somewhere private, as it maps your accounts and spending.
