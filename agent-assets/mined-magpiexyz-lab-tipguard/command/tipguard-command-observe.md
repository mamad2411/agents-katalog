---
description: "File a template observation manually. Use when you spot a template issue outside of automated observation."
type: analysis-only
reads: []
stack_categories: []
requires_approval: false
references:
  - .claude/patterns/observe.md
branch_prefix: ""
modifies_specs: false
---
Evaluate a template file and file an observation issue if it qualifies. $ARGUMENTS

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh observe`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh observe)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 2a

## Do NOT
- Modify any code files -- this skill is analysis only
- Create branches or PRs
- Change experiment.yaml or any spec file
- Install or remove packages
