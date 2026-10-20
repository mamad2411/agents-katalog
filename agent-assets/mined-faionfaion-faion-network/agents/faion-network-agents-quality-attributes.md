# Quality Attributes Framework

## Summary

**One-sentence:** Captures non-functional requirements (NFRs) as ISO-25010 quality scenarios with stimulus-response measurements, prioritised by ATAM utility tree; emits NFR spec + SLI/SLO doc.

**One-paragraph:** Captures non-functional requirements (NFRs) as ISO-25010 quality scenarios with stimulus-response measurements, prioritised by ATAM utility tree; emits NFR spec + SLI/SLO doc. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Service or product is past requirements gathering and needs measurable NFRs.
- Architecture review identifies missing or qualitative NFRs that block SLO definition.
- ATAM-style trade-off analysis is required (regulated, high-impact, cross-team domain).
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Service or product is past requirements gathering and needs measurable NFRs.
- Architecture review identifies missing or qualitative NFRs that block SLO definition.
- ATAM-style trade-off analysis is required (regulated, high-impact, cross-team domain).

## Skip If (ANY kills it)

- Throwaway prototype or pre-revenue experiment with no contractual quality requirements.
- Internal CLI tool used by a single team — NFRs implicit in usability conversation.
- Existing NFR doc still valid; review only needed if context changes materially.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stakeholder list with roles | table | PM |
| Top-5 business goals | list | product |
| Current SLI catalog (if any) | table | SRE |
| Compliance + regulatory matrix | table | legal |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[performance-architecture]] | Latency / throughput SLOs land here as performance scenarios. |
| [[security-architecture]] | Security NFRs land here as security scenarios. |

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
| `collect-scenarios` | sonnet | Interview stakeholders to elicit stimulus-response scenarios. |
| `build-utility-tree` | sonnet | Diverge / converge: cluster scenarios by quality attribute. |
| `define-sli-slo` | sonnet | Translate scenarios into SLIs + SLO numbers. |
| `score-tradeoffs` | haiku | Mechanical weighting + conflict-matrix construction. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nfr-scenario.md.j2` | Single ATAM-style scenario skeleton. |
| `templates/nfr-scenario.md` | Single ATAM-style scenario skeleton. Generated from `templates/nfr-scenario.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/nfr-spec.md.j2` | NFR spec template aggregating scenarios into ISO-25010 categories. |
| `templates/nfr-spec.md` | NFR spec template aggregating scenarios into ISO-25010 categories. Generated from `templates/nfr-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-quality-attributes.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[performance-architecture]]
- [[security-architecture]]
- [[trade-off-quality-attributes]]
- [[trade-off-decision-matrix]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (stakeholders, goals, SLIs, compliance)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
