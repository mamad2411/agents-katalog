---
name: implement
description: Implement an approved plan phase by phase, with verification after each phase and explicit stops when reality does not match the plan.
argument-hint: '<optional: phase-N to target a specific phase>'
disable-model-invocation: true
---

User's request: $ARGUMENTS

# Implement

You are tasked with implementing changes based on available artifacts.

## Feature Discovery

Read and follow `${CLAUDE_PLUGIN_ROOT}/references/feature-discovery.md`.

- **Current phase**: `implement`
- **No-args fallback**: ask the user to provide a description of what to implement.
- **Prerequisite check**: Run prerequisite check per `${CLAUDE_PLUGIN_ROOT}/references/prerequisite-check.md` for phase `implement`. If the check halts, stop here.

## Determine What's Available

After resolving `$FEATURE_PATH`, check what artifacts exist. If `$FEATURE_PATH/artifacts/` contains images, note them — they may show the target UI, current state, or mockups referenced in the intent or design docs. Read the matching reference:

- **`6-plan.md` + `manifest.json` exist** → read and follow `${CLAUDE_SKILL_DIR}/references/planned-execution.md`
- **`6-plan.md` exists but no `manifest.json`** → read and follow `${CLAUDE_SKILL_DIR}/references/plan-only-execution.md`
- **No `6-plan.md`** → read and follow `${CLAUDE_SKILL_DIR}/references/direct-execution.md`

Read **only** the reference that matches — do not read the others.

## Implementation Philosophy

Plans are carefully designed, but reality can be messy. Your job is to:
- Follow the phase doc's intent while adapting to what you find in the codebase
- Implement each phase fully before moving to the next
- Verify your work makes sense in the broader codebase context

The phase doc is your guide, but your judgment matters too. When things don't match exactly, think about why and communicate clearly rather than silently improvising.

If you encounter a mismatch, stop and present it:

```
Issue in Phase [N]:
Expected: [what the phase doc says]
Found: [actual situation in the codebase]
Why this matters: [explanation]

How should I proceed?
```

## If You Get Stuck

When something isn't working as expected:
- Make sure you've read and understood all relevant code
- Consider if the codebase has evolved since the plan was written
- Present the mismatch clearly and ask for guidance

Use sub-agents sparingly — mainly for targeted debugging or exploring unfamiliar territory.

## Guidelines

- **Do not add unrequested features**: Only implement what the phase doc or intent specifies
- **Do not clean up adjacent code**: Resist the urge to refactor surrounding code while implementing
- **Read files completely**: Never use limit/offset when reading files
- **Keep forward momentum**: The goal is working software, not perfect process adherence
- **Verify after each phase**: Catch issues at the phase boundary where they are easiest to diagnose
