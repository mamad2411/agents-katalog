---
name: fable-5-intake
description: >-
  Fable6 Step 0 MD-first intake (v6.1). Resume if state.json exists; NOT target_intake.py.
version: 6.1.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent]
---

# Fable6 Intake — Step 0

> Same canon as `fable-6-intake`. Read `Workflow/pre-engagement/PLAYBOOK.md`.

## Resume rule (mandatory)

**If `campaigns/{target}/state.json` exists:** read state + artifacts; do NOT rewrite intake; continue from `current_phase`.

## New campaign

1. Establish scope + dead vectors
2. Optionally: `bin/fable-util digest {target} --campaign campaigns/{target}`
3. Write `TARGET_INTAKE.json`, `pre-engagement/state.json`
4. Set `current_phase: reconnaissance`, `objective_status: none`

## FORBIDDEN

- Removed v6.1: `target_intake.py`, `fable-run.py`, enforcement stack
- Duplicate intake on existing campaign
- Raw JSONL reads
- Auto recon_pipeline before intake complete
