---
name: webgpt-todo-response
description: Use after receiving WebGPT or another LLM review on a Formax todo and before sending the todo back for another pass. Produce a concise handoff response that says what we adopted, what we reject or question, and what the reviewer should specifically re-evaluate in `docs/todolist.md`.
---

# WebGPT Todo Response

## Purpose

Generate the message to send back to WebGPT after we have read its previous
analysis and drafted or updated `docs/todolist.md`.

Use this skill when the user asks:

- whether we have rebuttals or questions for WebGPT
- what to include when sending our todo back to WebGPT for another pass
- to prepare a response asking WebGPT to evaluate, improve, or challenge our todo
- to compare WebGPT's recommendations against our chosen implementation scope

## Inputs To Inspect

Read only the files needed for the current handoff:

- WebGPT response, usually under `repomix-output/`
- current todo, usually `docs/todolist.md`
- relevant canonical docs under `docs/contracts/*`, `docs/frontend/*`, or other explicitly governing docs when the todo depends on them
- optional other LLM replies if the user asks for a multi-model synthesis

Do not re-run broad repository analysis unless the todo or WebGPT response
depends on code facts that are unclear.

## Workflow

1. Identify WebGPT's strongest recommendations.
   - Mark which ones are adopted in the todo.
   - Mark which ones are intentionally deferred.
   - Mark which ones are rejected or still need clarification.

2. Check the todo against Formax boundaries.
   - Canonical semantics belong in `docs/contracts/*` and canonical runtime layers, not only UI.
   - Web reference UI should reflect runtime/platform truth, not invent it.
   - Do not move thread/runtime state ownership into ad hoc component-local logic when the task is structurally runtime-driven.
   - Preserve parity-sensitive behavior when relevant: transcript surface semantics, URL/thread sync, prompt/tool exposure boundaries, permissions flow, and active-thread canonical gating.
   - Avoid turning a focused task into a broad cleanup or cross-subsystem redesign unless explicitly requested.

3. Find weak spots in the todo.
   - Missing canonical-doc step
   - Missing data/type/interface step before UI
   - Runtime state ownership drift
   - Welcome/draft/thread semantics being mixed together
   - Scope creep into unrelated app-server, terminal, diff, approval, or desktop integration work
   - Missing tests or review gates
   - Missing statement of protocol constraints or non-atomic failure boundaries

4. Write a concise message for WebGPT.
   - Assume WebGPT has no hidden context beyond the attached todo and bundle.
   - Be explicit about decisions already made.
   - Ask targeted questions instead of open-ended “any thoughts?”
   - Request concrete todo edits or challenges, not generic feedback.

## Output Shape

Produce a copy-ready Markdown response with these sections:

```md
# Response To WebGPT

## What We Adopted
- ...

## Where We Differ / Pushback
- ...

## My Current Leaning
1. ...

## Highest-Value Review Points
1. ...

## Specific Questions For You
1. ...

## Please Review The Todo For
- ...

## Constraints To Preserve
- ...
```

Keep it short enough to paste into WebGPT with the todo. Prefer 5-10 specific
questions/checks over a long essay.

Use `My Current Leaning` to distinguish default decisions from genuinely open
questions. WebGPT may challenge these, but should not treat them as blank slate.

Use `Highest-Value Review Points` to focus WebGPT on the few risks most likely
to improve the todo. These should be sharper than the broader checklist.

## Good Question Patterns

- “Does this todo still hide new semantics inside `!activeThreadId`, or is the draft state truly first-class?”
- “Are we separating `selectedCwd` from `draftCwd` cleanly enough to avoid left-rail/runtime state drift?”
- “Is the proposed first-send flow realistic given `thread/start` and `turn/start` are non-atomic?”
- “Are we over-expanding the task into unrelated desktop/add-project behavior instead of keeping the mainline on new-thread draft semantics?”
- “Do the loops lock runtime ownership first, then UI, then tests, or is there still UI-first drift?”

## Avoid

- Do not ask WebGPT to implement patches unless the user explicitly wants that.
- Do not ask WebGPT to run commands.
- Do not include local absolute paths.
- Do not send vague requests like “please improve this.”
- Do not restate the whole todo; reference it and ask for specific audit points.
