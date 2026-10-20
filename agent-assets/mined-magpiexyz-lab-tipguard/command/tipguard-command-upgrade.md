---
description: "Handle template sync: overwrite template-owned files, validate structural consistency, reconcile stale memory, and open a PR."
type: code-writing
reads:
  - CLAUDE.md
stack_categories: []
requires_approval: false
references:
  - .claude/patterns/verify.md
  - .claude/patterns/branch.md
  - .claude/patterns/skill-epilogue.md
  - .claude/patterns/observe.md
branch_prefix: chore
modifies_specs: false
---
Upgrade the project to the latest template version. $ARGUMENTS

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh upgrade`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh upgrade)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 2a

## Do NOT
- Auto-delete any files without explicit user confirmation
- Skip diagnostic steps (States 1-2) — the structural diff report is always valuable
- Modify project-owned files under `.claude/` that are outside the template-owned directory allowlist
- Use the standard PR template — upgrade PRs use a dedicated report format
