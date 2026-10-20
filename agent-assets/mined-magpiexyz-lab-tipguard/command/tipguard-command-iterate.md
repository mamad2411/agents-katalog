---
description: "Use when you have analytics data and want to decide what to do next. Analysis only — no code changes."
type: analysis-only
reads:
  - experiment/experiment.yaml
  - experiment/EVENTS.yaml
  - experiment/ads.yaml
stack_categories: [analytics]
requires_approval: false
references: []
branch_prefix: chore
modifies_specs: false
---
Review the experiment's progress and recommend what to do next.

## Argument Dispatch

Parse `$ARGUMENTS` for mode flags:

| Flag | Mode |
|------|------|
| _(none)_ | default |
| `--check` | check |
| `--cross` | cross |
| `--cross --phase2` | cross-phase2 |

## Lifecycle

1. Initialize based on detected mode:
   - If `--check`: Run `bash .claude/scripts/lifecycle-init.sh iterate '{"mode":"check"}'`
   - If `--cross --phase2`: Run `bash .claude/scripts/lifecycle-init.sh iterate '{"mode":"cross-phase2"}'`
   - If `--cross`: Run `bash .claude/scripts/lifecycle-init.sh iterate '{"mode":"cross"}'`
   - Otherwise: Run `bash .claude/scripts/lifecycle-init.sh iterate`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh iterate)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 2a

## Do NOT
- Write code or modify source files — this skill is analysis only
- Recommend more than 3 actions — focus is more valuable than breadth
- Recommend actions outside the defined commands (bootstrap, change, iterate, retro, distribute, verify)
- Be vague — every recommendation must be specific enough to act on
- Ignore the data — don't recommend features if the funnel shows a landing page problem
- Recommend adding features when the real problem is distribution or positioning
