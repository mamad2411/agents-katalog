---
name: fable-5-startup
description: >-
  Fable6 MD-first session startup (v6.1). Loads WORKFLOW_CANON_v6 + SOUL + COMMUNICATION_STYLE.
  On target: follow fable-6-intake PLAYBOOK — target_intake.py removed in v6.1.
version: 6.1.0
allowed-tools: [Read, Bash]
---

# Fable6 Startup (loaded as fable-5-startup for /fable compatibility)

**Root:** `FABLE5_ROOT=/home/Haza/Fable5` on Haza VPS.

## When operator gives a target

**Do NOT run target_intake.py** — removed in v6.1.

1. Read `docs/WORKFLOW_CANON_v6.md` + `docs/AGENT_SPINE.md` + `fable/COMMUNICATION_STYLE.md`
2. If `campaigns/{target}/state.json` exists → resume (read state, skip duplicate intake)
3. Else follow `Workflow/pre-engagement/PLAYBOOK.md`
4. Optionally: `bin/fable-util digest {domain} --campaign campaigns/{domain}`
5. Invoke skill `fable-6-intake` or `fable-6-router`

## When no target (startup only)

Load: `CLAUDE.md`, `fable/SOUL.md`, `docs/WORKFLOW_CANON_v6.md`, `fable/COMMUNICATION_STYLE.md`

**Banner (3 lines max — no tables, no box art):**

```
Fable6 MD-first — playbooks guide, utilities optional
Use bin/fable-util from FABLE5_ROOT for recon/check/digest
Ready for target.
```

## Key v6 paths

- `Workflow/{phase}/PLAYBOOK.md` — phase authority
- `bin/fable-util recon|check|digest|archaeology` — path-safe utilities
- `fable-6-router` — phase dispatch skill
