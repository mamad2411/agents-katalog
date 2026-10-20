# Trade-off Decision Methods

## Summary

**One-sentence:** Routes the decision to the right method (Weighted Matrix, ATAM, Cost of Delay, Wardley, Real Options) based on number of options, stakeholder breadth, reversibility, and uncertainty.

**One-paragraph:** Routes the decision to the right method (Weighted Matrix, ATAM, Cost of Delay, Wardley, Real Options) based on number of options, stakeholder breadth, reversibility, and uncertainty. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Architecture decision whose default method (weighted matrix) is suspect (cross-attribute conflicts, deep uncertainty, high reversibility cost).
- Multi-quality-attribute trade-off (perf vs cost vs security) needing ATAM-style analysis.
- Strategic decision needing Wardley map or Real Options framing.
- Output produces `decision-record` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Architecture decision whose default method (weighted matrix) is suspect (cross-attribute conflicts, deep uncertainty, high reversibility cost).
- Multi-quality-attribute trade-off (perf vs cost vs security) needing ATAM-style analysis.
- Strategic decision needing Wardley map or Real Options framing.

## Skip If (ANY kills it)

- Single-option / hard-constraint decision — no method needed.
- Routine reversible choice — weighted matrix is enough; no method routing required.
- Decision dominated by a mandate that overrides any method outcome.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision question + context | doc | team |
| Option shortlist (2-5) | list | team |
| Uncertainty level (low / med / high) + reversibility | field | architect |
| Stakeholder breadth (single team / cross-team / cross-org) | field | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[trade-off-decision-matrix]] | Weighted matrix is the default method. |
| [[quality-attributes]] | ATAM consumes the QA scenario set. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-context` | haiku | Lookup uncertainty + reversibility + stakeholder breadth → method bucket. |
| `pick-method` | sonnet | Bounded judgement: matrix vs ATAM vs CoD vs Wardley vs Real Options. |
| `draft-adr` | sonnet | Compose ADR with chosen method + rationale + review trigger. |

## Templates

| File | Purpose |
|------|---------|
| `templates/method-selection-adr.md.j2` | ADR skeleton for trade-off method selection. |
| `templates/method-selection-adr.md` | ADR skeleton for trade-off method selection. Generated from `templates/method-selection-adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/method-fit-matrix.md.j2` | Lookup: context → method. |
| `templates/method-fit-matrix.md` | Lookup: context → method. Generated from `templates/method-fit-matrix.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trade-off-decision-methods.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trade-off-decision-matrix]]
- [[trade-off-quality-attributes]]
- [[quality-attributes]]
- [[decision-tree-process]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (question, shortlist, uncertainty, breadth)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
