---
name: workflow-router
description: 'forge workflow router — Use when you need to: implement a feature or task; do periodic context-system maintenance; rewrite reader-facing docs / README / positioning; fix a bug or handle an incident; research, evaluate or spike; review or validate a spec; persist a session; solve a problem whose solution shape is still open; → use the direct common or method entry; start the engine only for selected development.'
status: active
invocation:
  primary: user-facing
disable-model-invocation: false
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.
Without Buddy (plugin): if this session holds no Buddy boot entry, run `python3 <root>/scripts/forge_setup.py offer-check` once, as its own call (`<root>`: two levels above this skill's folder); if it prints a line, pass that offer to the user in one sentence, then continue with this skill.


# Skill: workflow-router

<!-- generated-by: scripts/generate_workflow_router.py (do not hand-edit) -->

This is forge's workflow discovery router — one injected sign-post that points to the workflow runbooks. It carries no workflow methodology; the runbooks (`workflows/runbooks/<name>/WORKFLOW.md`) and `framework/process-map.md` are the SoT.

| Entry | Use case | Owner | Dispatch |
|---|---|---|---|
| `build` | implement a feature or task | `workflows/runbooks/build/WORKFLOW.md` | Selected development engine |
| `context_housekeeping` | do periodic context-system maintenance | `workflows/runbooks/context_housekeeping/WORKFLOW.md` | Direct common procedure |
| `docs-rewrite` | rewrite reader-facing docs / README / positioning | `workflows/runbooks/docs-rewrite/WORKFLOW.md` | Selected development engine |
| `fix` | fix a bug or handle an incident | `workflows/runbooks/fix/WORKFLOW.md` | Selected development engine |
| `research` | research, evaluate or spike | `workflows/runbooks/research/WORKFLOW.md` | Selected development engine |
| `review` | review or validate a spec | `workflows/runbooks/review/WORKFLOW.md` | Selected development engine |
| `save` | persist a session | `workflows/runbooks/save/WORKFLOW.md` | Direct common procedure |
| `solve` | solve a problem whose solution shape is still open | `workflows/runbooks/solve/WORKFLOW.md` | Selected development engine |
| `bedrock-drill` | Reason about the supplied problem | `skills/bedrock_drill/SKILL.md` | Direct generic method |
| `frame` | Reason about the supplied problem | `skills/frame/SKILL.md` | Direct generic method |
| `council` | Reason about the supplied problem | `skills/council/SKILL.md` | Direct generic method |

Save and housekeeping invoke their common runbook directly. Bedrock, Frame and Council invoke their skill directly; installation availability never selects development. For selected development, open `framework/process-map.md`, then start the matching engine workflow: `python3 scripts/workflow_engine.py --start <name> --task <id>`. Existing bound runs retain their engine obligations.
