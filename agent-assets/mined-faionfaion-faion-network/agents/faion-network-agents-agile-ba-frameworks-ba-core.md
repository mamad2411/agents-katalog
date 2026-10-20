# Agile BA Frameworks

## Summary

**One-sentence:** Picks the right Agile-BA framework (Scrum-BA, SAFe-BA, Disciplined Agile, Dual-Track) for a given team shape + cadence + regulatory bar, with named per-sprint BA activities and IIBA Agile-Extension 7-principle fit-report.

**One-paragraph:** Picks the right Agile-BA framework (Scrum-BA, SAFe-BA, Disciplined Agile, Dual-Track) for a given team shape + cadence + regulatory bar, with named per-sprint BA activities and IIBA Agile-Extension 7-principle fit-report. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- New squad — BA framework selection перед sprint-1.
- Existing team retro: BA activities либо missing либо overloaded.
- Scaling shift: single team → SAFe RTE — BA role змінюється.
- Discovery-delivery friction: discovery PB drifts faster than delivery PB.

## Applies If (ALL must hold)

- New initiative entering agile delivery OR major team / scope change in flight.
- BA function exists in the org (or being established).
- Constitution / playbook captures the framework decision.
- IIBA Agile Extension + at least one scaling reference (SAFe / DA / LeSS) on the table.

## Skip If (ANY kills it)

- Single-team Scrum with no scaling concern and no regulatory bar.
- Greenfield product discovery — use continuous-discovery / user-story-mapping.
- Non-software domain (marketing ops, HR change) — vocabulary misapplies.
- Pure tooling questions (Jira API, Linear webhooks) — frameworks are vendor-neutral.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Team composition + size | Markdown / org chart | Eng manager |
| Initiative scope brief | Markdown / Jira initiative | PM / sponsor |
| Regulatory / compliance bar | checklist | Compliance / legal |
| Framework-version pins | YAML in constitution | BA lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/ba/ba-core/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-agile-ba-frameworks` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md.j2` | Markdown decision record — context + options + decision + owner + last_reviewed |
| `templates/decision-record.md` | Markdown decision record — context + options + decision + owner + last_reviewed Generated from `templates/decision-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/decision-instance.json` | JSON instance of a filled decision record |
| `templates/framework-fit.md.j2` | Framework-fit report — IIBA AE / DA / SAFe comparison + recommendation + 7-principle gap table |
| `templates/framework-fit.md` | Framework-fit report — IIBA AE / DA / SAFe comparison + recommendation + 7-principle gap table Generated from `templates/framework-fit.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/sprint-ba-activities.md.j2` | Per-sprint BA activities checklist (refinement → planning → during → review → retro) |
| `templates/sprint-ba-activities.md` | Per-sprint BA activities checklist (refinement → planning → during → review → retro) Generated from `templates/sprint-ba-activities.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/ba/ba-core/AGENTS.md`
- [[ba-governance]]
- [[ai-user-story-decomposition]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
