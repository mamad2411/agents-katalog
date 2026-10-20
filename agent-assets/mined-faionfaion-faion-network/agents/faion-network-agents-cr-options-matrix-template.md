# CR Options Matrix Template

## Summary

**One-sentence:** An options matrix for major Change Requests scoring ≥2 viable responses on cost / value / risk and routing the recommended option to the named approver.

**One-paragraph:** Major CRs need option comparison, not just an impact memo. This template forces ≥2 viable response options (accept-as-is / reduce-scope / defer / re-baseline), scores each on cost / value / risk, names the recommendation, and routes it via `change-request-impact-rubric`. Output: a Markdown options matrix attached to the CR record.

**Ефективно для:**

- Major CRs (bin L per change-request-impact-rubric).
- Re-baselining decisions on multi-quarter programs.
- Steering-committee submissions where option theatre is forbidden.
- Programs with a track record of single-option recommendations failing.

## Applies If (ALL must hold)

- the CR is bin L (major) per change-request-impact-rubric
- the program has capacity to enumerate ≥2 viable options
- named approver exists
- scoring rubric for cost / value / risk is agreed

## Skip If (ANY kills it)

- CR is bin S or M — use cr-impact-memo-template instead
- single-option forced (regulatory mandate) — escalate as no-option memo
- no scoring rubric — agree one first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CR record + impact rubric bin | JSON | change-request-impact-rubric |
| scoring rubric (cost/value/risk) | MD | PM / BA |
| named approver | org chart | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[change-request-impact-rubric]] | Source of bin classification. |
| [[cr-impact-memo-template]] | Companion artefact for impact framing. |
| [[decision-options-memo-template]] | Generic options-memo pattern this specialises. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: ≥2 viable options, scored on cost/value/risk, named approver, recommendation backed by rationale, no single-option theatre | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for options matrix: options[], scores, recommendation, approver, version | 700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: single-option theatre, anonymous owner, score drift, post-hoc rationale, scope creep | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: enumerate options → score → recommend → review → route to approver | 700 |
| `content/05-examples.xml` | essential | Worked example: major CR with 3 options (accept / reduce / defer) and recommendation | 500 |
| `content/06-decision-tree.xml` | essential | Tree on bin + option count + approver availability | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-option scoring + recommendation. |
| `review_for_compliance` | opus | High-stakes re-baseline decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cr-options-matrix-template.json` | JSON skeleton for the options matrix. |
| `templates/cr-options-matrix-template.md.j2` | Markdown skeleton with required fields. |
| `templates/cr-options-matrix-template.md` | Markdown skeleton with required fields. Generated from `templates/cr-options-matrix-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable options matrix. |
| `templates/_smoke-test.md` | Minimum viable options matrix. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cr-options-matrix-template.py` | Validates the options matrix against the JSON Schema. | Before approver review; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[change-request-impact-rubric]]
- [[cr-impact-memo-template]]
- [[decision-options-memo-template]]
- [[decision-rationale-capture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
