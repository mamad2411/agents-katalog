# Change Request Impact Rubric

## Summary

**One-sentence:** A scored Change Request impact rubric that bins a CR by blast radius and routes it to BA, PO, or steering-committee approval.

**One-paragraph:** CRs that should be a 10-minute BA decision end up in the steering committee, and CRs that should escalate end up rubber-stamped. This rubric scores a CR on five blast-radius dimensions (requirements touched, AC touched, tests touched, regulatory clauses touched, dependent stories touched) into a S/M/L bin with a deterministic approval route per bin. Output: a CR impact record with score, bin, approver, owner, and rationale.

**Ефективно для:**

- Engagements with formal change-control gates.
- Regulated programs where the approval route matters legally.
- High-volume CR programs needing triage automation.
- Engagements with mixed CR severities and overloaded steering committees.

## Applies If (ALL must hold)

- a change-control process exists (even informal)
- traceability data is current (requirements ↔ AC ↔ tests ↔ stories)
- approval routes (BA / PO / steering) are defined
- named owner accepts the rubric output

## Skip If (ANY kills it)

- no change-control process at all — fix that first
- traceability data missing — rubric inputs are inferred
- single CR per quarter — rubric overhead > value

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| traceability graph | JSON / CSV | traceability-auto-maintenance |
| approval-route policy | MD / wiki | PM |
| CR record (description + affected ids) | ticket | submitter |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[traceability-auto-maintenance]] | Source of dependency data. |
| [[cr-impact-memo-template]] | Downstream artefact this rubric feeds. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: bound scope, typed input, named owner, versioned record, detector-first | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for CR impact record: artefact_id, owner, decision, rationale, inputs_used, version, last_reviewed, bin | 700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: inputs invented, owner collapsed to team, post-hoc rationale, version frozen, scope creep | 900 |
| `content/04-procedure.xml` | essential | 4-step procedure: collect inputs → score dimensions → bin → assign approver | 600 |
| `content/06-decision-tree.xml` | essential | Tree on traceability freshness + bin score + regulatory context | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation. |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs. |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/change-request-impact-rubric.json` | JSON skeleton for the CR impact record. |
| `templates/change-request-impact-rubric.md.j2` | Markdown skeleton with required fields. |
| `templates/change-request-impact-rubric.md` | Markdown skeleton with required fields. Generated from `templates/change-request-impact-rubric.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable rubric record. |
| `templates/_smoke-test.md` | Minimum viable rubric record. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-change-request-impact-rubric.py` | Validates the rubric record against the JSON Schema. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[cr-impact-memo-template]]
- [[cr-options-matrix-template]]
- [[traceability-auto-maintenance]]
- [[decision-rationale-capture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
