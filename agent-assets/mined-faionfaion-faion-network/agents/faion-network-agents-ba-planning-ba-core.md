# Business Analysis Planning

## Summary

**One-sentence:** Produces five BABOK KA1 task artefacts (T1-T5) with named approvers, cadences, and lifecycles seeding all downstream BA work.

**One-paragraph:** Produces five BABOK KA1 task artefacts (T1-T5) with named approvers, cadences, and lifecycles seeding all downstream BA work. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Програма починає планову delivery-фазу і потребує п'ять окремих artefact'ів (T1-T5) з названими approver'ами та різною каденцією review.
- Гібридний plan-driven + change-driven engagement, де відсотки фіксуються per-artefact (70/30, 50/50), а не глобально.
- Активація суміжних ba-core методологій — KA1 сеть seeding-церемонія для stakeholder-analysis, requirements-lifecycle, ba-governance.
- Запуск BA performance loop з ≥3 метриками з null-baselines на першому циклі.

## Applies If (ALL must hold)

- A new initiative crosses from discovery to planned delivery and needs an explicit BA approach, stakeholder map, governance, information management, and performance plan.
- Program must demonstrate BABOK conformance to certifying bodies or internal QA (CCBA/CBAP, IIBA-aligned PMOs).
- Hybrid plan-driven + change-driven engagement where per-artefact baselined-vs-living declarations are needed.
- Sibling ba-core methodologies (stakeholder-analysis, ba-governance, requirements-lifecycle, elicitation-techniques) are about to be activated — KA1 is their prerequisite.
- Introducing BA performance metrics (rework rate, requirement defect density, elicitation throughput).

## Skip If (ANY kills it)

- Solo MVP, prototype, or research spike — five KA1 tasks are heavier than the work itself; use a one-page lean canvas.
- Pure backlog-driven Scrum where the Definition of Ready already encodes the BA approach.
- Continuous-discovery context where requirements churn weekly — KA1 baselines go stale faster than they can be reviewed.
- Sponsor refuses to name a governance approver — KA1 governance becomes decorative.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Initiative brief | Markdown / Confluence page | sponsor |
| Org chart | CSV / HRIS export | people-ops |
| Existing methodology decision (Agile / Waterfall / hybrid) | ADR / steering memo | PMO |
| Tooling inventory (Jira / Confluence / GitHub) | list | operations |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[stakeholder-analysis]] | downstream consumer of T2 stakeholder list |
| [[ba-governance]] | downstream consumer of T3 governance plan |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-t1-t5` | sonnet | Apply BABOK KA1 template across five artefacts; deterministic structure with judgement on approach percentages. |
| `score-cadence` | haiku | Mechanical mapping of artefact type to review-cadence-days. |
| `review-coherence` | opus | Cross-check T2-T5 dependency chain against T1 approach declaration. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ba-approach-document.md.j2` | T1 plan-BA-approach skeleton with stakeholders, elicitation plan, deliverables, governance. |
| `templates/ba-approach-document.md` | T1 plan-BA-approach skeleton with stakeholders, elicitation plan, deliverables, governance. Generated from `templates/ba-approach-document.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ka1-bundle-skeleton.md.j2` | Bundle index linking T1-T5 artefacts in dependency order. |
| `templates/ka1-bundle-skeleton.md` | Bundle index linking T1-T5 artefacts in dependency order. Generated from `templates/ka1-bundle-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ka1_check.py` | Helper that verifies the 5 KA1 artefacts exist and are within review cadence; emits JSON. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[stakeholder-analysis]]
- [[ba-governance]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
