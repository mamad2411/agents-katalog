---
name: check-responsive
description: Reviews layout code for small-screen breakage such as overflow, fixed widths and cramped tap targets, then fixes the breakpoints.
disable-model-invocation: true
---

Check the responsive behavior of: $ARGUMENTS (the changed files from `git diff --name-only` if empty).

1. Read the markup and styles. Find the project's breakpoints (config, tokens or media queries) and use those, not new ones.
2. Look for: fixed `width` or `min-width` larger than 320px, `100vw` that causes sideways scroll, absolutely positioned elements, tables and `pre` blocks without an overflow wrapper, images without `max-width: 100%`, long unbroken strings without `overflow-wrap`, and flex or grid rows that never wrap.
3. Check touch targets are at least 44px, body text is at least 16px, and the viewport meta tag exists.
4. For each problem name the file and line, the width where it breaks, and the cause.
5. Apply fixes that are mechanical (wrap, `minmax`, `max-width`, a media query using an existing breakpoint). Ask before changing the visual design.

End with a table of issues found, fixed and left for you, and the widths you reasoned about (320, 375, 768).
