# Compliance Checklist by Domain

## Summary

**One-sentence:** A domain-indexed compliance checklist BAs apply during requirements validation to surface missing non-functional and regulatory items before sign-off.

**One-paragraph:** Requirements sign-off without a compliance checklist routinely misses non-functional items (data residency, retention, audit logging, accessibility). This methodology indexes checklists by compliance domain (GDPR / HIPAA / PSD2 / SOC2 / WCAG) so a BA can pick the relevant domain(s) and walk the checklist. Each item carries: rationale, evidence-required, owner, source-clause. Output: a checked checklist + gap list feeding the requirements backlog.

**Ефективно для:**

- Pre-sign-off requirements validation on regulated builds.
- Domain-onboarding BAs new to GDPR / HIPAA / PSD2.
- Pre-audit gap-finding (4–8 weeks before audit).
- Vendor RFP-response compliance section.

## Applies If (ALL must hold)

- the engagement touches at least one regulatory domain (GDPR / HIPAA / PSD2 / SOC2 / WCAG)
- named owner accepts the checked checklist
- a draft requirements set exists to validate against
- compliance scope is bounded (not 'all of EU')

## Skip If (ANY kills it)

- no regulatory domain applies — skip the checklist entirely
- the engagement is purely internal with no PII / payments
- compliance team owns this artefact already — defer

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| draft requirements set | MD / wiki / ALM | BA |
| regulatory scope statement | MD | compliance / legal |
| named owner | org chart | BA / compliance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[client-control-id-mapping]] | Maps checked items to client controls if a client list exists. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: domain-indexed selection, every item has source clause + evidence required, named owner, no checklist without rationale, ≤ 50 items per domain pass | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for checked checklist: items[], domain, owner, last_reviewed, gap_count | 700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: tick-the-box drift, missing source clause, anonymous owner, scope drift, stale checklist | 900 |
| `content/04-procedure.xml` | essential | 4-step procedure: select domains → walk items → record evidence → emit gap list | 600 |
| `content/06-decision-tree.xml` | essential | Tree on regulatory scope + audit horizon + checklist freshness | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-item evidence-check. |
| `review_for_compliance` | opus | Cross-domain synthesis on high-stakes audits. |

## Templates

| File | Purpose |
|------|---------|
| `templates/compliance-checklist-by-domain.json` | JSON skeleton for the checked checklist. |
| `templates/compliance-checklist-by-domain.md.j2` | Markdown skeleton with required fields. |
| `templates/compliance-checklist-by-domain.md` | Markdown skeleton with required fields. Generated from `templates/compliance-checklist-by-domain.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable checked checklist. |
| `templates/_smoke-test.md` | Minimum viable checked checklist. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-compliance-checklist-by-domain.py` | Validates the checked checklist against the JSON Schema. | Before sign-off; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[client-control-id-mapping]]
- [[definition-of-done-library]]
- [[cr-impact-memo-template]]
- [[scope-drift-early-warning-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
