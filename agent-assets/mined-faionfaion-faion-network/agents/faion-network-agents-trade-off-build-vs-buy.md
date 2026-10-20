# Build vs Buy Decision Framework

## Summary

**One-sentence:** Decides Build / Buy / Hybrid by scoring strategic differentiation, 3-year TCO, time-to-value, vendor lock-in, and integration cost. Emits ADR with quantified rationale.

**One-paragraph:** Decides Build / Buy / Hybrid by scoring strategic differentiation, 3-year TCO, time-to-value, vendor lock-in, and integration cost. Emits ADR with quantified rationale. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Capability that could be built in-house OR purchased / open-sourced.
- Budget owner needs a defensible recommendation with quantified rationale.
- Vendor evaluation: pilot completed and decision must be made.
- Output produces `decision-record` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Capability that could be built in-house OR purchased / open-sourced.
- Budget owner needs a defensible recommendation with quantified rationale.
- Vendor evaluation: pilot completed and decision must be made.

## Skip If (ANY kills it)

- Capability is core IP that competitors cannot replicate → Build is non-negotiable.
- Commodity capability with no strategic edge → Buy is non-negotiable.
- Pre-revenue exploration where neither build nor buy is on the timeline.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Capability description + scope | doc | PM |
| 3-year volume / usage forecast | data | PM / finance |
| Vendor shortlist with pricing | table | procurement |
| Internal build estimate (engineering-weeks) | data | tech lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[trade-off-decision-matrix]] | Scoring uses the weighted matrix shape. |

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
| `score-strategic-fit` | sonnet | Bounded judgement: differentiation × competitive-moat. |
| `compute-3y-tco` | sonnet | Bounded calc: build TCO vs buy TCO + integration. |
| `draft-adr` | sonnet | Compose ADR with chosen + rejected + exit plan. |

## Templates

| File | Purpose |
|------|---------|
| `templates/build-vs-buy-adr.md.j2` | ADR skeleton scoring build / buy / hybrid. |
| `templates/build-vs-buy-adr.md` | ADR skeleton scoring build / buy / hybrid. Generated from `templates/build-vs-buy-adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/tco-model.json` | TCO model inputs and computation shape. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trade-off-build-vs-buy.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trade-off-decision-matrix]]
- [[decision-tree-process]]
- [[decision-tree-tech-stack]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (capability, forecast, vendor shortlist, build estimate)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
