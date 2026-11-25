---
name: enterprise-next
description: Use when an enterprise lane needs a read-only next-action recommendation from the current repo profile, traps, and agent session state
---

# Enterprise Next

Read-only controller for deciding what enterprise stage should happen next.

## Required Behavior

1. Run the deterministic controller:

```bash
node scripts/enterprise-next.cjs --repo-root "$PWD" --json
```

2. If more than one session exists, rerun with the chosen session:

```bash
node scripts/enterprise-next.cjs --repo-root "$PWD" --agent-id <agent-id> --json
```

3. Report the verdict, recommended skill, blockers, and missing artifacts.
4. Do not invoke the recommended skill automatically unless the user explicitly asks you to continue.

## Verdicts

- `DISCOVER_REQUIRED`: repo profile, traps, or lane state is missing; use `enterprise-discover`.
- `NEEDS_TRIAGE`: the controller cannot choose a lane safely; ask for or pass `--agent-id`.
- `NEXT_STAGE`: continue with the recommended upstream stage.
- `BLOCKED`: repair the named artifact or gate evidence before advancing.
- `READY_TO_VERIFY`: run `enterprise-verify` against current code and evidence.
- `READY_TO_SHIP`: run `enterprise-harness` unless the harness is already recorded.

## Rules

- This skill is read-only. Do not create sessions, write artifacts, stage files, run gates, commit, or edit source code while answering "what next".
- Warm repo state wins over chat memory. Read `.codex/enterprise-state/repo-profile.json`, `.codex/enterprise-state/repo-traps.json`, and `.codex/enterprise-state/agent-sessions/`.
- If the controller says `BLOCKED`, do not skip ahead because a later stage feels more productive.
- If the user wants to proceed after the recommendation, use the recommended enterprise skill in a separate step.
