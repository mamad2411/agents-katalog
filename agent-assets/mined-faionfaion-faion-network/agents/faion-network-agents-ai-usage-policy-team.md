# Team AI Usage Policy

## Summary

**One-sentence:** 1-page team-facing policy spec: always-OK list, never-OK list, ask-first list, incident-response path. Owner + quarterly review locked in.

**One-paragraph:** Every product team needs a team-facing AI usage policy; 99% don't have one. Existing AI-governance work targets ML-engineers (wrong audience). This methodology produces a 1-page policy artefact with three explicit lists (always-OK, never-OK, ask-first) + a 4-step incident-response runbook + a named owner + quarterly review cadence. Output is a versioned Markdown spec validated by CI on every team change.

**Ефективно для:**

- Команди 3-50 розробників, які копіпастять у Cursor/Copilot/Claude без правил.
- Компанії, що handlуть customer data, source code, sales/legal docs, PII — швидкий policy за день.
- Post-incident: hot-fix policy перед audit, з incident-response runbook'ом.
- Quarterly AI-governance review: версіонована policy = audit trail.

## Applies If (ALL must hold)

- Team has 3-50 developers using AI tools (Cursor / Copilot / Claude / ChatGPT / CLI agents).
- Company handles ANY of: customer data, source code, sales/legal docs, PII, regulated data.
- No existing AI usage policy OR existing policy is &gt; 6 months old.

## Skip If (ANY kills it)

- Team uses zero AI tooling.
- Company-wide AI policy already exists and is &lt; 6 months old; refresh that document instead.
- Solo founder with no team yet.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tool inventory | list of AI tools team uses | team survey |
| Data inventory | categories of sensitive data team touches | security / data-protection officer |
| Incident report channel | Slack / form / email | existing IR plan |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: three-lists-required, named-owner-and-cadence, incident-response-runbook, gray-zone-resolution, policy-is-one-page | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory-tools-and-data` | haiku | Mechanical cataloguing. |
| `draft-three-lists` | sonnet | Light judgment on categorization. |
| `write-ir-runbook` | sonnet | Maps roles to time SLAs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-policy.md.j2` | 1-page policy Markdown template (owner, review, three lists, IR runbook) |
| `templates/ai-policy.md` | 1-page policy Markdown template (owner, review, three lists, IR runbook) Generated from `templates/ai-policy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ir-runbook.md.j2` | 4-step incident-response runbook template |
| `templates/ir-runbook.md` | 4-step incident-response runbook template Generated from `templates/ir-runbook.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-usage-policy-team.py` | Validate the spec artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-trust-disclosure-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
