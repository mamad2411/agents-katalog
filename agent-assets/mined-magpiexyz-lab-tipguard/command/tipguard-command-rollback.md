---
description: "Roll back to the previous production deployment. Emergency use — no branch or PR."
type: analysis-only
requires_approval: true
branch_prefix: ""
reads:
  - .runs/deploy-manifest.json
  - experiment/experiment.yaml
stack_categories:
  - hosting
references:
  - .claude/patterns/incident-response.md
modifies_specs: false
---
Roll back to the previous production deployment when something goes wrong after deploy.

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh rollback`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh rollback)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 2a

## Do NOT
- Modify any source code files
- Change experiment.yaml or any spec file
- Create a branch or PR — rollback operates directly on production
- Proceed without a valid deploy manifest (`.runs/deploy-manifest.json`)
- Rollback without explicit user confirmation of the target deployment
- Delete source code, database data, or git history
- Force-push or rewrite git history
