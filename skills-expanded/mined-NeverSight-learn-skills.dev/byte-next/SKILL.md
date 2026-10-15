---
name: byte-next
description: Continue a Your ByteDance / Byte OS project by inferring and executing the next workflow step from `.byte-os/` state. Use when the user says next, continue, resume, proceed, or asks what to do after the current stage.
---

# Byte Next

Next advances the project one step. It is the step-by-step mode companion to `byte-auto`.

## Workflow

1. Inspect `.byte-os/`.
2. Read `STATUS.md`.
3. Determine the next workflow.
4. Check `OKRS.md` so the next step advances visible goals.
5. Execute the workflow, not merely describe it, unless execution would be risky or requires missing input.
6. If the workflow writes, reviews, refactors, or iterates on code, apply `byte-code-rules`.
7. Update `STATUS.md`.

## Decision Table

| State | Next workflow |
|---|---|
| No `.byte-os/` | `byte-start` |
| Project exists, no `PRODUCT_SPEC.md` | `byte-shape` |
| Specs exist, no plan files | `byte-plan` |
| Plans exist and incomplete | `byte-build` |
| Plans complete, no review | `byte-review` |
| Latest review verdict is `block` or `iterate` | `byte-iterate` |
| Latest review verdict is `ship` and no delivery | `byte-deliver` |
| Delivery exists and new real feedback is provided | `byte-users` |
| Delivery exists and no new input | `byte-status` |

If several are plausible, choose the one that moves the product toward delivery.

## Safety

Ask one concise question if:

- The product idea is missing and no project exists.
- The next step would require destructive changes.
- Real user feedback is required but absent.
- The user asks for auto mode but iteration count or delivery target is unclear and the default would be risky.

Otherwise make reasonable assumptions and record them in `DECISIONS.md`.

## Output

Always report:

```text
Previous stage:
Selected next workflow:
Reason:
Artifacts updated:
Next command:
```

## Completion Criteria

The project has advanced exactly one major Byte OS step.
