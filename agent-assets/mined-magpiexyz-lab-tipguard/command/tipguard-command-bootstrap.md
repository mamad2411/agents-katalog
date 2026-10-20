---
description: "Use when starting a new experiment from a filled-in experiment.yaml. Run once per project."
type: code-writing
reads:
  - experiment/experiment.yaml
  - experiment/EVENTS.yaml
  - CLAUDE.md
stack_categories: [framework, database, auth, analytics, ui, payment, email, hosting, testing, ai, telephony, voice, notifications, project-management]
requires_approval: true
references:
  - .claude/patterns/verify.md
  - .claude/patterns/branch.md
  - .claude/patterns/observe.md
  - .claude/patterns/messaging.md
  - .claude/patterns/design.md
  - .claude/procedures/scaffold-setup.md
  - .claude/procedures/scaffold-init.md
  - .claude/procedures/scaffold-libs.md
  - .claude/procedures/scaffold-pages.md
  - .claude/procedures/scaffold-externals.md
  - .claude/procedures/scaffold-landing.md
  - .claude/procedures/wire.md
branch_prefix: feat
modifies_specs: false
---
Bootstrap the MVP from experiment.yaml.

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh bootstrap '{"skill":"bootstrap"}'`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh bootstrap)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT starts with "EMBED_COMPLETE:" → parse the suffix as `<skill>:<state>`, run `bash .claude/scripts/advance-state.sh <skill> <state>`, then return to step 2a
   d. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   e. Read the state file at $NEXT and execute its ACTIONS section
   f. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   g. Return to step 2a

**Note:** STATE 6 (USER_APPROVAL) pauses for user input. The lifecycle loop resumes when the user responds with approval.

## Do NOT
- Modify experiment.yaml or experiment/EVENTS.yaml during implementation
- Skip BG1/BG2 gate checks — they are enforced by hooks
- Add libraries not in experiment.yaml `stack` without user approval
- Commit to main directly
- Skip the user approval step (STATE 6)
