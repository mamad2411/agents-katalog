---
name: control-surface-designer
description: Design and review Blacktower control surfaces, including TUI sidebar, OpenTUI dashboard, control-center web UI, status boards, terminal UX, accessibility, state displays, and operator-facing copy.
metadata:
  blacktower-pack: engineering
  blacktower-kind: internal
  blacktower-tier: niche
  blacktower-capabilities: frontend-ui,control,surface,designer
---

# Control Surface Designer

Use this skill when users see or operate the interface that controls agents,
tasks, status, or background work.

## Design workflow

1. **Identify the operator job**
   - What decision must the user make from this screen/panel/status line?
   - What is urgent, stale, blocked, or safe to ignore?

2. **Design for scannability**
   - Put state, risk, and next action above decorative detail.
   - Use stable grouping and consistent labels.
   - Make loading/stale/error states explicit.

3. **Preserve accessibility**
   - Keyboard-first flows.
   - Sufficient contrast.
   - Non-color cues for status.
   - Concise but descriptive labels.

4. **Review copy and affordances**
   - Avoid cute wording in destructive or ambiguous actions.
   - Distinguish cancel, abort, delete, stop, hide, and dismiss.

Read `references/control-surface-principles.md` before substantial UI changes.
Use `templates/control-surface-review.md` for UI review notes and
`examples/status-board.md` as an example status hierarchy.
