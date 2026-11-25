---
name: execute-batch
description: Work through the approved tasks continuously, staying inside each task's file scope and stop conditions.
---

# execute-batch

Use `references/LOOP_ENGINEERING.md` for the full loop rule.

Before work, list each task coordinate. Continue without low-risk interruptions.
A `stage-complete` checkpoint inside the same authorized goal is a verification
and recovery point, not a user approval boundary. Stop only at the authorized
batch terminal condition, an explicit owner pause, a new authority or scope
requirement, a real unresolved blocker, exhausted budget, impossible V, or G change.

## Rules

- Keep output concise.
- Prefer G/T/S/V/X/P over duplicated fields.
- Do not write business code unless this skill explicitly covers execution.
- Do not hide failed verification.
- Fine-grained tasks are for traceability; they should not fragment the execution loop into unnecessary user stops.
- If an explicit stop rule pauses work at stage-complete, provide a closeout packet with auto-commit action and one next executable step.
