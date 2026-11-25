---
name: eight-ps-of-sales
description: Audits a sales process against the 8 Ps of Sales (Prospecting, Preparation, Presentation, Pricing, Persuasion, Persistence, Performance, Post-Sale) — scores each P from evidence, names the weakest link, and gives three next actions. Use when a pipeline leaks, win rate is flat, or someone asks "where is my sales process broken?". Run via /8ps-audit.
---

# The 8 Ps of the Sales Process

Source: SalesDaily.co infographic (quote by Brian Tracy: "Approach each customer with the idea of helping him or her solve a problem or achieve a goal, not of selling a product or service."). The infographic is a checklist, not a benchmark study — treat the scoring below as a diagnostic aid, not as validated research.

## The eight Ps (in cycle order)

| # | P | What it covers | Evidence to ask for |
|---|---|---|---|
| 1 | Prospecting | Identifying and qualifying potential customers via research, referrals, lead generation | ICP document, qualified-lead count per week, source mix |
| 2 | Preparation | Researching prospects, customizing the pitch, understanding pain points and business needs | Pre-call research template, % of calls with a written pain hypothesis |
| 3 | Presentation | Compelling demos and proposals that show value and ROI | Demo script, proposal template, ROI calculator |
| 4 | Pricing | Negotiating terms, discounts, payment options, creating urgency to close | Discount policy, approval matrix, average discount given |
| 5 | Persuasion | Handling objections, building trust, influencing decision-makers | Objection library, reference customers, mutual action plans |
| 6 | Persistence | Consistent follow-up, staying top-of-mind, nurturing long cycles | Follow-up cadence, % of deals with next step booked, nurture sequence |
| 7 | Performance | Tracking metrics, win/loss ratios, optimising sales activity | Dashboard, win/loss reviews, stage conversion rates |
| 8 | Post-Sale | Smooth onboarding, upsell, referrals from satisfied customers | Onboarding checklist, expansion rate, referral count |

The Ps form a loop: Post-Sale feeds Prospecting (referrals) and Performance feeds every P.

## How to run the audit

1. Ask for one sales motion only (e.g. "outbound to hospital procurement"), never "all sales".
2. Ask for evidence for all 8 Ps in ONE table (document, tool, dashboard, or "none").
3. Score each P 0–3: 0 = nothing, 1 = ad hoc/"we sort of do it", 2 = documented but inconsistently used, 3 = documented, used, measured.
4. Name the weakest P. If two tie, pick the earlier one in the cycle — upstream weakness starves everything downstream.
5. Give exactly three actions for that P: owner, date, evidence of done.
6. List every other P that scored ≤1 as "parked" with the condition that unparks it.

## Output format

```
Motion audited: <name>
| P | Score 0–3 | Evidence | Gap |
Weakest P: <P> — <one-sentence why it caps the funnel>
30-day actions: 1) … 2) … 3) …
Parked: <P — unpark when …>
Cross-links: <which existing skill helps: prospecting / sales-enablement / pricing / revops / churn-prevention>
```

## Rules

- Never invent conversion numbers; if evidence is absent the score is 0 or 1, and say "unverified".
- Do not recommend tooling before a process exists on paper.
- Pair with: `sales-enablement` (Presentation/Persuasion), `pricing` (Pricing), `prospecting` (Prospecting), `revops` (Performance), `churn-prevention` (Post-Sale), `sales-workflow-catalog` (automation of any P).
