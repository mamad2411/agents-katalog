---
name: privacy-and-data-retention-review
description: Review privacy, data retention, deletion, export, consent, telemetry, analytics, backups, account closure, children/minors, store disclosures, and data lifecycle for SaaS, apps, games, desktop utilities, developer tools, marketplaces, and support systems. Use when product decisions touch user data, tracking, storage, privacy claims, compliance risk, or trust.
---

# Privacy And Data Retention Review

Use this skill to make data behavior intentional, explainable, and supportable.

## Workflow

1. Identify data categories, users, jurisdictions/channels, processing purposes, and storage systems.
2. Read `references/privacy-data-retention-patterns.md`.
3. Map collection, use, sharing, retention, deletion, export, backup, telemetry, and support access.
4. Compare product behavior with user-facing privacy/store disclosures.
5. Produce risks, retention schedule, and product changes.

## Guardrails

- This is product/privacy design support, not legal advice.
- Do not invent compliance claims.
- Minimize data by purpose; do not collect because it might be useful someday.

## Output format

```text
Data surface:
Data categories:

Lifecycle map:
- Collect:
- Use:
- Store:
- Share:
- Retain:
- Delete/export:

Risks and fixes:
- <rule id> <risk> -> <fix>
```
