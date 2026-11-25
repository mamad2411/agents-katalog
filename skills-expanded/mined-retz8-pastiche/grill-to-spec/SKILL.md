---
name: grill-to-spec
description: Convert a completed grill-me session into a spec file. Captures only the task and the decisions locked during grilling — no implementation details, no invented decisions. Use when the user asks to write a spec from a grill, save grill decisions, or after a grill-me session concludes.
---

# Grill to Spec

Convert a just-completed `grill-me` session into a spec file under `_dev/docs/spec/`.

## File naming

Number first. Filename comes from the TODO number when available, otherwise name only. Do not ask the user about the path — derive it and proceed.

- Task (`**N.M**` in TODO): `_dev/docs/spec/task-<N.M>-<short-name>.md`
- Phase: `_dev/docs/spec/phase-<N>-<short-name>.md`
- No task number available: `_dev/docs/spec/<short-name>.md`

## Hard rules

- **Spec, not plan.** Capture *what was decided*, not how to implement it. No task breakdown, no step-by-step, no file-by-file instructions.
- **Only what was locked in the grill.** If a decision did not come up explicitly in the grilling conversation, do not include it. Do not infer, do not extend, do not add "for completeness."
- **No invented decisions.** If the user did not state a preference on something, it is not in the spec. Surface it as an open item only if the user flagged it as open during grilling.
- **No implementation details.** No code, no command lines, no file syntax, no per-step procedure. The spec is a high-level overview of the locked task scope and decisions.

## Required structure

```md
# <Task title>

<One- or two-sentence statement of what this spec covers. Reference the parent TODO item, phase, or OSS_SPEC section.>

## Scope

<Bulleted or short-prose statement of what is in scope for this task. Drawn from the grill, not invented.>

## Locked decisions

### 1. <Decision title>

<One short paragraph stating the decision as locked in the grill.>

### 2. <Decision title>

<...>

## Invariants

<Optional. Constraints the grill surfaced that apply throughout the task. Skip if none were raised.>

## Open items

<Optional. Only items the user explicitly flagged as deferred or unresolved during the grill. Skip if none.>
```

## Process

1. Re-read the grilling conversation in context. Identify every decision the user explicitly accepted, rejected, or modified.
2. Derive the target path per the File naming rules above. Do not ask, do not confirm.
3. Write the spec directly to that path using the required structure. Do not display the draft to the user beforehand — just write it.
4. Report the written path in one line. The user will redirect if revisions are needed.

## What this skill never does

- Decompose the task into sub-tasks or a plan.
- Specify file contents, command flags, or code shapes.
- Add "recommended next steps."
- Re-open decisions the grill closed.
- Add decisions the grill did not cover.
