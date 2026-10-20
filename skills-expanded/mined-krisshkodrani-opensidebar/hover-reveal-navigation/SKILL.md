# Hover Reveal Navigation

## When To Use

Use this skill when the target action depends on revealing UI through hover before the real target can be read or clicked.

Use it for:

- hover-driven navigation menus
- flyout menus or tooltips that expose the next target
- tasks where the visible control is only a reveal trigger, not the final target

Do not use it for:

- normal click-to-open menus
- layouts where the target is already visible without reveal
- generic navigation tasks with no hidden intermediate UI

## Procedure

1. Read the current page and identify the reveal trigger and the expected revealed content.
2. Hover the trigger deliberately rather than clicking it immediately.
3. Re-read or inspect the revealed area to confirm the menu, tooltip, or flyout actually appeared.
4. Only after the revealed target is visible, click or read the intended item.
5. If the reveal collapses while switching focus, re-ground and repeat the reveal instead of guessing.
6. Store the revealed target or extracted value before moving to the next step.
7. If the revealed value is only an intermediate fact, transition immediately into the downstream action that uses it instead of re-reading the same tooltip or flyout.

## Required Evidence

- The trigger element used for the reveal
- Visible evidence that the hover-dependent UI appeared
- The revealed target or value read from the revealed UI
- Evidence that any downstream action using the revealed value was actually started or completed

## Common Failures

- Clicking the trigger instead of hovering it first
- Assuming the hover succeeded without verifying the revealed UI
- Losing the revealed state and then clicking based on stale assumptions
- Repeatedly re-reading the revealed UI after the needed value is already known

## Verification

- Prefer deterministic confirmation that the revealed menu, tooltip, or flyout text is now visible before acting on it.
- If the reveal is transient, capture the needed fact immediately after verification.

## Relevance

This skill is narrow but real. It should be used only for hover-dependent interfaces, not as a generic navigation skill.

Current strongest E2E target:

- `tests/e2e/hover-menus.test.ts`

Additional candidate targets:

- future tooltip-first lookup flows
- future flyout navigation surfaces where reveal and action must stay separate
