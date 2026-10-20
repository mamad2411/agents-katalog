---
description: "Tear down cloud infrastructure created by /deploy. Use when ending an experiment."
type: analysis-only
reads:
  - experiment/experiment.yaml
  - .runs/deploy-manifest.json
  - CLAUDE.md
stack_categories: [hosting, database, analytics, payment]
requires_approval: true
references: []
branch_prefix: ""
modifies_specs: false
---
Tear down the cloud infrastructure created by `/deploy`.

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh teardown`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh teardown)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 2a

## Do NOT

- Delete source code, experiment.yaml, or git history
- Delete without user confirmation (name + data check)
- Block on partial failures — report and continue
- Delete .env.example (that's a template, not credentials)
