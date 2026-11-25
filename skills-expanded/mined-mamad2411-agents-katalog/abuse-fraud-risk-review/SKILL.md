---
name: abuse-fraud-risk-review
description: Review abuse, fraud, spam, promotion abuse, payment fraud, refund abuse, account takeover risk, marketplace trust, game economy exploits, referral abuse, automation abuse, and moderation risk for software products. Use when designing controls, risk ladders, rate limits, manual review, user messaging, support escalation, or fraud-safe product systems.
---

# Abuse Fraud Risk Review

Use this skill to protect product integrity without punishing legitimate users unfairly.

## Workflow

1. Identify assets at risk, attacker incentives, abuse surfaces, and legitimate-user harm.
2. Read `references/abuse-fraud-risk-patterns.md`.
3. Map signals, controls, review ladder, support route, and recovery/appeal.
4. Separate prevention, detection, response, and learning.
5. Produce risk matrix and control plan.

## Guardrails

- Do not recommend silent irreversible punishment without evidence and appeal path.
- Do not collect excessive data for vague fraud goals.
- Balance false positives against abuse damage.

## Output format

```text
Abuse surface:
Assets at risk:

Risk matrix:
- <scenario> -> likelihood, impact, controls, review path

Controls:
- Prevent:
- Detect:
- Respond:
- Recover:

Events/signals:
- <signal>
```
