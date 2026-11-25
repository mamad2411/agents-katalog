---
name: goal-loop-auditor
description: Audit goal, autonomous loop, research loop, execution loop, review loop, monitoring loop, or long-running agent prompts. Use when the user asks to review, harden, score, debug, or improve a goal/loop prompt for missing facts, ambiguous scope, weak validation, source-quality gaps, output-contract gaps, conflict-handling problems, stop-condition problems, permissions, or hidden assumptions.
---

# Goal Loop Auditor

Evaluate whether a goal/loop prompt is safe to launch. Prioritize defects that would cause wrong work, unverifiable results, scope drift, unsafe action, or guessing.

## Workflow

1. Identify loop type: `research`, `execution`, `review`, `monitoring`, or `mixed`.
2. Check launch fields: `PROJECT`, `GOAL`, `MODE`, `CONTEXT`, `SCOPE`, `RULES`, `SOURCES`, `METHOD`, `OUTPUT`, `ON CONFLICT`, `STOP CONDITION`, `DONE CRITERIA`.
3. For execution loops, also check `PERMISSIONS` for writes, dependencies, migrations, commits, pushes, network, secrets, production, and destructive actions.
4. Report only material findings. Group related missing fields instead of listing every absent label separately.
5. Produce a corrected prompt only when assumptions are explicit and non-blocking.

## Severity

- `Blocking`: should not launch until fixed.
- `High`: likely wrong, unsafe, or unverifiable.
- `Medium`: likely inefficient or inconsistent.
- `Low`: polish only.

Missing `GOAL`, `SCOPE`, `RULES`, `OUTPUT`, or `STOP CONDITION` is `Blocking`.

## Audit Standard

Check that the prompt has a concrete deliverable, explicit exclusions, observable validation, source rules, output schema, conflict handling, halt cases, no hidden conversation dependency, and checkpoints or budget for long-running work. Fold conflict, checkpoint, and budget gaps into grouped findings unless they are the primary launch risk.

If blocking facts prevent a safe corrected prompt, ask exactly one next blocking question with `Recommended answer:` instead of listing every missing fact.

## Output

Return this shape:

````text
Audit result: [Ready | Needs revision | Do not launch]

Findings:
- [Severity] [Field/group]: [problem]
  Impact: [why it matters]
  Fix: [specific change]

Next blocking question:
[Ask exactly one question when a safe correction needs user input.]
Recommended answer: [default that preserves momentum without inventing concrete facts.]

Assumptions:
- [non-blocking assumptions only]

Corrected prompt:
```text
[include only when safe]
```
````

Keep findings to the smallest set that changes launch safety. If there are no material issues, return `Audit result: Ready` and residual risks only.
