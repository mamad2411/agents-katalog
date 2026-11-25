---
name: meta-control
description: Optimize the agent's (Pi) own use of the control extension and subagents.
---
# Meta Control

Use this atom to improve your own performance as an agent driving this extension.

## Step 0 — run the sidecar

Before anything else, run the skill's sidecar so you know what's actually wired up:

```bash
packages/skills/meta-control/scripts/check.sh           # from repository root; doctor only
packages/skills/meta-control/scripts/check.sh --new-run # from repository root; allocate a unique evidence run
```

The script exits non-zero if the skill's SKILL.md, frontmatter, or referenced assets are missing. Read its JSON output — `missing[]` tells you exactly what to fix before you trust this skill's guidance. `validator_tail` is the tail of the package validator; `[FAIL]` lines there are also your problem.

Never reason about "this skill is fine" until `check.sh` returns `ok: true`.

## Self-Optimization Rules

1. **Doctor First**: At the start of a session, or after any tool failure, run `packages/skills/meta-control/scripts/check.sh` from the repository root (or `control_doctor` from the agent). Don't wait for errors to discover missing deps — `check.sh` exits non-zero on missing assets.
2. **RUN_ID discipline**: Always create a run dir with `packages/skills/meta-control/scripts/check.sh --new-run` for any multi-step task. Never overwrite previous evidence.
3. **Verification Loop**: If `control_verify_commitments` fails, do not proceed to the next step. Loop back to capture/compose until the proof is solid.

## Strategy for Complex Goals

For high-level requests ("Make a showcase video of X"), always break it down into:
1. `./scripts/check.sh --new-run` → get a RUN_DIR.
2. `control_route` → identify skills.
3. `background-pty` → execute steps.
4. `control_verify_commitments` → check proof.
5. `compose` → build video.

When the parent calls `/meta-control`, the extension has already run `check.sh` for you and surfaced the result.
