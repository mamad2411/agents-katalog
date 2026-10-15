---
name: launch-readiness-review
description: Review launch readiness for SaaS, mobile apps, games, desktop software, developer tools, marketplaces, and major releases across product quality, pricing, payments, distribution, support, analytics, incident readiness, promotion, legal/trust, rollback, and post-launch learning. Use when preparing public launch, store submission, beta, release, major campaign, or go/no-go review.
---

# Launch Readiness Review

Use this skill to decide whether launch is ready, risky, or blocked.

## Workflow

1. Identify launch type, audience, channels, release owner, and blast radius.
2. Read `references/launch-readiness-patterns.md`.
3. Review product, monetization, distribution, support, analytics, trust, infra, promotion, and rollback.
4. Classify blockers as launch-blocking, launch-risk, or post-launch follow-up.
5. Produce a readiness verdict and launch room checklist.

## Guardrails

- Do not treat marketing readiness as product readiness.
- Do not launch paid or data-risky flows without support and rollback paths.
- Make no-go criteria explicit before launch day.

## Output format

```text
Launch type:
Channels:
Verdict: go / conditional go / no-go

Blockers:
- <blocker> -> <owner/evidence needed>

Launch checklist:
- <check>

Post-launch watch:
- <metric/log/support signal>
```
