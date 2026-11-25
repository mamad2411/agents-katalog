---
name: dialog-accessibility
description: "Review or repair web dialog, modal, drawer, or popover-as-dialog accessibility: naming, initial focus, containment, Escape, inert background, close controls, and focus restoration. Use for dialog interaction or focus-trap work, not cosmetic-only changes."
license: MIT
metadata:
  version: "1.0"
---

# Dialog accessibility

Verify the whole open–operate–close lifecycle.

## Workflow

1. Reuse the project's established accessible dialog primitive when it fits
   (for example, its existing Radix Dialog). When choosing a new primitive,
   consider native `<dialog>`; do not replace working components merely to
   satisfy a preferred implementation.
2. Open it from a known invoker and apply
   [references/dialog-checklist.md](references/dialog-checklist.md).
3. Verify the accessible name and any useful description, deliberate initial
   focus, containment for a modal, background inertness, keyboard-operable close
   control, Escape behavior, and restoration to the logical invoker.
4. Test close by every offered path and test DOM removal or route changes that
   invalidate the invoker.
5. Replay at mobile width and high zoom. Assess nested dialogs as a separate
   high-risk interaction.
6. Record the bounded keyboard journey and rerun the relevant existing checks
   after repairs. If a browser or scan is unavailable, state the unverified
   behavior instead of claiming a live pass.

## Boundaries

Do not force focus to the first interactive control when a heading or
explanatory content is the more useful starting point. Do not add `role=dialog`
without implementing the interaction model. A passing axe scan does not prove
containment, restoration, or mobile usability.

## Local integration

Use only tooling already available for the task or dependencies justified by
the requested implementation. Follow browser-tool access rules. Keep source
review, synthetic/component tests, browser observation, and assistive-technology
validation distinct; do not claim unperformed checks. Preserve project scope
and existing authorization for external actions.
