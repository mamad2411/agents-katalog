---
description: "Unified verification: build, agent review, E2E tests. Run after /bootstrap or /change. Also works standalone as a quality gate."
type: code-writing
reads:
  - experiment/experiment.yaml
  - experiment/EVENTS.yaml
stack_categories: [testing, framework, analytics]
requires_approval: false
references:
  - .claude/patterns/verify.md
  - .claude/patterns/branch.md
  - .claude/patterns/observe.md
branch_prefix: fix
modifies_specs: false
---
Unified verification: build, agent review, E2E tests, and (in bootstrap-verify mode) PR creation.

## Mode Detection

Before entering the lifecycle, detect the operating mode by checking `.runs/current-plan.md`:

- If it exists with frontmatter `skill: bootstrap` and `checkpoint: awaiting-verify` → **bootstrap-verify** mode
- If it does not exist → **standalone** mode
- Otherwise → **change-verify** or **distribute-verify** mode (read `skill` from frontmatter)

State the detected mode: "Running in **[mode]** mode."

Shared algorithms (Exhaustion Protocol, Agent Efficiency Directives, Build & Lint Loop) are in `.claude/patterns/verify.md`.

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh verify '{"scope":"<scope>","skill":"verify"}'`
   (scope from $ARGUMENTS or default "full"; when embedded, parent passes scope)
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh verify)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 2a

## Do NOT
- Modify experiment.yaml or experiment/EVENTS.yaml
- Add new features — only fix what tests and agents expose
- Run tests against production (always use local dev server)
- Skip the build verification step
- Skip agent review steps required by the scope
- Commit to main directly
- Create a PR in change-verify mode (that's /change's job)
