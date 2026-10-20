---
name: modal-navigation-stack-with-back
description: For drill-down UIs reusing a single modal surface, snapshot head/path/body before each open and push to a stack; a Back button / Backspace pops the stack, Esc clears it.
category: frontend
triggers:
  - modal drill down
  - single modal multiple views
  - back button modal
  - reusable popup
tags:
  - ui
  - vanilla-js
version: 1.0.0
---

# modal-navigation-stack-with-back

Reusing one modal for chained drill-downs (e.g., click a chart segment → see a list → click a row → see a detail) silently destroys prior context — closing the innermost view leaves stale content on reopen, and the user has no way back to the list.

## Pattern

Snapshot current modal content before each open. Pop to restore. Clear the stack on close.

```js
const _stack = [];
function pushSnapshot() {
  if (!modal.classList.contains('open')) { _stack.length = 0; return; }
  _stack.push({ title: $title.innerHTML, path: $path.innerHTML, body: $body.innerHTML });
  $back.style.display = '';
}
function popSnapshot() {
  const prev = _stack.pop();
  if (!prev) { $back.style.display = 'none'; return false; }
  $title.innerHTML = prev.title; $path.innerHTML = prev.path; $body.innerHTML = prev.body;
  if (_stack.length === 0) $back.style.display = 'none';
  return true;
}
function closeModal() { modal.classList.remove('open'); _stack.length = 0; $back.style.display = 'none'; }
```

Call `pushSnapshot()` as the very first line of every `openX(...)` function — before mutating title/path/body. The `if modal is open` guard makes the first open a no-op push.

Bind: `×` → closeModal · `←` / Backspace → popSnapshot · backdrop click / Esc → closeModal.

## Why snapshot HTML instead of a data model

Each drill-down has a different shape (list vs. detail vs. list-of-lists). Reconstructing would require per-view serializers. Snapshotting rendered HTML is a flat, view-agnostic restore and costs a few KB per level.

## Guardrail

Backspace handler must early-return if an INPUT/TEXTAREA has focus — otherwise you eat text-editing backspaces.
