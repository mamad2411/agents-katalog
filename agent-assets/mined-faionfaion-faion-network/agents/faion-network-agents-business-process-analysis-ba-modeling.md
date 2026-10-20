# Business Process Analysis

## Summary

**One-sentence:** 5-stage cycle (identify → document → analyze → future-state → validate) that turns raw process evidence into BPMN + a value/time/cost analysis report.

**One-paragraph:** Pre-automation discovery for cross-team workflows: identify candidate processes, document current state with source citations, run a value/time/cost analysis, design a future state expressed as a diff table (not prose), and validate with stakeholders. Output artefacts: `process-documentation.md`, `process-analysis.md`, BPMN XML, and a future-state diff. The report becomes the input contract for the downstream automation team (n8n, RPA, backend service).

**Ефективно для:**

- Pre-automation discovery перед написанням n8n / RPA / backend сервісу.
- Cross-team workflows із symptoms of waste (rework, dual entry, long queues).
- Compliance / audit prep — документований process map з controls.
- Pre-spec stage BA-heavy SDD feature; output → requirements + AC.

## Applies If (ALL must hold)

- Raw process evidence exists (SOPs, Slack threads, ticket histories, transcripts).
- A cross-team workflow shows symptoms of waste (rework loops, long queues, dual entry).
- Pre-automation discovery is required before writing an n8n/RPA/backend service.
- Stakeholders for each lane can be named and reached for validation.

## Skip If (ANY kills it)

- Greenfield product where no current process exists — use use-case-modeling or user-story-mapping.
- One-off troubleshooting of a single broken instance — use 5-whys / fishbone.
- Tactical UI tweaks where the "process" is one click.
- Highly creative / knowledge-work flows (R&D, design) where steps are non-deterministic.
- Team is already mid-redesign and stakeholders have agreed on future state.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Process evidence | SOPs, transcripts, ticket exports | ops team |
| Stakeholder list | `stakeholders.md` with named owner per lane | BA |
| Cost + cycle-time data | spreadsheet (per-step duration, FTE rate) | finance / ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ba-planning]] | Upstream plan that sets BA approach + governance |
| [[bpmn-via-ai-then-human-review]] | AI-assisted BPMN drafting pattern this cycle reuses |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: source citation per step, named owner per lane, value/time/cost tables required, future-state as diff, stakeholder sign-off | 950 |
| `content/02-output-contract.xml` | essential | JSON Schema for process-analysis report + examples | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: prose without diagram, anonymous lanes, future-state without metric delta, sign-off skipped | 900 |
| `content/04-procedure.xml` | essential | 5-step cycle end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example: invoice-approval process before/after | 700 |
| `content/06-decision-tree.xml` | essential | Routing on evidence completeness + stakeholder access | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify_processes` | sonnet | Pattern-match candidates from evidence. |
| `draft_bpmn` | sonnet | Translate prose to BPMN structure. |
| `value_analysis` | opus | Multi-dimensional value/time/cost reasoning. |
| `future_state_diff` | opus | Decide what to keep/cut/add with rationale. |

## Templates

| File | Purpose |
|------|---------|
| `templates/process-analysis.md.j2` | Markdown skeleton for the report (current + analysis + future + diff) |
| `templates/process-analysis.md` | Markdown skeleton for the report (current + analysis + future + diff) Generated from `templates/process-analysis.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum filled-in report for the smoke fixture |
| `templates/_smoke-test.md` | Minimum filled-in report for the smoke fixture Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/process-documentation.md.j2` | current-state documentation skeleton (lanes + steps + sources) |
| `templates/process-documentation.md` | current-state documentation skeleton (lanes + steps + sources) Generated from `templates/process-documentation.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[bpmn-via-ai-then-human-review]]
- [[interface-analysis]]
- [[data-analysis]]
- [[ba-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes on observable signals (evidence completeness, stakeholder availability, automation downstream Yes/No) to the right step of the cycle and the matching rule. Use when in doubt whether the analysis is ready to advance to future-state design.
