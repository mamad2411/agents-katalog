---
name: icev-workflow
description: "Enforce the ICEV four-step loop (look, work out the change, apply it, check the result) for every Maya scene modification via the mcp-for-maya MCP server. Use whenever a task will create, move, rename, delete, or otherwise mutate scene objects — prevents blind edits by requiring scene_snapshot before changes and scene_assert/scene_review (plus visual tools on GUI sessions) after them."
compatibility: "Tested on Claude Code only; requires mcp-for-maya MCP server"
---

# ICEV Workflow

> **Experimental.** Evaluated on Claude Code only; untested on Codex/Gemini CLI/Cursor. Tracked in issue #3.

ICEV is four steps: look at the scene, work out the change, make the change, then check the result. Every scene change goes through all four, in order, every time. Skipping the look produces blind edits; skipping the check produces claims nobody verified — both are the failure modes this card exists to prevent.

## When to use

- Any request that modifies the scene: create, move/rotate/scale, rename, reparent, delete, or change materials, lights, cameras.
- Read-only questions ("what is in the scene?") need only the look step — answer straight from `scene_snapshot`.

## The loop

### 1. Look (INSPECT)

Call `scene_snapshot()`; add `scene_inspect(target)` for deep detail on one object or zone. Build the picture — names, types, positions, bounding boxes, hierarchy — BEFORE deciding anything.

### 2. Work out the change (COMPUTE)

Plan changes against the snapshot data: positions, sizes, clearances, naming. Follow the naming rules: `GRP_` groups, `GEO_` geometry, `MAT_` materials, `CAM_` cameras, `LGT_` lights, `LOC_` locators — never Maya's default names. If the scene may have changed since the last snapshot, take a new one instead of trusting stale coordinates.

### 3. Apply the change (EXECUTE)

Apply changes with `execute_code` — batch related edits into one call. Before risky or destructive operations, save a checkpoint with `scene_checkpoint(name)` first, so there is a file to read back if something goes wrong.

### 4. Check the result (VERIFY)

- `scene_assert(expectations=...)` — confirm the objects/properties you intended to change.
- `scene_review()` — full check when the change is structural (new groups, relayout, many objects).
- GUI sessions only: `scene_viewport_snapshot()` (what the artist sees) or `scene_render_preview()` (clean single frame) so the AI can look at the result. On headless sessions these return a `gui_session_required` error — do not retry them there.

## Failure handling

- A failed check → look at the affected region again, fix, then check again. Never report success before a check pass confirms it.
- If applying the change fails mid-way → `scene_rollback(filename)` opens the last checkpoint, then `scene_snapshot()` rebuilds context — a checkpoint file carries no undo history.
- After reading a checkpoint back, always take a new snapshot; never assume the state you landed in.

## Standing rules

- Never report "done" on a mutating task without a check step in the same turn.
- Batch related changes into one `execute_code` call; run `scene_review` after a unit of work, not between micro-edits.
- The pipeline (validation, rate limits, pattern scan) catches slips — treat its rejections as stop signals, not obstacles to route around.
