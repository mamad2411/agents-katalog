# Client Control ID Mapping

## Summary

**One-sentence:** A bi-directional map between client-supplied compliance control IDs and internal requirements + tests, queryable by auditor in < 5 minutes.

**One-paragraph:** Auditors arrive with a control list and demand 'show me evidence for control X-12'. Hand-maintained spreadsheets rot; engineers refactor tests and break the link silently. This methodology installs a versioned mapping with: (a) source-of-truth client control list, (b) internal requirement / test IDs per control, (c) evidence URL per pairing, (d) named owner per control, (e) broken-link detector. Output: a YAML/JSON mapping + auditor query CLI.

**Ефективно для:**

- Regulated builds (HIPAA, PCI, SOX, ISO 27001, SOC 2).
- Pre-audit hardening (4–8 weeks before audit).
- Vendor onboarding where the buyer dictates control IDs.
- Multi-tenant SaaS with per-tenant compliance overlay.

## Applies If (ALL must hold)

- client provides a discrete control list (IDs not free-form text)
- internal requirements + tests are ID-addressable
- named owner accepts maintenance of the mapping
- evidence is queryable (logs / CI / dashboards)

## Skip If (ANY kills it)

- no client control list — request one first
- internal IDs are not stable across releases — fix the ID system first
- no auditor will ever query this — premature compliance

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| client control list | CSV / PDF | client / regulator |
| internal requirement IDs | ALM export | BA |
| test ID list with evidence URLs | CI artefact | QA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[traceability-auto-maintenance]] | Provides the daily job rebuilding the mapping. |
| [[compliance-checklist-by-domain]] | Source of compliance-domain context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: bound scope, typed input, named owner, versioned record, detector-first | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for control-mapping record: control_id, internal_ids, evidence_urls, owner, last_reviewed | 700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: inputs invented, owner collapsed to team, post-hoc rationale, version frozen, scope creep | 900 |
| `content/04-procedure.xml` | essential | 4-step procedure: import client list → match internal IDs → attach evidence → assign owner | 600 |
| `content/06-decision-tree.xml` | essential | Tree on client list discreteness + internal ID stability + audit horizon | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation. |
| `synthesize_decision` | sonnet | Per-control mapping judgment. |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/client-control-id-mapping.json` | JSON skeleton for the control-mapping record. |
| `templates/client-control-id-mapping.md.j2` | Markdown skeleton with required fields. |
| `templates/client-control-id-mapping.md` | Markdown skeleton with required fields. Generated from `templates/client-control-id-mapping.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable control mapping. |
| `templates/_smoke-test.md` | Minimum viable control mapping. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-control-id-mapping.py` | Validates the control-mapping record against the JSON Schema. | After mapping update; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[compliance-checklist-by-domain]]
- [[traceability-auto-maintenance]]
- [[definition-of-done-library]]
- [[cr-impact-memo-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
