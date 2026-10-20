---
name: fable-6-intake
description: >-
  Step 0 MD-first intake. Resume if state.json exists; optional fable-util digest/archaeology.
version: 6.1.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent]
---

# Fable6 Intake (Step 0)

**Trigger:** Any new target from operator.

## Read first

`Workflow/pre-engagement/PLAYBOOK.md`

## Resume rule (mandatory)

**If `campaigns/{target}/state.json` exists:**

1. Read state + existing artifacts
2. Do NOT rewrite TARGET_INTAKE or TRANSCRIPT_BRIEF unless missing
3. Jump to `current_phase` — skip completed intake

**Only full intake when no state.json or operator requests fresh start.**

## New campaign actions

1. Reason: scope; dead vectors from prior work
2. Optionally:

```bash
bin/fable-util digest {target} --campaign campaigns/{target}
bin/fable-util archaeology {target}
```

3. Read `evidence/TRANSCRIPT_BRIEF.md`, `dead_ends.json` if present
4. Write `TARGET_INTAKE.json`, update `pre-engagement/state.json`
5. Set root `state.json` → `current_phase: reconnaissance`, `objective_status: none`

## FORBIDDEN

- Removed v6.1 wrappers (target_intake, fable-run, enforcement)
- Duplicate intake when campaign in progress
- Raw JSONL transcript reads
- Starting recon before intake artifacts written (new campaigns only)
