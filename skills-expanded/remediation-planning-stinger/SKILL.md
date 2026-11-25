---
name: remediation-planning-stinger
description: Plan fixes from audit findings. Clusters findings into work packages, orders Now, Next, Later, and with approval writes Library PRDs, IRDs, knowledge docs, and draft contracts.
license: AGPL-3.0-or-later
compatibility: Claude Code, Cursor, ChatGPT Codex, Claude Cowork. Python 3.9 or newer for scripts/build_plan.py (standard library only). Needs library-stinger, knowledge-stinger, contract-writing-stinger for the optional Library step.
metadata:
  author: Legion Code Inc.
  hive-drone: remediation-planning-wasp-drone
  pair-drone: remediation-planning-wasp-drone
  domain: remediation planning
  version: 1.0.0
  research-window: 2026-03-30 to 2026-09-30
---

# Remediation Planning Stinger

Designed and built by [Legion Code Inc.](https://www.legioncodeinc.com)

## Where this skill's files are

Every path below (`guides/`, `references/`, `scripts/`, `templates/`) is relative to the folder that contains this `SKILL.md`. If you cannot resolve it, find it with Glob for `**/remediation-planning-stinger/SKILL.md` and use that folder.

## Purpose

This is the last analysis step of the Mario Audit. It takes every finding written by the foundation, bloat, security and quality Drones and turns them into a plan a team can execute: a roadmap in Now, Next and Later waves, a machine-readable `plan.json`, and (only with the user's approval of the exact file list) Library Schema v2 documents inside the audited repository: PRDs for each work package, IRDs for discrete defects, knowledge docs for areas that are not yet documented, and draft shared contracts where two PRDs meet. It plans; it never changes source code.

## When to use

- The orchestrator reaches the remediation dimension of `/audit-my-code mario`
- "Turn these audit findings into a plan", "what do we fix first", "write PRDs for these findings"
- A workspace has `findings.jsonl` files and the user wants roadmap and Library documents

## When not to use

- Fixing the findings: route to the owner Drones named in the roadmap through `pest-controller-suit`
- Writing a PRD for a new feature with no audit behind it: `library-stinger`
- Finding problems in the first place: the dimension Drones (`code-foundation-wasp-drone`, `code-bloat-wasp-drone`, `security-wasp-drone`, `quality-wasp-drone`)
- Creating or scaffolding `library/`: `get-started-stinger`. This skill never creates the Library.
- Accepting shared contracts: only the user accepts a contract

## Procedure

1. Read `guides/00-inputs-and-consent-gate.md`. Confirm inputs and whether `library/` exists. Run `scripts/build_plan.py` for the first cut.
2. Read `guides/01-cluster-findings-into-work-packages.md`. Refine clusters by root cause and code area, never one PRD per finding.
3. Read `guides/02-prioritization-and-waves.md` and `references/prioritization-rules.md`. Assign waves, dependencies and owner Drones.
4. Write `04-remediation/roadmap.md` (template in `templates/roadmap-template.md`) and `04-remediation/plan.json` (schema in `references/plan-schema.md`). These two always get written.
5. Ask for approval of the exact `library/` file list (template `templates/consent-request.md`). If `library/` is missing, stop and tell the orchestrator to offer the get-started-stinger playbook. If the user declines, finish here.
6. With approval only: follow `guides/03-prds-irds-and-contracts.md` and `guides/04-knowledge-docs-via-knowledge-stinger.md`, loading `library-stinger`, `knowledge-stinger` and `contract-writing-stinger` first.
7. Follow `guides/05-handoff.md`: tell the user how to run the plan with `/smoke-it` and `/pest-controller`.
8. Report: files written, coverage (every finding in exactly one package), open questions.

## References map

| Path | Load when |
| --- | --- |
| `guides/00-inputs-and-consent-gate.md` | First, every run |
| `guides/01-cluster-findings-into-work-packages.md` | Grouping findings |
| `guides/02-prioritization-and-waves.md` | Ordering and sequencing |
| `guides/03-prds-irds-and-contracts.md` | After approval, writing PRDs, IRDs, CTR drafts |
| `guides/04-knowledge-docs-via-knowledge-stinger.md` | After approval, writing knowledge docs |
| `guides/05-handoff.md` | Finishing |
| `references/plan-schema.md` | Writing plan.json and roadmap.md |
| `references/prioritization-rules.md` | Setting waves, scores, effort, risk |
| `references/refactoring-sequences.md` | Splitting structural packages into safe steps |
| `references/acceptance-criteria-patterns.md` | Writing measurable criteria |
| `references/owner-routing.md` | Choosing the owner Drone |
| `references/research/distilled-remediation-planning.md` | Verifying a claim or settling a dispute |
| Source research archive (not shipped with the plugin) | Source-repository only; the shipped distillation summarizes it, do not require it |
| `templates/roadmap-template.md`, `templates/consent-request.md` | Writing the roadmap and asking for approval |
| `scripts/build_plan.py` | Step 1, first-cut plan; `python3 scripts/test_build_plan.py` checks it |

## Related drones and stingers

- `library-stinger` (Wasp Nest core) - Library Schema v2 templates, naming and lifecycle for PRDs and IRDs. Required for the Library step.
- `knowledge-stinger` (Wasp Nest core) - Knowledge doc format and domain taxonomy. Required for the Library step.
- `contract-writing-stinger` (Wasp Nest core) - Draft shared contracts between PRDs.
- `pest-controller-suit` (Wasp Nest core) - Roster used to name owner Drones.
- `get-started-stinger` (Wasp Nest core) - Offered when `library/` is missing.
- [audit-my-code-stinger](../audit-my-code-stinger) - The run contract this skill reads and writes against.
- [remediation-planning-wasp-drone](../../agents/remediation-planning-wasp-drone.md) - The paired agent.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - `library-stinger` (Wasp Nest core) - PRD and IRD authoring and lifecycle.
  - `knowledge-stinger` (Wasp Nest core) - Narrative knowledge docs.
  - `contract-writing-stinger` (Wasp Nest core) - Shared contracts between PRDs.
  - `pest-controller-suit` (Wasp Nest core) - Routing roster.

<!-- Ship Gate removed: research-only stinger, produces no committable code. -->

---

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.
