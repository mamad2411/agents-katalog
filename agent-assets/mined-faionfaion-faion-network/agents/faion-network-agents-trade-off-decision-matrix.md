# Weighted Decision Matrix

## Summary

**One-sentence:** Builds a stakeholder-weighted decision matrix: criteria + weights (sum = 100%), evidence-backed scores per option, conflict identification, and computed weighted totals.

**One-paragraph:** Builds a stakeholder-weighted decision matrix: criteria + weights (sum = 100%), evidence-backed scores per option, conflict identification, and computed weighted totals. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Multi-option architecture decision needing quantified, defensible scoring.
- Cross-stakeholder decision where weighting must be explicit (PM + SRE + sec).
- Audit / compliance context demanding a documented scoring trail.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Multi-option architecture decision needing quantified, defensible scoring.
- Cross-stakeholder decision where weighting must be explicit (PM + SRE + sec).
- Audit / compliance context demanding a documented scoring trail.

## Skip If (ANY kills it)

- Single-option decision — there is nothing to weigh.
- Decision dominated by a hard constraint (compliance, contract) — matrix theatre wastes time.
- Trivial reversible choice — a one-line PR comment suffices.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Option shortlist (2-5) | list | team |
| Stakeholder roster with roles | table | PM |
| Evidence base (benchmarks, case studies, POC data) | links | team |
| Decision question | single sentence | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[decision-tree-process]] | Matrix is the Phase-3 instrument. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `set-weights` | sonnet | Facilitate stakeholder weighting; ensure sum = 100%. |
| `score-options` | sonnet | Bounded scoring with cited evidence. |
| `compute-totals` | haiku | Mechanical weighted sum + conflict detection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-matrix.md.j2` | Matrix skeleton with criteria × options + weighted totals. |
| `templates/decision-matrix.md` | Matrix skeleton with criteria × options + weighted totals. Generated from `templates/decision-matrix.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/matrix.json` | Matrix data payload for scripted computation. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trade-off-decision-matrix.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[decision-tree-process]]
- [[trade-off-decision-methods]]
- [[trade-off-quality-attributes]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (shortlist, stakeholders, evidence, question)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
