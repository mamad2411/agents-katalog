---
name: accessibility-gate
description: Use before declaring a UI change done, fixed, working, ready, or shipped. Forces a real accessibility pass across keyboard flow, focus visibility, accessible names, contrast, reduced motion, and the platform's native semantics.
---

# Accessibility Gate

**A screen that looks right can still be unusable.** Before calling UI work
done, exercise it like a keyboard user and inspect the semantics a screen reader
will receive.

## The pass

1. Identify the changed surface and its interactive states.
2. Run the smallest real check available: axe/pa11y/Lighthouse, a focused UI
   test, or a manual keyboard pass when no automated check exists.
3. Tab through the complete flow. Confirm order, visible focus, escape/back
   behavior, and that no control is keyboard-trapped.
4. Check accessible names, roles, state announcements, contrast, touch targets,
   reduced motion, and error/empty/loading states.
5. Fix failures and repeat the check. Do not report a clean compile as a11y
   evidence.
6. End with the exact sentinel, including the checks and outcome:

   ```text
   ACCESSIBILITY-GATE: PASS — keyboard flow + axe scan, 0 blockers
   ```

The Stop hook blocks UI turns that do not include this evidence. It is silent on
non-UI work and fails open if its own inspection cannot run.

## Kill switch

```bash
touch .accessibility-gate-off
```

Or set `ACCESSIBILITY_GATE=off` for a single session.
