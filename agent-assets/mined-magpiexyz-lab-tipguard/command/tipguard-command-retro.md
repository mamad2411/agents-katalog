---
description: "Use at the end of an experiment or when the measurement window ends. Files structured feedback as a GitHub Issue."
type: analysis-only
reads:
  - experiment/experiment.yaml
  - experiment/EVENTS.yaml
stack_categories: []
requires_approval: false
references: []
branch_prefix: chore
modifies_specs: false
---
Run a structured retrospective for the current experiment and file it as a GitHub Issue.

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh retro`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh retro)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 2a

## Do NOT
- Modify any code files
- Create branches or PRs
- Change experiment.yaml, experiment/EVENTS.yaml, or any spec file
- Install or remove packages
