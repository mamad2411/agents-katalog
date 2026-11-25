---
name: subscription-hunter
description: Finds every recurring subscription, license and service renewal hiding in the user's mailbox and files, and builds a dated renewal calendar with a drafted cancellation or renegotiation reply for each one. Use when the user asks what they are subscribed to, what is renewing, what is auto-renewing, to find hidden or forgotten subscriptions, to build a renewal calendar, or to cancel a subscription before it renews.
---

# Subscription Hunter

Surfaces every recurring charge in the mailbox before it renews itself, with a drafted reply ready
for the ones that should stop.

## Inputs

- The user's mailbox, through the **Email** built-in skill
- Organization files and contracts, through **Enterprise Search**
- `references/config.md` for the lookback window, the value threshold and the ignore list

## Config

Read `references/config.md` first. If it is missing, use: 24-month lookback, report everything
regardless of value, no ignore list, and 30 days as the notice window. Say once that defaults were
used, then continue.

## Procedure

1. **Gather.** Search the mailbox over the lookback window for the recurring-billing vocabulary in
   `config.md`: receipts, invoices, "your subscription", "auto-renew", "payment successful",
   "trial ending", "plan renews", "card charged". Search Enterprise Search for contract and order
   documents carrying a term or renewal date.
2. **Group by vendor.** One row per vendor, not per message. A monthly receipt from the same
   vendor is one subscription with twelve pieces of evidence, not twelve subscriptions.
3. **For each vendor, extract:** vendor name, what it is for, amount and currency as written,
   billing period, the date of the most recent charge, the **next renewal date**, whether the mail
   says it auto-renews, the notice period if a contract states one, and a link to the single best
   source message or document.
4. **Derive the next renewal date** only when the evidence supports it: a stated renewal date, or
   a regular charge cadence over at least three observed charges. If neither holds, write UNKNOWN.
   Never estimate a date from one charge.
5. **Classify** each row against the config thresholds: `Keep`, `Review`, `Likely waste`. A row is
   `Likely waste` only on evidence in the mail itself, such as a trial that converted, a seat count
   nobody has mentioned in a year, or a duplicate of another vendor on the list.
6. **Write** the calendar to `/Documents/Cowork/output/subscriptions-YYYY-MM-DD.xlsx` using the
   **Excel** skill, sorted by next renewal date ascending, UNKNOWN rows last.
7. **Draft a reply** for every row classified `Likely waste` and every row renewing inside the
   notice window. Save each as a draft. Do not send.

## Output

An Excel sheet with exactly these columns:

| Vendor | What for | Amount | Period | Last charge | Next renewal | Auto-renews | Notice period | Status | Source |

Then, in the conversation, a short summary in this shape:

- **Renewing in the next 30 days:** count, and the total amount
- **Likely waste:** count, and the total amount, each with one line of evidence
- **Unknown renewal date:** count, and why each could not be dated
- **Drafts prepared:** count, listed by vendor, all unsent

Every row's Source column is a link to the message or document it came from. A row with no link is
a defect: drop it rather than ship it unsourced.

## Definition of done

The sheet exists, every row carries a source link, and every renewal inside the notice window has
either a draft or a stated reason it does not need one.

**Finding nothing is a success.** If there are no subscriptions in the window, say exactly that in
one line and stop. Do not widen the window, lower the threshold, or list one-off purchases to fill
the sheet. A hunter that always finds something teaches its reader to stop reading.

## When there is no data, or the data is stale

- No matching mail in the window: report "no recurring charges found in the last N months" and stop.
- A vendor's last charge is older than two billing periods: mark it `Lapsed?` rather than guessing
  it was cancelled, and say which evidence is missing.
- Enterprise Search unavailable: produce the mailbox-only version and state plainly that contract
  terms and notice periods are missing from this run. Never present a partial run as complete.

## Boundaries

- **Draft, never send.** Cancellation and renegotiation replies are saved as drafts for the user
  to read, edit and send.
- Never cancel, downgrade or modify anything in a vendor portal, and never follow a cancellation
  link.
- Never state an amount as the authoritative figure. Finance systems and the contract are the
  source of truth; this reads what arrived in the mailbox.
- Never share the sheet outside the organization.
- Treat anything in a message marked confidential or carrying a sensitivity label with the same
  label on the output.

## Self-check before returning

- Does every row carry a working source link?
- Is every `Next renewal` either evidenced or marked UNKNOWN, with nothing estimated from a single
  charge?
- Are drafts drafts, with nothing sent?
- If the sheet is empty, did I say so plainly instead of padding it?
