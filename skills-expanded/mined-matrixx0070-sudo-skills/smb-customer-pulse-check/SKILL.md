---
name: smb-customer-pulse-check
version: 1.0.0
description: Synthesize disputes, tickets, and reviews into a top-3 fixable-issues list, each with root cause and a ready-to-edit response template — never auto-sent.
author: matrixx0070
tags: [customer-success, support, reviews, analytics, retention]
capabilities: []
---

# Customer Pulse Check

## When to use
Use this when customer feedback is scattered across support tickets, payment disputes, and online reviews and you want the signal: what's actually hurting customers and what to say about it.

**Not for:** deep portfolio analysis with trend and revenue-at-risk (use smb-customer-pulse) or resolving one specific complaint (use smb-handle-complaint). This surfaces the top three fixable issues and drafts reply templates.

## Method
1. Gather recent disputes, support tickets, and reviews across your channels.
2. Cluster the feedback by theme (shipping, product defect, billing, response time) and count how often each appears.
3. Rank themes by frequency and severity to find the top three that are genuinely fixable. Decision point: exclude one-off complaints and things outside your control — focus on patterns you can act on.
4. For each issue, note the likely root cause and a concrete operational fix.
5. Draft a response template the owner can adapt for affected customers. Present everything for approval. Do not send any reply or post any public response — the owner approves all customer-facing messages.

## Example
Pulse summary: 28 items, sentiment trending down. Top issue: billing confusion — 9 mentions, medium-high severity. Example: "Got charged twice and no one replied for days." Root cause: no auto-confirmation on the retry path. Fix: add a payment-confirmation email + a same-day billing-reply SLA. Template: "Hi {name}, you're right — we double-charged you and were too slow to respond. The duplicate is refunded and here's what we changed... " — owner edits before it goes out.

## Pitfalls
- **Fixing one-offs.** A single angry review isn't a pattern; require repetition before it makes the top 3.
- **Templates that dodge fault.** A response that won't own a real error reads as corporate and worsens churn.
- **Skipping root cause.** A reply without an operational fix means the same complaints return next month.
- **Auto-sending.** Every customer-facing message waits for owner approval or edits.

## Output format
```
Pulse summary: volume <n> | sentiment trend <up/flat/down>
Top 3 issues:
  1. <theme> — frequency <n> — severity <H/M/L>
     Example quote: "..."
     Root cause: ___
     Suggested fix: ___
     Response template: "<ready-to-edit draft>"
"Approve or edit these templates before anything goes to a customer."
```

## Reference

### Feedback taxonomy — cluster into these themes
Consistent categories make patterns visible across channels. Tag every item to one primary theme:
- **Product/quality** — defects, doesn't-work, poor durability, missing features.
- **Shipping/fulfillment** — late, damaged, wrong item, tracking gaps.
- **Billing** — double charges, surprise fees, refund delays, subscription confusion.
- **Support experience** — slow response, unhelpful, had to repeat themselves, rude.
- **Onboarding/usability** — confusing setup, hard to find things, unclear docs.
- **Pricing/value** — too expensive, unclear what's included.
- **Expectation gap** — worked as designed but not what they expected (a marketing/comms signal).

### Severity and prioritization scoring
Rank the top 3 fixable issues by a simple **priority score = frequency × severity × fixability**.
- **Frequency:** count of mentions in the window (require ≥ 3 to qualify as a pattern, not a one-off).
- **Severity (1-3):** 1 = annoyance, 2 = blocks a task / real cost to customer, 3 = churn/safety/reputational.
- **Fixability (1-3):** 3 = clear operational fix you control, 2 = fixable with effort, 1 = structural/outside control.
Exclude anything with fixability 1 or a single mention from the top-3 — focus attention where action changes outcomes.

### Sentiment and health signals worth reading
- **Trend, not level** — 12% negative this month vs 6% last is the story, not the raw 12%.
- **Emerging spikes** — a theme that jumped from 0 to several mentions in one week beats a chronic low-level gripe for urgency.
- **CSAT** = % positive responses (rating ≥ 4/5); ~75-85% is a common healthy band.
- **NPS** = % promoters (9-10) − % detractors (0-6); positive is fine for SMBs, 30+ is strong, 50+ is excellent.
- **Review-star drift** — a moving 30-day average of new reviews catches decline the lifetime average hides.
- **Support volume per 100 orders / active customers** — rising ticket rate is a leading churn indicator.

### Root-cause discipline
For each top issue, push past the symptom with a quick 5-whys and separate the *incident* from the *system*. "Customer double-charged" → why? retry path had no idempotency guard → the fix is the guard plus a confirmation email, not just refunding this one customer. Always pair the top issue with the **operational fix + owner**, or the same theme returns next cycle.

### Response templates by theme (owner edits before send)
Spine: **Acknowledge specifically → Own the error → State the fix already made → Invite them back.** Avoid corporate hedging.
- **Billing:** "Hi {name}, you're right — we {double-charged/mis-billed} you and were too slow to fix it. The {amount} is refunded (clears in {days}), and we've added {confirmation email / SLA} so it can't repeat. Sorry for the hassle."
- **Shipping:** "Hi {name}, your order arriving {late/damaged} isn't the experience we want. {Replacement/refund} is {status}, and we've changed {carrier/packaging}."
- **Product/quality:** "Hi {name}, thanks for flagging the {issue} — that's a real defect, not you. Here's the fix {…}, and we've addressed {root cause} in the next batch."
- **Support experience:** "Hi {name}, waiting {duration} for a reply isn't acceptable and I'm sorry. I've {change}, and here's my direct line if it happens again."
- **Public review reply (keep short, move money offline):** "Thank you for the honest feedback, {name} — you're right about {issue}, and we've {fix}. I've sent a private message to make this right." Never negotiate refunds in public.

### Cadence
Run weekly for high-volume or fast-moving businesses, monthly otherwise. Compare each run against the prior to confirm fixes are landing — a resolved theme should shrink or disappear. If a "fixed" issue reappears, the operational change didn't hold; reopen it rather than re-drafting a reply.
