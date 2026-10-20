# Architecture Decision Process

## Summary

**One-sentence:** Six-phase architecture decision process (problem, options, trade-off, validation, ADR, implementation) that emits a complete decision report with weighted matrix + ADR + rollback plan.

**One-paragraph:** Six-phase architecture decision process (problem, options, trade-off, validation, ADR, implementation) that emits a complete decision report with weighted matrix + ADR + rollback plan. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Significant architecture choice with one-way-door reversibility (style, framework, cloud, data store).
- Cross-team or cross-stakeholder decision needing explicit weighting and documentation.
- Decision where 'why did we choose this?' will be asked again within 12 months.
- Output produces `report` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Significant architecture choice with one-way-door reversibility (style, framework, cloud, data store).
- Cross-team or cross-stakeholder decision needing explicit weighting and documentation.
- Decision where 'why did we choose this?' will be asked again within 12 months.

## Skip If (ANY kills it)

- Trivial reversible decision (lightweight library, CLI tool) — a one-line PR comment is enough.
- Time-critical emergency where action precedes documentation — decide now, document retroactively.
- Decision already made and working; only run the process at the scheduled review interval.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Problem statement as a single question | Markdown bullet | team |
| Stakeholder list with roles | table | PM / lead |
| Constraints (budget, timeline, team skills) | table | team |
| Reversibility classification (one-way / two-way) | field | architect |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[trade-off-decision-matrix]] | Phase 3 uses the weighted decision matrix. |
| [[trade-off-decision-methods]] | Phase 3 may invoke ATAM / cost-of-delay if the matrix is insufficient. |

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
| `phase1-problem-definition` | sonnet | Force a single-question statement; mark reversibility. |
| `phase2-options-generation` | opus | Diverge / converge; include do-nothing + unconventional option. |
| `phase3-tradeoff-analysis` | sonnet | Mechanical weighted matrix scoring with stakeholder weights. |
| `phase4-validation` | sonnet | Design POC scope + success criteria for high-impact one-way doors. |
| `phase5-documentation` | sonnet | Compose ADR (MADR / Y-statement). |
| `phase6-implementation` | haiku | Generate task list + monitoring + review cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-process-report.md.j2` | End-to-end report skeleton covering all six phases. |
| `templates/decision-process-report.md` | End-to-end report skeleton covering all six phases. Generated from `templates/decision-process-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/tradeoff-matrix.json` | Weighted matrix payload consumed in Phase 3. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-tree-process.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trade-off-decision-matrix]]
- [[trade-off-decision-methods]]
- [[decision-tree-tech-stack]]
- [[decision-tree-cloud-provider]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the decision a high-impact or one-way-door choice that meets the prerequisites?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
