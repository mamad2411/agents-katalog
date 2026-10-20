---
name: design-token-extractor
description: Extract a reusable design-token set (color roles, type scale, spacing scale) from a reference site, screenshot, or description into a structured CSS custom-properties file, so a rebuild or redesign stays consistent instead of eyeballing values off a screenshot each time. Use when asked to "match this site's style," "extract the design system from X," or before starting a build that needs to visually match a reference.
---

## Workflow

1. **Identify the reference** — a URL, screenshot, or description of an existing design. If it's a live URL, prefer inspecting the rendered page (e.g. via a screenshot) over guessing from a text description alone.
2. **Extract color roles, not a hex dump.** Group observed colors by function: `background`, `surface` (cards/panels), `text-primary`, `text-secondary`, `border`, `primary` (brand/action color), `accent`. Don't list every slightly-different gray seen — collapse near-duplicates into one role.
3. **Extract a type scale, not every size seen.** Identify the smallest coherent set of font sizes that covers what's actually used (typically 5-7: display, h1-h3, body, small/caption) rather than a size per element.
4. **Extract a spacing scale.** Infer the base unit (commonly 4px or 8px) and the multiples actually in use, rather than recording arbitrary pixel values.
5. **Output as CSS custom properties**, ready to drop into a build:
   ```css
   :root {
     --color-bg: #...;
     --color-surface: #...;
     --color-text-primary: #...;
     --color-text-secondary: #...;
     --color-border: #...;
     --color-primary: #...;
     --color-accent: #...;

     --font-size-display: ...;
     --font-size-h1: ...;
     --font-size-h2: ...;
     --font-size-body: ...;
     --font-size-small: ...;

     --space-1: 4px;
     --space-2: 8px;
     --space-3: 16px;
     --space-4: 24px;
     --space-6: 48px;
   }
   ```
6. **Flag confidence and gaps explicitly.** Values read from a screenshot are approximate (font names in particular often can't be identified exactly from pixels alone) — say so rather than presenting a guess as a measured fact. Note anything that couldn't be determined.

## Related skills in this repo

- **image-to-code**: Run this skill first when cloning a reference UI, so the resulting code uses named tokens instead of hardcoded values scattered through the markup.
- **theme-factory**: A preset theme is a faster starting point when there's no specific reference to match — use this skill only when there's an actual site/screenshot to extract from.
- **brandkit-generator**: Once a brand direction is chosen, extract it into this token format for downstream builds.
- **design-review-audit**: Inconsistent spacing/color values found during a review are a signal to run this extraction (or define a fresh token set) instead of patching values ad hoc.
- **design-dev-resources**: Its tweakcn entry is a live tool for editing shadcn tokens against a real dashboard preview once this skill has produced a token set — useful for iterating on the values interactively rather than only editing them as code.

## Notes

Source: a "Claude Replaces Designers" screenshot-carousel video (@vibes.codes) describing an "Extract Design System" skill that pulls colors/typography/spacing tokens from a reference site.
