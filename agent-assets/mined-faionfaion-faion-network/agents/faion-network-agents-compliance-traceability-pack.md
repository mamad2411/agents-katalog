# Compliance Traceability Pack

## Summary

**One-sentence:** Produces a compliance traceability pack for a regulated BA engagement (KYC / FHIR / GDPR / SOC2): requirement-to-regulation map, evidence inventory, control owner table, audit-ready exports.

**Ефективно для:** BAs on FinTech / HealthTech / GovTech engagements; compliance officers auditing requirements coverage; PMs gating release on regulatory traceability.

**One-paragraph:** This methodology pins the recurring decision around "compliance-traceability-pack" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Engagement touches a named regulation (KYC / FHIR / GDPR / SOC2 / EU AI Act).
- Requirements exist or are being authored.
- Owner exists for the pack.
- Audit deadline exists or is foreseeable.

## Skip If (ANY kills it)

- Engagement is fully unregulated.
- Compliance handled by a separate team with their own artefact (link out).
- Pilot / spike with no production launch.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Requirement register | CSV / Markdown | BA |
| Applicable regulation list + clauses | Markdown | legal |
| Evidence inventory | CSV | QA / compliance |
| Control owner table | CSV | engineering / compliance |
| Audit deadline + scope | spreadsheet | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[ai-transcript-to-traceable-requirement]]` | requirements carry traceability metadata |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_map` | sonnet | Requirement-to-regulation mapping needs judgment. |
| `synthesize_evidence` | sonnet | Per-clause evidence selection. |
| `escalate_gap` | opus | When a clause has no evidence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/compliance-traceability-pack.json` | JSON Schema for the Compliance Traceability Pack output contract |
| `templates/compliance-traceability-pack.md.j2` | Markdown skeleton with the required fields |
| `templates/compliance-traceability-pack.md` | Markdown skeleton with the required fields Generated from `templates/compliance-traceability-pack.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a compliance-traceability-pack record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a compliance-traceability-pack record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-compliance-traceability-pack.py` | Enforce the Compliance Traceability Pack output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[fintech-kyc-ba-pack]] — adjacent KYC-specific pack.
- [[ai-transcript-to-traceable-requirement]] — feeds traced requirements.
- [[ai-enabled-business-analysis]] — parent methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
