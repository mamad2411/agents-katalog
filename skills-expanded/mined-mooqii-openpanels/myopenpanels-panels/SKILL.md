---
name: myopenpanels-panels
description: Use before reading or changing content through a MyOpenPanels Canvas, Wiki, Writing, Typesetting, or Publishing panel.
---

Use this Skill as the shared operating contract for MyOpenPanels panels. The
current CLI is authoritative for Project context, panel targets, selection,
commands, Tasks, and Operations. Read every Reference required by the current
Bootstrap before acting; do not choose a remembered panel workflow instead.

Shared rules:

- Panel reads and writes target the requested Project panel without changing
  the visible panel. Only current-selection reads require that panel to be
  active.
- Never infer selection from visible content, a preview, screenshot, fallback,
  or most-recent item. Respect the Procedure's selection policy.
- Begin target-bound generation before invoking an external model. Continue
  against the captured target even if the user changes panels.
- Use only commands and flags advertised for the current Procedure. Keep
  Operation and Task completion, failure, and cancellation explicit.
- During a claimed Task, use its Broker and immutable execution context. Never
  read or write shared storage directly.
- A selected portable Skill controls content method or style only. This System
  Skill and the current CLI continue to own targeting, storage, and lifecycle.
- Publishing is Task-only. Use the exact captured release, pre-bound checkpoint
  commands, and result contract from its ExecutionBundle; never replace it with
  a Procedure or a newly discovered Publishing Skill.
- Typesetting generation is Task-only. Use the captured publication snapshot,
  selected Title, Cover, or Layout Skill, workspace paths, and artifact contract from
  the exact ExecutionBundle; never write directly to panel state.

Completion requires all Bootstrap References to have been read and the result
to be committed to the captured panel through its owning Operation or Task.
