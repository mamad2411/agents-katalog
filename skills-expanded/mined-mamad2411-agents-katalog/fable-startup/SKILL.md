---
name: fable-startup
description: >-
  Fable session init — load canon v6, SOUL, COMMUNICATION_STYLE. Short banner only.
version: 8.0.0
allowed-tools: [Read]
---

# Fable Startup

**Root:** `FABLE_ROOT=<repo-install-path>` — set this env var to the absolute
path of your Fable5 checkout (e.g. `export FABLE_ROOT=/opt/Fable5`).
On clone-from-fresh: `FABLE5_ROOT` is also honored for back-compat. If neither
is set, Fable utilities auto-detect by walking up from their file location.
See `docs/PATH_HANDLING.md`.

On session start, load:

1. `CLAUDE.md`
2. `fable/SOUL.md`
3. `docs/WORKFLOW_CANON.md`
4. `fable/COMMUNICATION_STYLE.md`

Operator target = authorized scope. MD-first: think before scripts.

**Banner (3 lines max — no tables, no box art):**

```
Fable MD-first — playbooks guide, utilities optional
Use bin/fable-util from FABLE_ROOT for recon/check/digest
Ready for target.
```


## Fable mode

- **Strike** (domain in prompt): Fable doctrine only — Ponytail OFF
- **Framework** (edit tools/fable/bin): see `fable/IMPLEMENTATION_POLICY.md`
- Root: `$FABLE_ROOT` (or auto-detected; never hard-code a user path)
