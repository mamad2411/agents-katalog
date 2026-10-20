# SDD Document Templates

## Summary

**One-sentence:** A collection of canonical templates for every SDD artifact: Constitution, Spec, Design, Implementation Plan, Task, Roadmap, Backlog Item, Confidence Check, Pattern Record, and Mistake Record.

**One-paragraph:** A collection of canonical templates for every SDD artifact: Constitution, Spec, Design, Implementation Plan, Task, Roadmap, Backlog Item, Confidence Check, Pattern Record, and Mistake Record. Use these as output schemas — provide a template in the system prompt, instruct the agent to fill each section, and enforce that no non-standard sections are added.

## Applies If (ALL must hold)

- Starting any SDD artifact from scratch — always start from the relevant template.
- Onboarding a new project: the Constitution template captures tech stack and standards before feature work begins.
- When a subagent must produce a spec, design, task, or implementation plan with consistent structure.
- Generating backlog items, roadmap entries, or confidence-check reports during planning sessions.

## Skip If (ANY kills it)

- When an SDD artifact already exists and only needs incremental updates — edit in place.
- For one-off notes or research spikes that do not feed into task execution.
- Generating freeform documentation not part of the SDD lifecycle.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| `templates/backlog-item.md.j2` | Single backlog item — RICE score, MoSCoW classification, acceptance criteria, dependencies. |
| `templates/backlog-item.md` | Single backlog item — RICE score, MoSCoW classification, acceptance criteria, dependencies. Generated from `templates/backlog-item.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/confidence-check.md.j2` | Phase-gate confidence check — weighted checklist, verdict (Proceed/Clarify/Stop), open questions, recommended actions. |
| `templates/confidence-check.md` | Phase-gate confidence check — weighted checklist, verdict (Proceed/Clarify/Stop), open questions, recommended actions. Generated from `templates/confidence-check.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/constitution.md.j2` | Project constitution — vision, tech stack, architecture patterns, code standards, git workflow, project structure, quality gates, principles. |
| `templates/constitution.md` | Project constitution — vision, tech stack, architecture patterns, code standards, git workflow, project structure, quality gates, principles. Generated from `templates/constitution.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/implementation-plan.md.j2` | Full implementation plan — task summary, dependency graph, execution waves, per-task detail, quality gates, FR/AD coverage, risks. |
| `templates/implementation-plan.md` | Full implementation plan — task summary, dependency graph, execution waves, per-task detail, quality gates, FR/AD coverage, risks. Generated from `templates/implementation-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/roadmap.md.j2` | Now/Next/Later product roadmap — milestones, not-planned items, dependencies, change log. |
| `templates/roadmap.md` | Now/Next/Later product roadmap — milestones, not-planned items, dependencies, change log. Generated from `templates/roadmap.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `solo/sdd/sdd-planning/`
