---
name: user-preferences-settings-review
description: Design and audit user preferences, personalization controls, notification settings, privacy toggles, accessibility options, language/region settings, theme, default behavior, reset/export behavior, cross-device sync, and settings discoverability. Use when users need durable control over product behavior without confusing admin policy, billing, or security settings.
---

# User Preferences Settings Review

Use this skill to convert a risky product, operations, trust, or marketplace question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Inventory preference types, scope, default, persistence, sync behavior, privacy impact, and reset/recovery need.
2. Read `references/user-preferences-patterns.md`.
3. Separate personal preference, account setting, workspace policy, device setting, privacy consent, and entitlement-controlled option.
4. Design settings IA, default behavior, disabled states, migration, export/delete behavior, and instrumentation.
5. Produce preference matrix, state flow, UX copy, edge cases, and event schema.

## Guardrails

- Do not hide privacy consent or legal choices inside cosmetic preferences.
- Do not override user preference with growth experiments without explicit policy.
- Do not make destructive or high-impact settings too easy to change accidentally.
- Respect accessibility, localization, and cross-device consistency.

## Output format

```text
Preferences context:
User scope / device / account / workspace:

Preference matrix:
| Preference | Scope | Default | Persistence | Disabled state | Reset/export |
| --- | --- | --- | --- | --- | --- |

State flow:
- <view/change/sync/reset/migrate>

Events and copy:
- <event or user-facing explanation>
```
