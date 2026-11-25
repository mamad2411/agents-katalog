---
name: visual-verification
description: Inspect rendered UI or graphics and verify affected interactions when implementing a visual change or auditing an interface.
---

# Verify the rendered result

Render the affected product surface, capture it, and open the image at readable
scale before claiming a visual outcome. A passing build or an unopened screenshot
does not establish appearance. Use the project's existing harness when possible.

## Choose the relevant evidence

- For a component change, inspect that component and its affected states.
- For a whole-screen audit, inspect overlapping readable close-ups covering the
  screen before judging the full composition. Open each close-up, record what it
  shows, then inspect the next. A contact sheet is useful for routing, not a
  substitute for detail inspection. Recapture affected regions after corrections.
- For web interactions, read [browser QA](references/browser-qa.md).
- For transient motion defects, read [motion evidence](references/motion.md).
- If a capture harness is needed, see [capture examples](references/capture.md).

Inspect presence, clipping, alignment, legibility, contrast, and visual hierarchy.
Cover the viewport sizes and empty, loading, error, ready, focus, or disabled
states relevant to the change. Keep a narrow fix from becoming an unrelated audit.

A specimen board supports an asset or direction decision. Inspect the integrated
surface and affected controls before calling the feature complete. Distinguish
headless, development, packaged-app, and device evidence in the report.

Run required checks and relevant verification. After they pass, broaden or repeat
only for a new change, failure, or unresolved concern. If rendering is unavailable,
continue useful work and state the verification gap plainly.
