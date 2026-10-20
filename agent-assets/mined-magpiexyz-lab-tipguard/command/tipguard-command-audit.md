---
description: "Analyze template structural quality: duplication, complexity, abstractability, skill architecture. Analysis only — no code changes."
type: analysis-only
reads:
  - CLAUDE.md
  - scripts/check-inventory.md
stack_categories: []
requires_approval: false
references: []
branch_prefix: ""
modifies_specs: false
---
Audit the template's structural quality. $ARGUMENTS

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh audit`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh audit)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 2a

## Do NOT
- Modify any source files — this skill is analysis only
- Create branches or PRs
- Propose fixes for correctness issues — that is `/review`'s job
- Flag intentional JIT repetition as duplication
- Report "long but simple" files as complexity hotspots
- Report the same finding under both Dimension A and Dimension C
- Report D2 findings for cross-skill patterns — that is Dimension C's scope
- Report D1 findings for file-level complexity — that is Dimension B's scope
