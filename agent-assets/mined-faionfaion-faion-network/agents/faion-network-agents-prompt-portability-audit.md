# Prompt Portability Audit

## Summary

**One-sentence:** Audit report identifying provider-specific lock-in in the current prompt suite — XML tags, role placement, refusal styles — before any cross-vendor migration.

**One-paragraph:** Prompts often encode model-specific assumptions: Claude's XML wrappers, OpenAI's developer/user roles, Gemini's safety markers. Migrating without auditing burns a quarter of engineering time discovering these the hard way. This methodology produces a `portability-audit-report.json` flagging every provider-specific construct, severity, owner, deadline, and remediation pointer to `[[prompt-portability-across-providers]]`. Output is a versioned audit report consumed by the migration spec.

**Ефективно для:**

- Pre-migration audit перед provider swap або model-generation upgrade.
- Кількісна оцінка lock-in: severity + count + owners.
- Audit trail для legal / security review.
- Generator для downstream prompt-portability-across-providers spec.
- Quarterly portability health check.

## Applies If (ALL must hold)

- Planning migration LLM provider or model generation.
- Existing prompt suite committed to repo.
- Named accountable auditor.
- Auditing repository hosts the report.

## Skip If (ANY kills it)

- No migration planned in next 2 quarters.
- Prompt suite already migrated and audit-clean.
- Fewer than 3 instances per year.
- No named owner.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current prompt suite | Markdown / YAML | git |
| Provider catalog (current + planned) | YAML | platform |
| Severity policy (low/medium/high criteria) | Markdown | audit policy |
| Named accountable auditor | string | ownership log |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[prompt-portability-across-providers]]` | Downstream spec consuming this audit. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for audit report + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns | ~900 |
| `content/04-procedure.xml` | essential | 5-step: scope → scan → severity → assign → commit | ~700 |
| `content/05-examples.xml` | essential | Worked example: 23-prompt support-bot audit | ~700 |
| `content/06-decision-tree.xml` | essential | Routes audit-find severity to remediation pointer | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scope-prompt-suite` | haiku | Enumerate files. |
| `scan-and-tag` | sonnet | Per-prompt judgment. |
| `severity-synthesis` | opus | Cross-prompt synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/portability-audit-report.md.j2` | Narrative review draft. |
| `templates/portability-audit-report.md` | Narrative review draft. Generated from `templates/portability-audit-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-portability-audit.py` | Validate audit report | Pre-commit + before migration spec |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[prompt-portability-across-providers]]
- [[prompt-pr-review-checklist]]
- [[provider-deprecation-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree decides whether each finding requires a portability-spec rewrite, a refusal-policy update, or no action. Walk it before assigning remediation owners.
