---
description: Audit a live URL for motion-accessibility issues (WCAG 2.2.2 Pause, Stop, Hide and WCAG 2.3.3 Animation from Interactions). Use when asked to check a site's animations, reduced-motion support, autoplaying/looping motion, or "motion slop".
argument-hint: <url>
---

# Motion-accessibility audit

Audit the URL in "$ARGUMENTS" (ask for one if missing):

1. Call the `motion_audit` MCP tool with the URL.
2. Read `status` first. If it is `not-measurable`, say that no CSS motion was
   found in the loaded CSS and that runtime motion was not checked — do not
   report a score (it is `null`).
3. Otherwise report the score and each finding with its selector, the rule it
   violates, the WCAG reference (2.2.2 or 2.3.3), and the suggested fix snippet.
   List `preload-candidate` findings (loading indicators) separately as items
   for manual review; they do not affect the score.
4. If the page is measurable and clean, say so and mention the
   `reduced-motion-safe` badge string the tool returns.

State the scope honestly in every report:

- This is a static scan of the page's linked CSS and `<style>` blocks —
  runtime animation (WAAPI, GSAP, JS-driven) is **not** evaluated.
- It is a motion-accessibility check, not a full accessibility audit, and it
  never yields a legal compliance verdict.

Typical findings: animation or transition without an effective
`prefers-reduced-motion` guard, animated properties other than
transform/opacity, `infinite` animation with no pause path, and marquee/autoplay
motion longer than 5 seconds. Colour/opacity-only transitions are not motion
under WCAG 2.3.3 and are not reported.
