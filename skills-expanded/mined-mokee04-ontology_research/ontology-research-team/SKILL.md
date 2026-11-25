---
name: ontology-research-team
description: Run the research stage for a domain ontology project by collecting primary sources, checking whether the needed data is actually collectible in practice, curating evidence, identifying reuse candidates, and writing research artifacts to the exe folder.
---

# Ontology Research Team

Read:

- `../refs/Total Guide.md`
- `../shared/references/exe-artifact-contract.md`
- `../shared/references/templates.md`

Use this skill after planning is complete and before ontology construction begins.

## Research Segments

| Segment | Goal | Required user feedback |
| --- | --- | --- |
| R1 Research framing | confirm what must be answered now and what can wait | yes |
| R2 Internal data feasibility | inspect what data can actually be collected | yes |
| R3 External source triage | identify reusable sources and standards | yes |
| R4 Evidence synthesis | separate feasible scope from aspirational scope | yes |

## Team Composition

Route research work through:

- `ontology-source-scout`
- `ontology-evidence-curator`

## Tasks

1. Start from competency questions and required standards.
2. Reconfirm with the user which questions are highest priority before expanding the research scope.
3. Prefer primary and official sources first.
4. Check whether each important concept or relation can be supported by data that is realistically obtainable, licensable, and maintainable.
5. Log the research process, not just the conclusion.
6. Build a source inventory with keep, reject, or pending status.
7. Curate evidence for concepts, definitions, relations, constraints, reuse candidates, and data collection feasibility.
8. Produce a feasibility-oriented synthesis that can be handed to the build team, clearly separating feasible modeling scope from aspirational scope.
9. Pause at each segment and ask the user whether to narrow, expand, or reprioritize the research focus.

## EXE Rule

All research process logs and results must be written under:

- `../exe/<run-id>/research/queries.md`
- `../exe/<run-id>/research/source-inventory.md`
- `../exe/<run-id>/research/evidence-log.md`
- `../exe/<run-id>/research/synthesis.md`
- `../exe/<run-id>/research/reuse-candidates.md`

## Exit Criteria

Do not hand off to build until:

- the source inventory exists
- evidence is linked to sources
- data collection feasibility has been checked for the main planned ontology scope
- reusable standards or ontology candidates are identified
- unresolved ambiguities are named
- a research checkpoint has been reviewed with the user
