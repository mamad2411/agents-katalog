---
name: workflow-and-sop-builder
description: Turn a repeated business task into a human-run, AI-assisted, automated, or combined workflow with an SOP, roles, steps, decisions, exceptions, controls, and tests.
---

# Workflow And SOP Builder

Turn how work actually gets done into a usable process people and tools can follow.

## Job contract

- Owns: repeated business processes and operational playbooks.
- Does not own: AI instruction files (`agents-md-setup`).
- Finished deliverable: selected-mode workflow, SOP, exception handling, and test run.

## Choose a mode

- `Human-run`: people follow the SOP manually.
- `AI-assisted`: AI prepares or checks defined steps while a person decides.
- `Automated`: systems move information under explicit rules and controls.
- `Combined`: assigns each step to the cheapest safe owner.

## Workflow

1. Capture the trigger, desired result, frequency, inputs, owner, current steps, systems, exceptions, and failure cost.
2. Observe the real path. Do not document an imaginary ideal process as current reality.
3. Remove duplicate work before automating anything.
4. Assign each step to a person, AI, or system and explain why.
5. Define decision rules, approval gates, data handling, failure paths, and recovery.
6. Write the SOP so a new operator can run it without oral context.
7. Dry-run one normal case and one exception; revise where instructions fail.

## Output

```markdown
# Workflow And SOP

## Purpose And Success
[Trigger, outcome, measure]

## Roles And Systems
[Who or what owns each part]

## Procedure
| Step | Owner | Input | Action | Output | Check |

## Decision Rules
[If/then rules]

## Approvals And Safety
[External actions, sensitive data, spend, irreversible steps]

## Exceptions And Recovery
[What can fail and what to do]

## Run Checklist
[Compact repeat-use version]

## Test Record
[Normal and exception cases]
```

## Guardrails

- Never automate sending, publishing, spending, deletion, or account changes without an explicit approval gate.
- Keep sensitive data out of prompts and logs unless required and authorised.
- Prefer a reliable manual step to a brittle automation.
