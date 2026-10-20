# CR Impact Memo Template

## Summary

**One-sentence:** A standardised CR impact memo with scope / cost / schedule / risk deltas and a recommendation, produced by BA and signed by the approver from change-request-impact-rubric.

**One-paragraph:** CRs without an impact memo land in the steering committee as raw debate. Memos surface scope / cost / schedule / risk deltas with evidence per delta, plus a recommendation. Output: a structured Markdown memo attached to the CR record. Reads in <5 minutes; reviewed by the approver chosen by `change-request-impact-rubric`.

**Ефективно для:**

- Engagements with formal change-control gates.
- Regulated programs where memo trail is audit evidence.
- Steering-committee submissions needing concise framing.
- Recurrent-CR programs where memo template reduces drafting time.

## Applies If (ALL must hold)

- a CR record exists with the affected IDs
- impact rubric has bin and approver assigned
- named author accepts memo ownership
- approver named

## Skip If (ANY kills it)

- no CR record — fix that first
- impact rubric not run — run it first
- CR is trivial (bin S) and can be approved inline

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CR record | ticket | submitter |
| CR impact rubric output | JSON | change-request-impact-rubric |
| traceability graph | JSON | traceability-auto-maintenance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[change-request-impact-rubric]] | Source of bin + approver decision. |
| [[cr-options-matrix-template]] | Sibling artefact for option comparison. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: bound scope, typed input, named owner, versioned record, detector-first | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for CR impact memo: deltas[], recommendation, approver, owner, version | 700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: deltas without evidence, anonymous owner, post-hoc rationale, version frozen, scope creep | 900 |
| `content/04-procedure.xml` | essential | 4-step procedure: pull rubric → quantify deltas → recommend → review with approver | 600 |
| `content/05-examples.xml` | essential | Worked example: medium CR impact memo (scope + 3 stories, schedule +1 sprint) | 500 |
| `content/06-decision-tree.xml` | essential | Tree on rubric bin + traceability freshness + approver availability | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-delta quantification. |
| `review_for_compliance` | opus | High-stakes regulated CRs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cr-impact-memo-template.json` | JSON skeleton for the memo. |
| `templates/cr-impact-memo-template.md.j2` | Markdown skeleton with required fields. |
| `templates/cr-impact-memo-template.md` | Markdown skeleton with required fields. Generated from `templates/cr-impact-memo-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable memo. |
| `templates/_smoke-test.md` | Minimum viable memo. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cr-impact-memo-template.py` | Validates the CR impact memo against the JSON Schema. | Before approver review; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[change-request-impact-rubric]]
- [[cr-options-matrix-template]]
- [[decision-options-memo-template]]
- [[decision-rationale-capture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
