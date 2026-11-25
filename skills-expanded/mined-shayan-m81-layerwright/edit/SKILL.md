---
name: edit
description: Change an existing Figma design - the current selection or a frame named by the user - with the Design System, in one undo step. Use for /layer:edit.
argument-hint: "<the change>"
disable-model-invocation: true
---

# Change an existing design

The change is what the user typed after the command. Follow the figma-design skill, §5 (Job C):

1. `figma_status` with a `title`. What to change: the selection (`figma_inspect` target "selection"; with other sessions connected the user confirms it in the Figma window) or the frame they named (`figma_inspect` target "page", then by id).
2. Read before you write: `figma_inspect({ format: "summary" })`, then `"text"`, `"instances"` or `"tree"` as needed.
3. Changing or removing existing layers needs the user's yes: say exactly what will change, then `figma_edit({ ops, approved: true })` (one call, one undo step), or a plan with `inserts` for new parts.
4. Look at the result (`figma_export_image`) and fix what looks wrong.
5. Report what changed; one undo in Figma (⌘Z, or Ctrl+Z on Windows) reverts it.
