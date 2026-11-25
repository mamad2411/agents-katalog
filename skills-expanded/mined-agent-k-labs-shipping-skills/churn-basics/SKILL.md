---
name: churn-basics
description: Diagnose and reduce early churn for a small SaaS — measure the real churn rate, find where users drop, run exit interviews that get answers, and ship the three highest-leverage retention fixes. Use when the user asks "users sign up and disappear," "how do I reduce churn," "people cancel after one month," "measure retention," or has paying users but revenue is flat.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Churn Basics

At small scale, churn is not a dashboard problem — it's a "talk to the five people who left" problem. Acquisition fills the bucket; this skill patches the holes. It's for products with real users (even 10) where signups aren't turning into a growing base.

## Context

Read `product-context.md` if present. Otherwise ask for:
1. Product, pricing model, and what the core value action is
2. Current numbers: signups/mo, active users, paying users, cancellations
3. What analytics exist (events table, PostHog, Stripe) — even rough
4. Any known complaints or cancellation reasons so far

## Process

### 1. Measure it honestly (30 minutes)

Two numbers, monthly:
- **Customer churn** = customers lost in month ÷ customers at start of month
- **Activation-adjusted retention** — of users who signed up 30 days ago, how many did the core action in the last 7 days?

Early-stage reality check: 5–10% monthly customer churn is normal for young SaaS; >15% means the product isn't delivering its promise yet. With < 50 customers, ignore percentage noise — count *people* and talk to each one.

### 2. Find the drop point

Users churn at predictable cliffs — locate which one is yours:

| Cliff | Symptom | Likely cause |
|-------|---------|--------------|
| Never activated | Signed up, never did the core action | Onboarding / unclear first step |
| Used once, gone | Did it once, never returned | Value was a novelty, not a workflow |
| Gone at first invoice | Cancelled when billing hit | Price ≠ perceived ongoing value |
| Slow fade | Usage decayed over weeks | Product lost to habit competition |

Pull the last 10 churned users and tag each with a cliff. The most common tag is the work queue.

### 3. Exit interviews that get answers

Email every cancellation within 24 hours. Three rules: one question, reply-to goes to the founder, no survey link.

```
Subject: quick question (no win-back attempt)

Saw you cancelled [Product] — totally fine, and I won't try to talk you out of it.
One question so I can fix it for the next person:
what was the moment you decided it wasn't worth keeping?

— [Name], founder
```

30–50% reply to this when it's genuinely one question. "What made you decide" gets the trigger moment; "why did you cancel" gets a polite lie.

### 4. Ship the three standard fixes

Match the fix to the cliff — in leverage order:
1. **Never activated** → cut onboarding to one step that reaches the core action in < 3 minutes (see `onboarding-activation`); send a founder email on day 1 offering to set them up personally
2. **Used once** → build the return trigger: a weekly email/notification tied to *their* data ("your launch video got 400 views"), not a generic digest
3. **Invoice churn** → move the plan boundary so the invoice lands *after* a value moment, add pause-instead-of-cancel, and show usage on the billing page ("you made 12 videos this month")

Re-measure 30 days after each fix. One fix at a time — three at once tells you nothing about what worked.

## Output

1. **Churn snapshot** — the two metrics computed from this product's actual data (or the SQL/queries to get them)
2. **Cliff diagnosis** — last 10 churned users tagged, with the dominant cliff named
3. **Exit-interview email** — personalized, ready to send on the next cancellation (+ automation note for Stripe webhook → email)
4. **Fix plan** — the one fix matched to the dominant cliff, specced concretely for this product, with the 30-day re-measure date
5. **Retention dashboard note** — where these two numbers live from now on (KPI script, PostHog insight, or a pinned SQL query)

---

> **Retention starts before signup — the right users churn less.** [SoloMax](https://solomax.app?ref=shipping-skills) launch videos show your product doing the real thing, so the users who arrive are the ones the product is actually for.
