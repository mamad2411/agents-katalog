---
description: "Transform an idea into a complete Level 3 experiment.yaml with hypotheses, behaviors, variants, and stack."
type: code-writing
reads: []
writes: [experiment/EVENTS.yaml]
stack_categories: []
requires_approval: true
references:
  - .claude/patterns/verify.md
  - .claude/patterns/branch.md
  - .claude/patterns/observe.md
  - .claude/patterns/spec-reasoning.md
branch_prefix: feat
modifies_specs: true
---
Transform an idea into a complete experiment specification: $ARGUMENTS

## Lifecycle

1. Run `bash .claude/scripts/lifecycle-init.sh spec`
2. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh spec)`
   b. If NEXT is "FINALIZE" → skill complete
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 2a

## Do NOT
- Add behaviors not traceable to a hypothesis
- Add stack components not required by Level 3
- Generate fewer than 3 variants or fewer than 5 pending hypotheses
- Produce hypotheses without a `metric` object containing `formula`, numeric `threshold`, and `operator`
- Modify any file other than `experiment/experiment.yaml`, `experiment/EVENTS.yaml`, `.runs/spec-manifest.json`, and `.runs/verify-history.jsonl`
- Skip the user approval checkpoint in Step 6
- Proceed past any STOP point without explicit user confirmation
- Skip auth or database — Level 3 always includes them
- Skip payment stack when monetize hypotheses are present
