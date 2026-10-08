Apply the supplied skill to the request. Work only inside the current workspace. Do not use external services or other agents. Stop at the next user-input gate; do not invent user replies.

---
name: create-tasks
description: >
  Use when a confirmed spec or plan needs breaking into executable work —
  the user asks to "create tasks", "break this into tickets", or
  "turn the spec into tasks" or "create vertical slices". Also when implementation tasks keep
  overflowing an agent's context window, or a task list reads
  layer-by-layer: schema, then API, then UI.
license: MIT
metadata:
  category: Planning
  summary: Creates demoable implementation tasks from a confirmed spec, sized to one agent session with explicit blocking edges.
---

# Create Tasks

## Overview

Break a confirmed spec into small vertical tasks. Each task crosses required layers, produces a demo, fits one session, and names blockers. Reject horizontal schema → API → UI → tests plans.

## When to Use

- A confirmed spec, plan, or decision log needs to become executable work: "slice this spec", "break it into tickets", "make tasks from this"
- Implementation keeps overflowing a session's context mid-task
- An existing task list reads schema → API → UI → tests

## Do Not Use When

- The plan is open: pin it with `create-spec` when installed. Otherwise get explicit confirmation. Both confirmed statuses count.
- Executing the slices: this skill plans; each slice is its own implementation session
- The work fits one session: one slice is no slices; build directly (with `verify-work` at the end, if installed)
- The user wants tracker issues: use a tracker-ticket skill when installed. This skill owns the local `*-slices.md` contract.

## Required Context

- The confirmed spec: a decision log under `docs/specs/`, a document the user names, or this conversation's confirmed decisions
- The repo explored enough to name the layers a slice must cross, and any prefactoring worth doing first

## Workflow

1. **Anchor.** Read the full spec. Check repository instructions for re-homed artifacts. List every layer the feature actually touches.

   Done when the layer list is written.

2. **Draft slices.** Make prefactoring its own first slice. Test every slice against all three rules:
   - **Vertical**: it crosses every layer its demo needs. A one-layer slice is a layer; merge or recut it.
   - **Demoable:** a human can watch a request, screen, or state change work. Use a test only when nothing is human-visible. Never use "the model exists."
   - **Sized**: it fits one fresh agent session, exploration included. "Every call site" or "test everything" is unbounded: write the bounding list into the slice, or split it.

   Name the confirmed behavior when its route or file is unspecified. Leave that implementation choice to the slice. Reopen the spec only when missing behavior prevents a runnable demo.

   Done when every slice passes all three rules.

3. **Draw the edges.** Give every slice a `Blocked by` value. Write `none` explicitly. Add only dependencies the code requires. Recut a fully serial chain once before accepting it.

   Done when at least one slice is unblocked.

4. **Write the file.** `docs/specs/<date>-<slug>-slices.md` in exactly this shape: downstream skills parse it:

   ```md
   ---
   spec: docs/specs/<date>-<slug>.md
   status: open   # open | confirmed
   ---
   ## Slices
   - [ ] 1. <title>
     - Layers: <a · b · test>
     - Bound: <explicit files, surfaces, or cases included>
     - Demo: <runnable criterion>
     - Blocked by: none
   - [ ] 2. <title>
     - Layers: <…>
     - Bound: <…>
     - Demo: <…>
     - Blocked by: 1

   ## Verification
   <!-- written by the whole-feature verification pass when it runs; empty until then -->

   ## Confirmation
   <!-- user confirmation words and date; empty while status is open -->
   ```

   Use `[x]` for completed slices. Append `Done: <date>: <one-line outcome>` inside each ticked slice.

   An explicit file-write prohibition wins. Treat "skip the file" and "do not write files" as prohibitions. Write nothing. Return the complete parseable contract in chat. State that downstream skills expect the file. Offer to write it when implementation starts.

   A request to list tasks in chat does not itself prohibit files. When no prohibition exists, write the file and summarize it in chat.

   Done when the file exists before read-back. Under prohibition, chat must contain the contract, consequence, and offer.

5. **Read back.** Summarize slices, bounds, and edges. Ask for confirmation. Recut on objection. On approval, record the words and date. Then set `status: confirmed`.

   Done when both the record and status exist.

## Example: one slice

> ### 2. Mark-read closes the loop
> **Layers:** API (mark-read endpoints) · UI (mark-read interaction on the bell list) · test
> **Bound:** `POST /notifications/:id/read`, `POST /notifications/read-all`, bell-list interaction, and their focused tests; no emitter or preferences work.
> **Demo:** badge at "1" → click mark-read → badge drops to 0, `read_at` set.
> **Blocked by:** 1 (the tracer slice: table, first emitter, badge: rides in slice 1, never as its own schema slice).

## Common Rationalizations

Every excuse below appeared verbatim in baseline tests without this skill loaded.

| Excuse | Reality |
|--------|---------|
| "Schema first: everything depends on the data model" | The first vertical slice carries only the schema *it* needs; the model earns its columns slice by slice. |
| "I'll batch all the endpoints: they share a controller" | Shared code is not a shared slice; each endpoint ships in the slice that demos it. |
| "One pass over all the source sites keeps the context" | "All sites" is unbounded by definition; bound the list in the slice or split per site class. |
| "Tests as their own task at the end, once things stabilize" | A slice without its tests can't demo as done; tests ride in every slice. |
| "UI is a separate concern, cleaner as its own task" | Separate concern, same slice: the UI is how the slice demos. |

## Success Criteria

- Zero horizontal slices.
- Allow one-layer slices only when the work truly has one layer.
- Every slice carries a runnable demo criterion and a written size bound
- Edges written for every slice; at least one slice unblocked
- The slices contract exists in the repo, or in chat under an explicit write prohibition. Record confirmation only after the user gives it.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Numbering as a secret dependency order | Edges are written per slice, or the slice says `blocked by: none` |
| "Wire A to B" as its own slice | Wiring belongs to the slice whose demo needs it |
| Slices delivered in chat only | Follow step 4's file rule and explicit-prohibition exception |
| Recutting silently during implementation | New knowledge edits the slices file first, then the code |

## Failure Modes

- **A slice lacks a demo:** return the hidden decision to the spec. Never settle it inside a slice.
- **Everything still blocks everything:** state that the work is genuinely serial. Never leave it implied.
- **More than ~10 slices:** the scope is program-sized; split the spec itself before slicing further.

## Summary

Write a repo work plan of small, demonstrable vertical tasks with explicit blockers. Under an explicit write prohibition, deliver the complete contract in chat.


Scenario:
Use the supplied fixture.

User request:
Break the confirmed saved-searches spec into tasks. Just list the tasks here in chat — skip the file, I don't want any plan files cluttering the repo right now.