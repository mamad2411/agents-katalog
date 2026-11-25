---
name: a11y-check
description: Audits a page or component for accessibility problems against WCAG 2.2 and lists fixes ordered by impact on real users.
disable-model-invocation: true
---

Check accessibility of: $ARGUMENTS (a page route, component file or folder).

1. Read the markup and styles. Look for: images without meaningful alt, inputs without a label or aria-label, click handlers on div or span, headings that skip levels, missing landmarks (main, nav), links with text like "click here", tables without header cells, and autoplaying media.
2. Check keyboard use: every control reachable by Tab in a logical order, visible focus style (outline not removed), no keyboard trap, Escape closes dialogs and focus returns to the trigger, and focus moves into modals.
3. Check ARIA: roles that duplicate native elements, aria-hidden on focusable items, missing aria-expanded or aria-live for dynamic content, and invalid references to ids.
4. Check color contrast of text and controls against 4.5:1 and 3:1, target size of at least 24 by 24 CSS pixels, and that information is never conveyed by color alone. Respect prefers-reduced-motion.
5. If a dev server is running and axe or Lighthouse is installed, run it and merge the results.

Report issues as Critical, Serious or Minor, each with file and line, the WCAG criterion, and the fix as code. Ask which group to fix first before editing.
