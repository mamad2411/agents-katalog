---
name: onboarding-activation-review
description: Review and design onboarding and activation flows for SaaS, mobile apps, games, developer tools, utilities, marketplaces, and web products. Use when improving first-run experience, setup checklists, permission timing, aha moments, trial activation, invite/team setup, empty states, tutorials, or early retention measurement.
---

# Onboarding Activation Review

Use this skill to move users from curiosity to first real value with minimal ceremony.

## Workflow

1. Identify target user, promised outcome, activation event, and required setup.
2. Read `references/onboarding-activation-patterns.md`.
3. Map first session, permission prompts, account setup, tutorial, first value, and return path.
4. Remove non-essential friction before adding guidance.
5. Produce activation flow, instrumentation, and experiment backlog.

## Guardrails

- Do not mistake completed onboarding screens for activated users.
- Do not ask for permissions, imports, invites, or payment before the value rationale is clear.
- Preserve skip/recovery paths where setup can happen later.

## Output format

```text
Target user:
Activation event:

Flow review/spec:
- <rule id> <issue or decision> -> <fix>

Activation metrics:
- <event or metric>

Experiment backlog:
- Hypothesis: <hypothesis>
  Change: <change>
  Measure: <metric>
```
