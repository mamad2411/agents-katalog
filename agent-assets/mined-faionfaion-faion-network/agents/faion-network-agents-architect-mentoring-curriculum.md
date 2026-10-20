# Architect Mentoring Curriculum

## Summary

**One-sentence:** Produces a 6-month mentoring curriculum for staff engineers transitioning into architect roles.

**One-paragraph:** Produces a 6-month mentoring curriculum for staff engineers transitioning into architect roles. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- 6-місячна curriculum для staff → architect transition з phased autonomy.
- Чіткий rubric-to-graduate з conviction (не суб'єктивне 'feels ready').
- Mentor pool ≥2: уникнення single-mentor blind spots.

## Applies If (ALL must hold)

- Candidate is a staff engineer with ≥2 years system-design experience.
- Organization has ≥2 architects who can serve as mentors.
- Org has a defined architect-level rubric to graduate against.

## Skip If (ANY kills it)

- Candidate is mid-level — too early; refer to staff-track curriculum.
- Org has no architect-level rubric — define one first.
- Mentor pool of 0 or 1 — single point of failure.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Architect-level rubric | markdown | head of engineering |
| Candidate self-assessment vs rubric | markdown | candidate |
| Mentor availability per week | calendar | mentor pool |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[architecture-review-meeting-facilitation]] | Curriculum embeds shadow-then-facilitate cycles of arch review |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 4-step procedure with input/action/output per step | 1000 |
| `content/05-examples.xml` | reference | One full worked example end-to-end | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/curriculum-spec.md.j2` | 6-month curriculum skeleton with month-by-month milestones |
| `templates/curriculum-spec.md` | 6-month curriculum skeleton with month-by-month milestones Generated from `templates/curriculum-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/mentor-pairing-doc.md.j2` | Per-mentor pairing doc with focus area + cadence |
| `templates/mentor-pairing-doc.md` | Per-mentor pairing doc with focus area + cadence Generated from `templates/mentor-pairing-doc.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in curriculum for a Staff → Architect candidate |
| `templates/_smoke-test.md` | Filled-in curriculum for a Staff → Architect candidate Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-architect-mentoring-curriculum.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-review-meeting-facilitation]]
- [[architecture-proposal-document-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
