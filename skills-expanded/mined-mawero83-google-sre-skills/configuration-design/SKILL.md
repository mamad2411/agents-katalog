---
name: configuration-design
description: >-
  Design safe configuration systems: validation, separation of config/code risks, rollout of config, and avoiding dangerous defaults — from the SRE Workbook. Use for config platform design and config-caused outages.
---

# Configuration Design

**Domain:** `delivery`  
**Sources:** Workbook Ch14–15

## When to use

- Config-triggered outage
- Designing feature flags / config service
- Reviewing dangerous global config

## Principles

- Config changes are production changes — canary and review them.
- Validate early; fail closed on invalid critical config when safe.
- Limit blast radius of global knobs.
- Make intent clear; avoid cryptic magical flags.

## Workflow

1. Inventory high-risk config (routing, auth, quotas, parsers).
2. Add schema validation + dry-run.
3. Require progressive rollout for global config.
4. Add audit log + ownership.
5. Create break-glass with expiry.

## Decision guide

- If one bad flag can brick all regions → split by failure domain.

## Output template

```markdown
# Config safety review
- High-risk knobs:
- Validation:
- Rollout controls:
- Blast radius limits:
- Actions:
```

## Anti-patterns

- Push-all-globally config.
- Undocumented kill switches.

## Related skills

`canarying-releases`, `simplicity`, `incident-management`

## Canonical references

- [Configuration Design](https://sre.google/workbook/configuration-design/)
- [Configuration Specifics](https://sre.google/workbook/configuration-specifics/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
