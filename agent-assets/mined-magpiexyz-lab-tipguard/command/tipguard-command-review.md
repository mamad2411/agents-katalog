---
description: "Automated review-fix loop: find issues, fix them, validate, repeat until clean."
type: code-writing
reads:
  - CLAUDE.md
  - experiment/EVENTS.yaml
  - scripts/check-inventory.md
  - experiment/experiment.example.yaml
stack_categories: []
requires_approval: false
references:
  - .claude/patterns/verify.md
  - .claude/patterns/branch.md
  - .claude/patterns/observe.md
branch_prefix: chore
modifies_specs: false
---
Run an automated review of the experiment template, fix findings, and validate
until clean. Replaces the manual workflow of running `scripts/scoped-review-prompt.md`.

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh review`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh review)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 2a

## Loop Dispatch

States 2a through 2f form a review-fix loop. Run **2 to `max_iterations`** iterations.

Initialize before first loop iteration: `seen_findings` = empty, `iteration` = 1, `yield_history` = empty.

- `lifecycle-next.sh` handles loop re-entry automatically via the `loop` field in skill.yaml
- STATE 2f writes `.runs/review-loop-decision.json` with `{"continue": true/false}`
- When continuing, `lifecycle-next.sh` re-dispatches from STATE 2a

Within-iteration early exits:
- STATE 2b produces 0 remaining findings → exit loop to STATE 3
- STATE 2e: no fixes succeeded → exit loop to STATE 3

## Do NOT

- Modify experiment.yaml or experiment/EVENTS.yaml
- Enter plan mode or wait for user approval
- Add new features or pages
- Propose checks that regex-match natural-language prose
- Fix findings that overlap with check-inventory.md
- Run more than `max_iterations` iterations
- Exit before completing iteration 2 (minimum 2 required)
- Skip running validators after each fix
- Commit fixes that cause validator regressions
- Install or remove packages
- Commit to main directly
