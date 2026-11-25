---
name: store-review-policy-risk
description: Audit store review and platform policy risk across App Store, Google Play, Microsoft Store, Steam, web/direct download, mobile apps, games, SaaS companions, utilities, subscriptions, IAP, ads, UGC, privacy, permissions, health, finance, children, AI features, notifications, dark patterns, refunds, and review notes. Use when preparing submission, launch, major monetization changes, or auditing any product that may be rejected, delisted, or delayed by channel policy.
---

# Store Review Policy Risk

Use this skill to find review blockers before a store reviewer, player, or user does.

## Workflow

1. Identify distribution channels, product type, audience, monetization, data collection, permissions, UGC, ads, and regulated claims.
2. Read `references/store-review-policy-risk-systems.md`.
3. Map every risky feature to policy area, user-facing disclosure, reviewer evidence, fallback, and support path.
4. Separate hard blockers, clarification needs, reviewer-note improvements, and post-approval monitoring.
5. Produce a risk register and submission readiness checklist.

## Guardrails

- Verify current platform policy before submission; this skill is a risk-audit framework, not legal advice.
- Do not recommend hiding behavior from review or users.
- Treat privacy, payments, children, health/finance, UGC/moderation, and external purchases as high-risk until proven otherwise.

## Output format

```text
Channels:
Product risk profile:

Risk register:
- <risk> -> channel, policy area, blocker level, evidence, mitigation

Reviewer notes:
- <channel> -> note, demo account, test path, disclosure

Submission gate:
- go / conditional / no-go with reasons
```
