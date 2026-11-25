---
name: progress-event-state-bridge
description: "Bridge reconciliation progress events into shared UI state so the install surface reflects installing, installed, and failed transitions."
metadata:
  author: ychampion
---

# SKILL: Progress Event State Bridge
**Domain:** plugin-installation
**Trigger:** Use when background reconciliation emits per-source progress updates and shared UI state must reflect each source's lifecycle (`installing`, `installed`, `failed`).
**Source Pattern:** Distilled from reviewed install-progress callbacks and immutable UI-state bridge implementations.

## Core Method
Let the reconciler emit progress events for each marketplace or extension source, then bridge those events into shared UI state through one immutable update path. Each event should update only the matching source entry, carrying both the new status and any error payload, while leaving unrelated entries untouched. This makes the install UI responsive without forcing broad rerenders or duplicating install logic in the view layer.

## Key Rules
- Use one immutable helper or reducer path so only the target entry changes and unrelated UI state keeps structural sharing.
- Preserve the event’s status semantics directly: `installing`, `installed`, and `failed` should remain distinct in the UI state.
- If the event carries an error payload, preserve it so the UI can surface meaningful diagnostics.
- Progress events should update previously seeded entries, not silently invent new rows that were never declared to the user.

## Example Application
When a background source sync starts, the UI row for that source flips from `pending` to `installing`. If the fetch succeeds, it moves to `installed`; if it fails, it moves to `failed` and stores the error text for display.

## Anti-Patterns (What NOT to do)
- Do not mutate the source list in place or reorder entries when mapping events; unaffected rows should retain reference stability.
- Do not drop the `error` payload when a `failed` event fires; without it, the UI cannot explain why manual intervention is required.
- Do not rebuild unrelated state slices while handling these events; keep the bridge scoped to the installation-status surface.

