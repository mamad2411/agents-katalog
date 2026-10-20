---
description: "Deploy or update the app. Run after /bootstrap PR is merged; re-run to update."
type: analysis-only
reads:
  - experiment/experiment.yaml
  - .env.example
  - CLAUDE.md
  - experiment/EVENTS.yaml
stack_categories: [hosting, database, auth, analytics, payment, email, ai, telephony, voice, notifications, project-management]
requires_approval: true
references:
  - .claude/patterns/observe.md
branch_prefix: ""
modifies_specs: false
---
Deploy the app to production by creating cloud infrastructure and deploying via CLI.

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh deploy`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh deploy)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 2a

## Do NOT

- Create a git branch or PR — this is infrastructure-only
- Modify any source code files
- Store secrets in code or commit them
- Skip the approval step — the user must review the plan before resources are created
- Proceed if CLI auth checks fail — always stop and tell the user which login command to run
