# Business Process Analysis — Enterprise Scale and Governance

## Summary

**One-sentence:** Five-stage BPA loop (identify → document → analyze → design → validate) under portfolio-agent orchestration that produces auditor-grade as-is/to-be process models with NVA-percentage baselines.

**One-paragraph:** A five-stage methodology for documenting how work actually flows through an organization (current state), classifying each step as value-adding (VA), business-necessary (BN), or non-value-adding (NVA), and designing a measurable future state. At enterprise scale (M&A, ERP rollout, digital transformation), a portfolio agent maintains the process inventory while per-process agents apply the 5-stage loop against APQC PCF or SCOR reference frameworks. Output is a BPMN model repository plus a structured diff table per process driving the implementation plan.

**Ефективно для:**

- програм трансформації з ≥100 процесів, де неможливо документувати все одним агентом і потрібна портфельна оркестрація.
- M&A інтеграцій з вибором acquirer/target/hybrid процесів і доказовою trace на deal-thesis.
- ERP gap-fit аналізу з обов'язковим adopt→configure→extend→build порядком.
- Аудиту SOX 404 / ISO 9001 з vendor-незалежними BPMN моделями у version control.

## Applies If (ALL must hold)

- M&A integration requiring Day-1/Day-100/target-state process comparison across two organizations' inventories.
- ERP/CRM/HCM rollout (SAP S/4HANA, Oracle Fusion, Workday) — gap-fit analysis against vendor reference processes.
- Digital transformation programme: 100–500 processes scored on maturity, automation readiness, customer impact.
- Pre-IPO/pre-acquisition due diligence (SOX 404, ISO 9001) requiring auditor-grade process narratives with control points.
- Shared-services/GBS design consolidating multiple business units into one process model.

## Skip If (ANY kills it)

- Single-team local workflow — enterprise governance overhead is unjustified; use lightweight process mapping.
- Greenfield startup with no installed process estate — jump to use-case-modeling or user-story-mapping.
- Pure customer-experience redesign — use customer-journey-mapping; BPA is downstream.
- Single broken process instance requiring root-cause analysis — use 5-whys/fishbone.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Process inventory seed | CSV / XLSX | BU heads + org chart mining |
| Reference framework | APQC PCF / SCOR / eTOM XML | vendor or APQC subscription |
| Deal thesis / programme charter | Markdown / PDF | sponsor |
| Volume + cycle time data | JSON / CSV from system logs | process-mining-automation upstream |
| BPMN convention guide | Markdown | standards/bpmn-conventions.md (this methodology) |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/elicitation-techniques` | Sources current-state evidence from operators. |
| `pro/ba/business-analyst/frontline-validation-protocol` | Two-operator validation gate for as-is models. |
| `pro/ba/business-analyst/process-mining-automation` | Provides event-log conformance metrics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `portfolio-agent-inventory-maintenance` | sonnet | Read-heavy aggregation across N processes. |
| `per-process-as-is-modelling` | sonnet | Per-process narrative + BPMN draft. |
| `nva-classification` | haiku | Mechanical step-by-step tagging. |
| `diff-table-synthesis` | opus | Cross-system trade-offs and risk reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/process-analysis.md.j2` | Per-process analysis narrative with VA/BN/NVA classification + baseline metrics. |
| `templates/process-analysis.md` | Per-process analysis narrative with VA/BN/NVA classification + baseline metrics. Generated from `templates/process-analysis.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/process-documentation.md.j2` | BPMN-linked process documentation skeleton with control-point markers. |
| `templates/process-documentation.md` | BPMN-linked process documentation skeleton with control-point markers. Generated from `templates/process-documentation.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/rank-portfolio.py` | Score processes by nva_minutes_per_year × strategic_fit and emit the deep-modelling Pareto set. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in process analysis. |
| `templates/_smoke-test.md` | Minimum viable filled-in process analysis. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-business-process-analysis.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[frontline-validation-protocol]]
- [[process-mining-automation]]
- [[elicitation-techniques]]
- [[modern-ba-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
