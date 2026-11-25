---
name: moderation-trust-review
description: Design and audit moderation, trust, safety, policy, review queues, creator or user submissions, appeals, enforcement ladders, transparency, and marketplace/community integrity flows. Use when products include UGC, reviews, comments, listings, plugins, skills, marketplaces, communities, or creator submissions that need safe publishing and fair enforcement.
---

# Moderation Trust Review

Use this skill to turn a recurring product-operations problem into a concrete, reviewable artifact instead of generic advice.

## Workflow

1. Identify content types, actors, harm classes, visibility states, enforcement authority, and appeal ownership.
2. Read `references/moderation-trust-patterns.md`.
3. Map submission, automated checks, queue triage, human review, enforcement, notification, appeal, and audit logging.
4. Separate policy uncertainty, low-risk quality issues, abuse/fraud, illegal content, safety emergencies, and repeat offenders.
5. Produce a moderation workflow, queue policy, enforcement ladder, transparency copy, and event schema.

## Guardrails

- Do not make irreversible account or creator decisions from low-confidence automation alone.
- Do not hide enforcement reasons when a safe, specific explanation is possible.
- Keep moderator tooling, user-facing policy, and product ranking logic separate.
- Escalate legal, child safety, self-harm, or jurisdiction-specific obligations to qualified review.

## Output format

```text
Moderation context:
Content / actor / surface:

State flow:
- <state> -> <action / reviewer / user-visible effect>

Decision table:
| Scenario | Visibility | Enforcement | Appeal | Evidence |
| --- | --- | --- | --- | --- |

Queue policy and events:
- <queue/SLA/event>
```
