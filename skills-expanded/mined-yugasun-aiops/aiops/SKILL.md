---
name: aiops
description: Flow Conductor for the aiops bundle. One entry — infers task type, shows plain-language steps, tracks journey in flow.state.yaml, dispatches skill + agent per phase.
disable-model-invocation: true
---

# aiops — Flow Conductor

Single entry for the bundle. Ordinary users only need this command; experts can still `/aiops <agent> …`.

## Invocation

```
/aiops <what you want>           # Conductor — infer, narrate, dispatch
/aiops 继续 / resume             # Resume from .scratch/<slug>/flow.state.yaml
/aiops <agent-name> <task>       # Expert — direct agent; still update journey if in a flow
```

Agents: `architect`, `design-reviewer`, `planner`, `prototyper`, `builder`, `ui-designer`, `code-reviewer`, `quality-auditor`, `gitops`

## Conductor loop (every turn)

1. **Resume or start** — Read `.scratch/<slug>/flow.state.yaml` if user resumes or slug known. If `current_phase_id` is `done`, inform user the journey is complete. Else infer slug (kebab-case from description; user may override). See [journey.md](journey.md).
2. **Bootstrap** — If `docs/agents/` missing, run **bootstrap** inline:
   - No `aiops.yaml` → silent defaults: local markdown issues + 1:1 triage labels ([aiops-setup/aiops-yaml.md](../aiops-setup/aiops-yaml.md)).
   - `aiops.yaml` with `issue_tracker.kind: github|gitlab` → seed GitHub/GitLab tracker docs from yaml; do not prompt for tracker unless yaml incomplete.
   - Do not ask user to run another command.
3. **Plan** — Build `FlowState` from journey + repo signals (see [journey.md](journey.md)). **Default `delivery_mode: single_session`** unless user confirms multi or heuristics clearly warrant multi. Use `flow_cli.py plan` to generate the phase list.
4. **Narrate** — One block from [narration.md](narration.md): **Chinese** `title_zh`, `body_zh`, `artifact_zh`; English only in `title_en`. Hide skill/agent names unless user asks.
5. **Dispatch** — Load `agents/<agent>.md` when `agent` set; invoke `skill` for the phase. Gather `.scratch/<slug>/` inputs per agent Inputs.
6. **Gate** — Before advancing: run `flow_cli.py validate --slug <slug>` to verify gate artifacts. If validation fails, do not advance. On success, append gate name to `gates_satisfied`.
7. **Advance** — Run `flow_cli.py advance --slug <slug>` to update `current_phase_id` and `phases_done`. On handoff, advance journey **before** writing temp handoff doc.
8. **Delivery** — When phase is `delivery`, hand off to `/aiops-implement` (owns lean → tdd → prune → review). Do not interleave those gates from the conductor.

## Task types → phase tail (after bootstrap if needed)

| Task type | Phases (abbrev) | Grill | Ends at |
| --- | --- | --- | --- |
| **Feature** | align → design → design_review → task_breakdown → delivery → drift_check → ship | yes | `/gitops` |
| **Feature + UI** | + ui_mockup before design_review | yes | `/gitops` |
| **Bug** | diagnose → delivery → drift_check → ship | no | `/gitops` |
| **Incoming** | triage → (align if unclear) → delivery → drift_check → ship | conditional | `/gitops` |
| **Architecture health** | graph_build → architecture_scan → align → design → design_review → task_breakdown → delivery → drift_check → ship | yes | `/gitops` |
| **Prototype** | prototype only | — | `VERDICT.md` |
| **New personal skill** | skill_authoring checklist | yes | new `SKILL.md` |

Dispatch rows for `AGENTS.md` live in `skills/manifest.json` → `dispatch`. Phase order detail: `skills/aiops/scripts/phases.py`.

**Explore** (opt-in): when `explore_requested`, insert `explore` phase after bootstrap (if any) and before task-specific phases.

**Multi-session**: after design_review → `planning_prd` → `planning_issues` → `issue_session` → delivery per issue. Single-session: after design_review → `task_breakdown` → delivery.

**Prototype branch** (optional): handoff → `/prototype` → handoff back; require `VERDICT.md` before planner/builder.

Lean is **not** active during grill/alignment phases.

## Multi-session heuristic

Recommend **multi-session** when: 3+ modules, multiple slices, near smart zone, or AFK per-issue. **Default single-session** — single-session still includes `task_breakdown` (lightweight tasks.md); multi-session uses full `planning_prd` → `planning_issues` → `issue_session`.

## New personal skill checklist

1. Purpose and trigger scenarios
2. User-invoked vs model-invoked
3. Steps vs reference files (progressive disclosure)
4. Author `SKILL.md` — Cursor **create-skill** (External; `docs/skill-registry.md`)

## Reference

- Journey file format: [journey.md](journey.md)
- User narration keys: [narration.md](narration.md)
- State operations: `python3 <aiops-root>/skills/aiops/scripts/flow_cli.py {plan,init,advance,validate,satisfy-gate,phase-gates}`
- Project config yaml: [aiops-setup/aiops-yaml.md](../aiops-setup/aiops-yaml.md)
- Vocabulary: target `CONTEXT.md`; skill registry: `docs/skill-registry.md`
