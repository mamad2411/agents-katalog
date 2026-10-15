---
name: mobile-first-ui-review
description: Review and improve mobile-first UI for apps, web products, SaaS, utilities, and games across touch ergonomics, safe areas, navigation, forms, permissions, loading, offline states, and perceived speed. Use when designing or auditing mobile interfaces, responsive mobile views, onboarding screens, purchase flows, settings, or any UI that must feel fast and modern on phones.
---

# Mobile First UI Review

Use this skill to make mobile experiences feel native, fast, and easy to operate with one hand.

## Workflow

1. Identify the primary mobile job, screen type, and device constraints.
2. Read `references/mobile-ui-rules.md`.
3. Review the UI through hierarchy, reachability, input, feedback, platform chrome, and failure states.
4. Separate critical blockers from polish opportunities.
5. Produce a concrete patch plan or review findings with rule IDs.

## Guardrails

- Do not optimize only for screenshots; optimize the lived touch flow.
- Preserve accessibility, reduced motion, dynamic type, safe areas, and keyboard behavior.
- Prefer removing friction before adding decoration.

## Output format

```text
Surface:
Primary mobile job:

Critical issues:
- <rule id> <issue> -> <fix>

Polish opportunities:
- <rule id> <detail> -> <fix>

Mobile acceptance checks:
- <check>
```
