---
name: game-soft-launch-review
description: Plan and audit mobile or PC game soft launches, test markets, cohort gates, economy balance, IAP, ads, retention, FTUE, live events, store listing tests, crash/performance health, community feedback, and scale/kill decisions. Use when preparing a game before global launch or evaluating whether to expand, iterate, or stop.
---

# Game Soft Launch Review

Use this skill to convert a high-stakes product decision into a concrete, measurable, reviewable operating artifact.

## Workflow

1. Identify game genre, target market, test region, acquisition source, monetization model, core loop, and launch decision horizon.
2. Read `references/game-soft-launch-patterns.md`.
3. Define cohort gates across retention, session quality, economy, IAP, ads, crashes, store conversion, support, and community sentiment.
4. Separate product learning, monetization tuning, technical readiness, acquisition quality, and creative/listing tests.
5. Produce soft-launch plan, gate matrix, live-ops calendar, instrumentation, and scale/iterate/kill decision record.

## Guardrails

- Do not scale paid acquisition from blended metrics that hide low-quality cohorts.
- Do not over-monetize early cohorts in ways that invalidate retention learning.
- Do not treat one test market as global proof without market-fit caveats.
- Protect player trust around economy resets, purchases, ads, and support during test periods.

## Output format

```text
Soft-launch context:
Game / market / cohort / monetization:

Gate matrix:
| Gate | Metric | Segment | Pass | Watch | Stop | Action |
| --- | --- | --- | --- | --- | --- | --- |

Live-ops and economy review:
- <event/economy/ad/IAP/support item>

Decision record:
- <scale / iterate / hold / kill with evidence>
```
