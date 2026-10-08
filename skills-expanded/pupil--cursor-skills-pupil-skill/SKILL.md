---
name: pupil
description: Operate Windows GUIs through Pupil by looping `perceive` and `indicate` until the user goal is met or explicitly canceled. Prefer `click` on visible controls over equivalent keyboard shortcuts, and use `input` for real typing/paste or true shortcut-only actions. Use this skill whenever Pupil tools are available and the task involves multi-step desktop automation or guided user interactions. Treat `r.perceive` as the default next snapshot and keep chat minimal while the loop runs.
---

# Using Pupil

This skill is a **workflow guide** for the model. Use MCP tool descriptions for
exact payload contracts and validation details.

## Mental model

- If this skill is explicitly invoked as `/pupil <task>`, treat that as a hard
  execution mode: use Pupil tooling to complete that task end-to-end, even if a
  non-Pupil path could also work.
- Pupil has two tools: `perceive()` for reading UI and `indicate(...)` for showing
  an overlay card and optionally executing one action.
- Real GUI automation is a **loop**, not one call.
- Default next-frame source is `r.perceive` returned by the last `indicate`.
- Call standalone `perceive()` at task start, when `r.perceive` is missing/stale,
  or when you need full (untruncated) names.
- Prefer `click` over `input` and shortcuts when a visible control can do the
  same action.

## The loop

Repeat until goal reached or hard stop:

```
1) If no fresh snapshot, call perceive()
2) Pick next target from latest snapshot
3) Call indicate(...) with the right type
4) Parse r = { result, perceive }
5) Use r.perceive as next snapshot and continue
```

Never reuse stale `coords` after the UI changes.

## Chat output during Pupil loops

- Do not narrate play-by-play between tool calls.
- Put user-facing step guidance on the overlay card (`desc`) when needed.
- Keep chat to: optional one-line preface, real endings/blockers, brief final summary.
- Minify JSON payloads in tool calls to reduce token usage.

## Persistence: blocks are cards, not dead ends

- If blocked, keep moving with a meaningful card (`wait`, `action`, `warning`)
  instead of stopping in chat.
- If one card is skipped, do not end the task by default. Reconcile on
  `r.perceive`, infer why, and propose the next card.
- Stop only for true endings: goal met, explicit full cancellation, or repeated
  no-progress after recovery attempts.

## Picking the next card type fast

- Visible control can do action -> `click`.
- Need typing/paste or true shortcut-only behavior -> `input` (still pass `coords`).
- UI loading or transition in progress -> `wait`.
- Interaction is out of scope or failed repeatedly (`scroll`, `drag-drop`,
  right/middle click, unsupported control) -> `action`.
- Elevated risk/ambiguity -> `warning`.
- Highest-risk/safety-critical notice -> `danger`.
- Normal guidance/progress/done marker -> `info`.

## Handling `indicate` results

- `result="done"`: verify state using `r.perceive`, then continue or finish.
- `result="skipped"`: only this card action did not run; do not treat as full
  cancellation.
- Timeout: unresolved state, not success. Recover with fresh context and safer
  next step (`wait`, `action`, or retry with corrected target).
- Always choose the next target from `r.perceive` when available.

## Cross-cutting habits

- Keep one logical keyboard automation in one `input` call.
- For replace-text, do select-all + paste in the same `input` sequence.
- Re-read state between steps via `r.perceive`; avoid standalone `perceive()`
  unless needed.
- If the target window is already visible/in focus from `perceive` cues, act
  directly in that window; do not detour through taskbar re-focus steps.
- Keep `desc` concise and non-redundant with the visual highlight.

## Operator checklist (use every run)

Before first action:

- Confirm the goal and target app/window from user context.
- Get a fresh snapshot (`perceive()` if no valid `r.perceive`).
- Choose the next control from the latest snapshot only.

During loop:

- Pick the smallest safe next step (one `indicate` at a time).
- Prefer `click` over equivalent shortcuts.
- Keep `coords` aligned with the selected row in the latest snapshot.
- After each resolution, branch on `result`, then use `r.perceive`.
- If uncertain, surface uncertainty on card (`wait`/`action`/`warning`) instead
  of long chat questions.

Before finish:

- Verify the user goal is visible on the latest snapshot.
- Send one final `info` card with concise completion summary.

## Recovery playbook (when progress stalls)

- **Skip received once**: infer likely cause from `r.perceive` (already done,
  wrong target, manual step), then attempt the next best card.
- **Repeated skips**: switch strategy (`click` target change, then `action` or
  `wait` with clear `desc`) and re-check state.
- **Timeout**: treat as unresolved; reacquire snapshot and choose safer next move.
- **Target disappeared**: reacquire with standalone `perceive()`, then either
  re-locate target or ask user for manual alignment via `action`.
- **Risky operation**: raise `warning`/`danger` before continuing.

## Compact recap (full contract in tool descriptions)

- Buttons:
  - `info|warning|wait|action|danger` -> Next (Tab)
  - `click|input` -> Skip (Escape) + Accept (Tab)
- Type semantics:
  - `click`: center-click target `coords`.
  - `input`: center-click target `coords`, then run key sequence.
  - `wait`: pause/pacing for loading or unstable state.
  - `action`: manual fallback for out-of-scope interaction.
  - `warning`/`danger`/`info`: indication cards with increasing attention level.

For exact payload shape and validation, follow the `perceive`/`indicate` MCP
tool descriptions.

## Examples (minified payloads)

```json
{"type":"info","desc":"Ready for next step."}
{"type":"click","coords":"120,440,72,28"}
{"type":"input","coords":"200,300,320,28","value":{"clip":"user@example.com","chords":[["LeftControl","V"]]}}
{"type":"input","coords":"10,50,600,32","value":{"clip":"https://example.com/","chords":[["LeftControl","A"],["LeftControl","V"]]}}
```

## Anti-patterns to avoid

- One-shot automation ("one indicate then done").
- Calling `perceive()` after every `indicate()` without need.
- Reusing stale `coords`.
- Using `input` when an equivalent visible `click` target exists.
- Splitting one shortcut chain across multiple `indicate` calls.
- Treating one `"skipped"` as global user cancellation.
- Stopping in chat before trying a recovery card.
- Verbose play-by-play narration in chat during the loop.

## When to stop and how to end

- Goal visibly met on screen.
- User explicitly cancels the **entire** task.
- Repeated no-progress after recovery cards and realignment attempts.
- Unapproved `danger` step.

Not default stops: a single skip, missing information, or ambiguous UI. Use
`wait`/`action`/`warning` with clear `desc`, then continue.

End with:
`indicate({ "type": "info", "desc": "Done — <short summary>." })`
