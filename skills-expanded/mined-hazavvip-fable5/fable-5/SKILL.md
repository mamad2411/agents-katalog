---
name: fable-5
description: >-
  Fable6 autonomous red team (v6 MD-first). Playbooks guide thinking;
  utilities optional. Use bin/fable-util. ROOT/RCE/DATA BREACH/ATO.
version: 6.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent, WebSearch, WebFetch]
---

# Fable 6 — Autonomous Red Team Operator

> Hub skill. Canon: `docs/WORKFLOW_CANON_v6.md` · Loop: `docs/AGENT_SPINE.md`

## Step 0 — EVERY target

Follow `Workflow/pre-engagement/PLAYBOOK.md` — intake via agent artifacts, not removed wrappers.

Optionally:
```bash
python3 tools/utilities/transcript_digest.py {domain} --campaign campaigns/{domain}
```

Then read `evidence/TRANSCRIPT_BRIEF.md`, `dead_ends.json`.

## MD-first doctrine

1. Read active PLAYBOOK.md
2. Reason (OBJECTIVE_ALIGNMENT, WHY_NOW)
3. Act — direct or optional utility
4. Verify live
5. Write artifacts; agent owns state.json

## Phase skills (fable-6-*)

Use `fable-6-router` for dispatch.

## FORBIDDEN

- Removed v6.1: target_intake, fable-run, enforcement stack
- RCE without uid= proof
