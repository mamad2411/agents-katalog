---
name: marketing-adaptability-score
description: Measure a marketing team's adaptability, not just its performance, with the five-stage Marketing Adaptability Score - Signal (how quickly we detect meaningful market change), Decision (how quickly we decide what it means for us), Experiment (how quickly we test a response), Adoption (how quickly the organisation changes how it works), Learning (does what we learn change the next decision). Converts each stage into a measurable latency or rate, scores it 1–5, and names the bottleneck stage. Use when a marketing team hits its performance KPIs but keeps being surprised by market shifts, when designing a marketing scorecard for leadership, or when asked "how adaptable is our marketing". Complements `kpi-dashboard-framework` and `saas-growth-efficiency-metrics`, which measure performance.
---

# Marketing Adaptability Score

Source: uploaded infographic "Most marketing teams measure performance. Very
few measure adaptability." (© Andrea Rubik). **[Certain]** the five stages and
their questions are from the image. **[Guessing]** the metrics, thresholds and
scoring below are added here so the idea can actually be measured; the
source gives questions, not measures. Calibrate the thresholds to your own
sales cycle before using them for decisions.

## Performance vs adaptability

| Performance metrics (traditional focus) | Adaptability score (broader focus) |
|---|---|
| Tells you how marketing is working **today** | Tells you whether marketing can **keep working tomorrow** |
| Leads generated · Conversion rate · Market share · Traffic & engagement · Pipeline revenue | Signal · Decision · Experiment · Adoption · Learning |

## The five stages, made measurable

| # | Stage | Source question | Metric | 5 (best) | 3 | 1 |
|---|---|---|---|---|---|---|
| 01 | Signal | How quickly do we detect meaningful market change? | Days from a market event (competitor launch, price change, regulation, demand shift) to it being logged internally | ≤ 7 | 8–30 | > 90 |
| 02 | Decision | How quickly can we decide what it means for us? | Days from logged signal to a written decision (act / watch / ignore) with an owner | ≤ 7 | 8–21 | > 45 |
| 03 | Experiment | How quickly can we test a response? | Days from decision to first live test with a success metric | ≤ 14 | 15–45 | > 90 |
| 04 | Adoption | How quickly can the organisation change how it works? | Days from a winning test to the change being standard practice (SOP, template, budget line updated) | ≤ 30 | 31–90 | > 180 |
| 05 | Learning | Does what we learn change the next decision? | % of last quarter's decisions that explicitly cite a previous test or learning | ≥ 60 % | 30–59 % | < 10 % |

Scores 2 and 4 sit between the bands. **Adaptability Score = average of the
five (1–5).** The lowest stage is the bottleneck. Improving any other stage
first does not raise real adaptability; it only moves the queue.

## How to run it
1. Collect the last 3–5 market signals from the past two quarters (competitor moves, regulatory changes, demand shifts). For each, reconstruct the dates for event → logged → decided → tested → adopted. Use emails, meeting notes, tickets and launch dates, not memory.
2. Compute median days per stage; compute the Learning % from last quarter's decision log.
3. Score, find the bottleneck, and propose one mechanism for it:
   - Signal → a weekly signal log with a named owner (see `trend-analysis`, `competitor-research-web`).
   - Decision → a fixed 30-minute weekly decision slot; every signal leaves it as act/watch/ignore.
   - Experiment → a pre-approved test budget and a one-page test template.
   - Adoption → a winning test is not "done" until the SOP or template is updated (`operational-excellence-layers` ring 1).
   - Learning → decision template has a mandatory "which past test informs this?" field.
4. Re-score each quarter. Report it next to the performance metrics, not instead of them.

## Output format
```
Period: [quarter]   Signals reviewed: [n]
Signal x | Decision x | Experiment x | Adoption x | Learning x  → Adaptability Score x.x / 5
Bottleneck: [stage] — median [n] days vs target [n]
Mechanism: [one change] — owner — start date
Evidence table: signal | event date | logged | decided | tested | adopted
```

Run with `/adaptability-score`.
