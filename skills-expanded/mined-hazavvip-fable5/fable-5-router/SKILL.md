---
name: fable-5-router
description: >-
  Fable6 MD-first phase router (v6). Read state.json → PLAYBOOK.md.
  No fable-run.py. Alias of fable-6-router behavior.
version: 6.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent]
---

# Fable6 Router

> Same canon as `fable-6-router`. See `docs/AGENT_SPINE.md`.

## On target

1. Read `campaigns/{target}/state.json` → `current_phase`
2. Load `Workflow/{current_phase}/PLAYBOOK.md`
3. Execute AGENT_SPINE loop
4. Update `state.json` directly when phase done

## Phase skills

| Phase | Skill |
|-------|-------|
| pre-engagement | fable-6-intake |
| reconnaissance | fable-6-recon |
| initial-access | fable-6-initial-access |
| resource-development | fable-6-resource-dev |
| execution | fable-6-execution |
| post-exploitation | fable-6-post-exploit |
| persistence | fable-6-persistence |
| defense-evasion | fable-6-defense-evasion |
| report | fable-6-report |

## FORBIDDEN

- Removed v6.1: target_intake, fable-run, fable-phase-advance, enforcement
