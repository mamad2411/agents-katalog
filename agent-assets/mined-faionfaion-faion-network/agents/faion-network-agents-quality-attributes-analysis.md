# Quality Attributes Analysis

## Summary

**One-sentence:** Systematic QAA pass binding NFRs to structural decisions — ISO/IEC 25010:2023 characteristics, 6-part quality-attribute scenarios, utility tree with (Importance, Difficulty) scoring, ATAM-style tradeoff analysis — every (H,H) scenario gates an executable fitness function in CI.

**One-paragraph:** Systematic QAA pass binding NFRs to structural decisions — ISO/IEC 25010:2023 characteristics, 6-part quality-attribute scenarios, utility tree with (Importance, Difficulty) scoring, ATAM-style tradeoff analysis — every (H,H) scenario gates an executable fitness function in CI. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- A team is producing spec for the topic 'Quality Attributes Analysis'.
- Output is reviewed by a named human on a published cadence.
- Inputs and constraints fit the rules in `content/01-core-rules.xml`.

## Skip If (ANY kills it)

- One-shot work with no recurrence — write a single doc, not a versioned artefact.
- Regulated context that mandates a different template — use the regulator's.
- No named owner is available — defer until ownership is resolved.

**Ефективно для:**

- Pre-architecture phase of a non-trivial system surfacing NFRs.
- Major architectural pivot (monolith → microservices, on-prem → cloud, sync → async).
- Investor / customer due-diligence requiring evidence the architecture meets SLA / compliance promises.
- Postmortem after a perf/security/availability incident the original architecture did not anticipate.
- Multi-tenant or regulated domain (healthcare, finance, public-sector) requiring ISO 25010 traceability.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Base ADR format the output extends. |
| `pro/dev/software-architect` | Role/operating context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in instance. |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/scenario-template.md.j2` | One quality-attribute scenario — six-part (source/stimulus/environment/artifact/response/response-measure) plus a wired fitness function. |
| `templates/scenario-template.md` | One quality-attribute scenario — six-part (source/stimulus/environment/artifact/response/response-measure) plus a wired fitness function. Generated from `templates/scenario-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/utility-tree.md.j2` | ATAM-style utility tree — quality attributes scored (Importance, Difficulty), active (H,H) drivers, sensitivity points, trade-offs. |
| `templates/utility-tree.md` | ATAM-style utility tree — quality attributes scored (Importance, Difficulty), active (H,H) drivers, sensitivity points, trade-offs. Generated from `templates/utility-tree.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-quality-attributes-analysis.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-decision-records]]
- [[stride-threat-model-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
