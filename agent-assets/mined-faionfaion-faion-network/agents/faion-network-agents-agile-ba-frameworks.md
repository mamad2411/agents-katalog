# Agile BA Frameworks Mapping

## Summary

**One-sentence:** Map BA competencies onto Scrum ceremonies + SAFe levels (Team / Program / Solution / Portfolio) — produces a `spec` of which BA activity fires when.

**One-paragraph:** Map BA competencies onto Scrum ceremonies + SAFe levels (Team / Program / Solution / Portfolio) — produces a `spec` of which BA activity fires when. Captured as a versioned artefact downstream agents and reviewers consume without re-deriving rationale. Mechanism: typed input → bounded transformation → contract-checked output.

**Ефективно для:**

- Onboarding BA до Scrum / SAFe org.
- Audit BA-activity coverage across ceremonies.
- Multi-team coordination — який BA fires when.
- Performance-review framework для BA contributions.

## Applies If (ALL must hold)

- Org runs Scrum or SAFe (Team/Program/Solution/Portfolio).
- ≥1 BA active across teams.
- Cadence is consistent (sprint length, PI length).
- Activity inventory can be enumerated.

## Skip If (ANY kills it)

- Non-agile delivery model (waterfall, ad-hoc).
- Solo BA scope (no cross-team mapping needed).
- Pre-agile transition discovery; use change-management instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent task context (30 days) | Markdown / tracker | BA |
| Write access to artefact store | repo / wiki | engagement manager |
| Named downstream owner | stakeholder list | BA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ba-planning]] | Companion / upstream methodology |
| [[acceptance-criteria]] | Sibling artefact in the same lifecycle |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + examples | 800 |
| `content/03-failure-modes.xml` | essential | Antipatterns | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Mechanical template fill. |
| `synthesize_decision` | sonnet | Per-instance bounded judgment. |
| `review_for_compliance` | opus | Cross-input synthesis on high-stakes outputs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agile-ba-frameworks.json` | Skeleton artefact with required fields |
| `templates/_smoke-test.json` | Minimum viable filled artefact |
| `templates/sprint-ba-activities.md.j2` | Per-sprint BA activity checklist — refinement, planning, in-sprint, review and retrospective duties. |
| `templates/sprint-ba-activities.md` | Per-sprint BA activity checklist — refinement, planning, in-sprint, review and retrospective duties. Generated from `templates/sprint-ba-activities.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agile-ba-frameworks.py` | Validate artefact against output-contract | After subagent returns; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ba-planning]]
- [[acceptance-criteria]]
- [[ba-standup-script-template]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on artefact-state signal to the active rule.
