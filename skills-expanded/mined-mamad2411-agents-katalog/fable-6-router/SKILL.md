---
name: fable-6-router
description: >-
  Fable6 MD-first phase router. Read state.json, load PLAYBOOK.md, execute
  AGENT_SPINE loop. No script orchestrator.
version: 6.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent]
---

# Fable6 Router

**Trigger:** Operator supplies target domain/URL.

## Cognitive routing (no fable-run.py)

1. Read `docs/WORKFLOW_CANON_v6.md` and `docs/AGENT_SPINE.md`
2. Read or create `campaigns/{target}/state.json` → `current_phase`
3. Load `Workflow/{current_phase}/PLAYBOOK.md`
4. Execute loop: reason → optional utility → write artifacts → verify
5. When PLAYBOOK `done_when` met, update `state.json` → next phase

## Phase → skill hint

| current_phase | Focus |
|---------------|-------|
| pre-engagement | `fable-6-intake` |
| reconnaissance | `fable-6` → skill-recon |
| initial-access | skill-initial-access |
| resource-development | skill-resource-dev |
| execution | skill-execution |
| post-exploitation | skill-post-exploit |
| persistence | skill-persistence |
| defense-evasion | skill-defense-evasion |
| report | skill-report |

## FORBIDDEN

- Removed v6.1: fable-run, fable-phase-advance, enforcement, target_intake
- Auto-scaffold artifacts
- Skip PLAYBOOK read order
