---
name: better-typography
description: "Type that renders well: scale, line-height, tracking, measure, wrapping, truncation, fonts. Use when setting or reviewing text styles, choosing fonts, or fixing text that wraps or truncates badly."
---

# Typography

Mostly restraint: a small scale, comfortable spacing, enough contrast. A label, a table cell, a headline and a paragraph don't share one set of rules. Review the rendered page, not just the code; bad wrapping and truncation only show at real content lengths.

Write fixes in the project's styling system. Never introduce a new or paid typeface unless the task asks for a type change.

Copy belongs to `better-writing`, heading semantics to `better-accessibility`, RTL layout to `better-layout`, contrast to `better-colors`.

## Scale and roles

A small named scale, deviated from rarely. On a team, name by use (`text-body-sm`), not just size. Starting point for a product UI:

| Role | Size | Line-height | Weight |
| --- | --- | --- | --- |
| Display | 36px | 1.1 | 600 |
| Title | 24px | 1.2 | 600 |
| Heading | 18px | 1.3 | 600 |
| Body | 16px | 1.5 | 400 |
| Caption | 13px | 1.4 | 400 |

- Emphasis inside a role is one weight step (400 to 500), not a size change.
- Heading levels map to descending steps; a child never outweighs its parent. Pick the element for semantics, then style it.
- Long-form body starts at 16px. UI text: 14px for inputs and menus, 13px captions, rarely below 12px.
- At most about three fonts. Pair for contrast (serif display over sans body), not near-twins.
- Below 18px stay at weight 400+; weights 100 to 300 are for 28px+ display only.

## Spacing

- Line-height unitless: headings about `1.1`, body `1.5` to `1.6`. Anything wrapping to 3+ lines needs at least `1.4`, even in a tight card.
- Letter-spacing: large headings slightly negative (`-0.02em`), small uppercase labels positive (`0.05em`), body none.
- Measure: cap long-form text at 60 to 75 characters (`65ch`, or `max-w-xl`/`max-w-2xl` at 16px).
- `text-box: trim-both cap alphabetic` removes the font's built-in top/bottom space so text centers in buttons and badges (Chromium 133+, Safari 18.2+; progressive enhancement).

## Wrapping and truncation

- `text-wrap: balance` on headings, `pretty` on descriptions, neither on long-form text.
- `overflow-wrap: break-word` where URLs or IDs could escape; `nowrap` on labels and badges.
- Truncate with `truncate` or `line-clamp-*`, and keep the full value reachable (tooltip or expanded view) when it matters.
- `text-align: start` in interfaces; justify only in specific editorial layouts.

## Rendering details

- `font-variant-numeric: tabular-nums` on any value that changes (timers, counters, prices) so it doesn't shift layout.
- Prefer CSS properties over raw tags: `font-weight: 650` not `"wght" 650`, `tabular-nums` not `"tnum"`. Properties survive a non-variable fallback; raw tags only for custom axes (`"GRAD"`) and stylistic sets (`"ss01"`).
- Load the weights and styles the design uses, or the browser synthesizes fake ones. Set `font-synthesis: none` only after checking every bold, italic and small-cap form exists across the fallback stack.
- `.woff2` on the web.
- `antialiased` (both smoothing properties) once on the root, not per component.
- Underlines: `text-underline-position: from-font` and `text-decoration-thickness: from-font`, `skip-ink: auto`. Only the color animates reliably; for other underline animations, draw it as a separate element. Dotted underline hints at extra info (abbreviations, defined terms).
- Store text in natural case and use `text-transform`. Smart punctuation in rendered text: curly quotes (straight in code), en dash for ranges, the single `…` character, `&nbsp;` in `16 px`.
- iOS Safari zooms on inputs under 16px. Either `text-base sm:text-sm` (looks different on mobile) or keep 16px and `scale()` it down (identical everywhere, more code). Ask which the design wants.
- Set `lang` and `dir` where language or direction changes; isolate mixed-direction values with `<bdi>`. A 3+ line paragraph aligns to its own script inside an opposite-direction UI.
- Keep text selectable. `user-select: none` only on drag or gesture surfaces.

Load [references/fonts-and-recipes.md](references/fonts-and-recipes.md) for choosing typefaces, variable font axes, OpenType tags, the iOS input scale recipe and a CSS-to-Tailwind map.

## Reporting (standalone)

`HIGH`: unreadable text, or content truncated with no way to recover it. `MEDIUM`: broken type system or heading hierarchy. `LOW`: isolated polish. One row per root cause: Severity, Location (`path:line`), Before, After, Why. Check computed heading sizes descend, line-height and measure, and truncation at realistic string lengths; mark what you couldn't run `Not verified`. End with `Block` if any `HIGH`, else `Approve`.
