---
name: csm-health-score
version: 1.0.0
description: Define and compute an account health score with weighted risk signals and a clear action threshold.
author: matrixx0070
tags: [customer-success, health-score, risk, retention, analytics]
capabilities: []
---

## When to use

Use this when you need a repeatable, defensible number that tells you which accounts are healthy and which need intervention. Reach for it when building a portfolio-wide health model, or scoring a single account before a QBR, renewal, or escalation.

**Not for:** measuring a single support interaction's CSAT (that is customer-support); forecasting deal probability for new logos (that is sales); one-off gut-feel escalations where no scoring is needed.

## Method

1. Choose 4-6 signal categories across three dimensions: **usage** (adoption breadth, frequency, key-feature use), **relationship** (sponsor engagement, exec access, NPS), and **commercial/support** (open escalations, invoice health, seat utilization).
2. For each signal, define an objective measurement and a 0-100 sub-score with explicit bands. Decision point: if a signal cannot be measured objectively, drop it or convert it to a manual red/yellow/green flag.
3. Assign weights summing to 100%. Weight leading indicators (usage trend, sponsor engagement) higher than lagging ones (NPS). Decision point: if you lack usage data, weight relationship signals higher and mark the score as low-confidence.
4. Compute the weighted score. Apply **override rules**: any critical red signal (e.g., sponsor left, contract dispute) caps the total at "at-risk" regardless of math.
5. Map the score to a tier: Healthy (≥75), Watch (50-74), At-risk (<50).
6. Attach the top 1-2 dragging signals and a recommended play to every non-healthy account.
7. Recompute on a fixed cadence and track the trend — direction matters more than the absolute number.

## Example

Account scores: usage-breadth 40/100 (weight 25%), usage-trend 30 (25%), sponsor-engagement 80 (20%), NPS 70 (10%), open-escalations 60 (10%), seat-utilization 50 (10%). Weighted = 10+7.5+16+7+6+5 = 51.5 → Watch. Trend is down two quarters and the sponsor just changed → override to At-risk. Top drags: usage-trend, seat-utilization. Recommended play: re-onboard new sponsor, run adoption push on unused seats.

## Pitfalls

- **All lagging indicators.** A score built only on NPS and renewals tells you about churn after it is unavoidable.
- **No override for critical events.** A green score with a departed champion is a false negative that costs the renewal.
- **Vanity precision.** Reporting 73.4 implies accuracy you do not have; use tiers and trend.
- **Score with no assigned play.** A number nobody acts on is a dashboard, not a health system.

## Output format

```
HEALTH SCORE — <account> | <date>
Overall: <n>/100 → <Healthy|Watch|At-risk> (trend: ↑/↓/→ vs last period) | confidence: <high|low>
Signals (score × weight):
- usage-breadth: <n> × <w>%
- usage-trend: <n> × <w>%
- sponsor-engagement: <n> × <w>%
- <signal>: <n> × <w>%
Override applied: <none | reason → capped tier>
Top drags: <signal 1>, <signal 2>
Recommended play: <play + owner>
```
