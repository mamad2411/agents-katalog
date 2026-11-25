---
name: smb-customer-pulse
version: 1.0.0
description: Aggregate disputes, tickets, and reviews into weighted themes with trend and revenue-at-risk, then recommend the three highest-leverage fixes.
author: matrixx0070
tags: [small-business, customers, feedback, reviews, support, voice-of-customer]
capabilities: []
---

# Customer Pulse

## When to use
Use this when the owner wants to understand what customers are actually experiencing across scattered channels — support tickets, chargebacks/disputes, and public reviews — and turn the noise into a short list of fixes.

**Not for:** handling a single complaint end-to-end (use smb-handle-complaint) or drafting per-customer reply templates (use smb-customer-pulse-check). This is portfolio-level analysis, not a response tool.

## Method
1. **Set window and sources.** State the period and channels included (tickets, disputes, reviews, survey/NPS if any).
2. **Normalize the inputs.** For each item capture channel, date, sentiment, and the underlying issue in a common form.
3. **Cluster into themes.** Group by root issue (product, delivery, billing, support responsiveness, expectations). Decision point: weight by severity and frequency together — one chargeback can outweigh ten mild grumbles.
4. **Trend it.** Compare theme volume against the prior window to show what's rising or cooling.
5. **Quantify impact.** Estimate revenue at risk per theme (dispute amounts, churn signals, review-score effect).
6. **Pick three actions.** Recommend the three highest-leverage fixes, each with the theme it addresses and expected effect.

Do not reply to reviewers, issue refunds, or change policy on your own; present analysis and proposed actions for owner approval, since these touch customers and money.

## Example
30-day window, 42 items (tickets, disputes, Google reviews). Top theme: "late delivery" — 14 items, rising from 6 last month, ~$2,100 revenue at risk (2 disputes + 3 one-star reviews). Representative quote: "Third time my order came a week late." Do these 3: (1) audit the courier SLA, (2) add proactive delay notifications, (3) offer store credit to the 5 affected customers — owner to approve credits.

## Pitfalls
- **Counting frequency only.** A rare but high-dollar dispute can matter more than a common minor gripe — weight severity.
- **Cherry-picking quotes.** Pick a representative quote per theme, not the most dramatic one.
- **Acting unilaterally.** Refunds, replies, and policy changes are owner decisions, not this skill's.
- **No trend baseline.** A theme count means little without the prior window to compare against.

## Output format
```
Window: <period> | Sources: <list> | Volume: <n>
Themes:
| Theme | Count | Severity | Trend vs prior | Rev at risk |
Representative quotes:
  - <theme>: "<quote>"
Do these 3 things:
  1. Action — theme addressed — expected effect
Items needing owner decision (refunds, replies, policy):
```

## Reference

### Theme taxonomy (root-cause buckets)
Cluster every item into one primary root cause so themes are comparable across channels:

| Theme | What lands here | Typical fix lever |
|---|---|---|
| **Product/quality** | Defects, doesn't-work, wrong item, durability | QA, supplier, spec change |
| **Delivery/fulfillment** | Late, lost, damaged in transit, slow shipping | Carrier SLA, packaging, lead-time honesty |
| **Billing/pricing** | Overcharge, surprise fee, refund delay, chargeback | Pricing transparency, refund SLA |
| **Support responsiveness** | Slow reply, no reply, unhelpful, hard to reach | Staffing, hours, first-response SLA |
| **Expectations/accuracy** | Overpromised, misleading listing, scope creep | Clearer descriptions, set expectations upfront |
| **Ease/UX** | Confusing site/checkout, hard to book/return | Process/UX fix |
| **Staff/service** | Rudeness, professionalism, attitude | Coaching, hiring |

### Severity-weighted scoring (impact, not just count)
Rank themes by a weighted score, not raw frequency. Assign each item a severity weight, sum per theme:

| Severity | Examples | Weight |
|---|---|---|
| Critical | Chargeback/dispute, safety issue, threat to leave/churn, public 1-star | 5 |
| High | Formal complaint, refund demand, 2-star | 3 |
| Medium | Ticket with frustration, 3-star, repeat contact | 2 |
| Low | Mild grumble, passing mention, 4-star nit | 1 |

**Theme score = Σ(item severity weights).** One 5-weight chargeback (5) outweighs four low grumbles (4). Rank themes by score; show raw count alongside so nothing hides.

### Revenue-at-risk formula
Make the impact concrete in dollars:
`Rev at risk = disputed/refund amounts + (customers signaling churn × their annual value) + review-score effect`.
For the review-score effect, use the customer's or category's average order/annual value × the count of customers a bad public rating plausibly deters. Example: 2 disputes ($1,200) + 3 at-risk repeat customers (3 × $300 = $900) = **$2,100 at risk**. State assumptions; don't fabricate precision.

### Benchmarks to judge health against
- **CSAT:** 75-85% satisfied is typical; 90%+ is strong.
- **NPS:** above 0 is net-positive; 30+ good, 50+ excellent (varies by industry).
- **First response time:** email under 24h (ideally a few hours); live chat under 2 min; social DMs within a few hours.
- **Reviews:** a 4.0-4.5 star average with recent, responded-to reviews reads as trustworthy; below 4.0 actively deters buyers. Responding to reviews (good and bad) measurably lifts perception.
- **Complaint iceberg:** for every customer who complains, many more are silently unhappy — treat each surfaced item as representing several unheard ones.

### Response templates (owner sends, not the skill)
Draft these for the owner to review and send; never auto-send.
- **Public negative review:** "Hi [name], I'm sorry your [order/experience] fell short — that's not our standard. I'd like to make it right; please reach me directly at [contact]. — [Owner name]." Brief, owns it, moves the resolution offline, signed by a human.
- **Support-ticket recovery:** "Thanks for flagging this and I'm sorry for the trouble. Here's what happened [brief], here's the fix [action], and here's what we're doing so it doesn't recur." Acknowledge → explain → remedy → prevent.
- **Dispute/chargeback follow-up:** factual, documented, and routed through the owner given the money involved.
- **Positive review reply:** short, specific thanks referencing what they praised.

### The three-fixes discipline
Recommend exactly three actions, each mapped to a theme and an expected effect ("add proactive delay notifications → cuts late-delivery tickets and pre-empts 1-star reviews"). Prefer systemic fixes (process/SLA) over one-off apologies — solve the cause, not the instance. Three focused fixes beat a list of fifteen nobody executes.

### Owner-approval gate
This skill analyzes and proposes only. Replying to reviewers, issuing refunds or store credit, contacting affected customers, and changing policy all touch customers or money and are owner decisions. Present the themes, the dollars at risk, the draft responses, and the three fixes — then wait for the owner to approve before anything is sent or spent.
