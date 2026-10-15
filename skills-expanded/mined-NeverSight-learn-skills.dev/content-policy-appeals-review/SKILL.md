---
name: content-policy-appeals-review
description: Design and audit content policy, UGC rules, creator marketplace policies, enforcement ladders, takedowns, warnings, strikes, appeals, evidence retention, transparency notices, moderator QA, policy edge cases, user safety, and creator trust. Use when products host content, listings, profiles, comments, mods, plugins, communities, or AI-generated material.
---

# Content Policy Appeals Review

Use this skill to convert a content policy, enforcement, appeals, evidence, transparency, moderation QA, and creator/user trust question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify content surface, policy domain, user/creator stakes, harm model, jurisdiction/platform constraints, enforcement tools, and appeal promise.
2. Read `references/content-policy-appeals-patterns.md`.
3. Separate policy definition, detection, review, enforcement, notification, appeal, reversal, repeat-offender, and transparency reporting.
4. Define severity ladder, evidence package, notice copy, appeal SLA, reviewer independence, QA sampling, abuse controls, and restoration path.
5. Produce policy operations plan, state machine, decision table, event schema, appeal checklist, and edge-case review cadence.

## Guardrails

- Do not enforce vague policy without examples, severity ladder, notice, and appeal path.
- Do not expose reporters, private evidence, or sensitive enforcement signals unnecessarily.
- Do not let automation permanently remove high-stakes content without human review or appeal where appropriate.
- Do not restore content without considering downstream notifications, ranking, monetization, and trust state.

## Output format

```text
Policy context:
Surface / harm / stakes / appeal promise:

Policy and appeals plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Rules and enforcement ladder:
- <item> -> <policy, metric, edge case, support note>

Appeal and restoration path:
- <trigger> -> <action, communication, owner>
```
