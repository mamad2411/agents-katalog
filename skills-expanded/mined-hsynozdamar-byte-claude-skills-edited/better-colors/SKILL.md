---
name: better-colors
description: "Color systems: ramps, semantic tokens, dark mode, gradients, OKLCH and contrast. Use when choosing or changing colors, generating a palette from a brand color, or checking a color pair."
---

# Colors

A color system is a few ramps, named by role and checked against the backgrounds they actually render on. Colors have exact answers: compute them with a library (`culori`, `colorjs.io`, `chroma.js`) and never report a contrast value you didn't measure.

Contrast minimums are not style; `better-accessibility` owns when a pair must pass.

## Defaults

- **Notation.** Reuse the project's notation. A hex codebase stays hex; don't drop one `oklch()` into it. For a new system, `oklch()` is the best default because its lightness steps evenly and its hue holds.
- **Ramps.** One neutral ramp (carries 80 to 90% of the UI), one accent ramp, and only the status ramps the product renders. A second accent hue earns its place only when two things must be told apart at a glance.
- **Every step has a role**: page bg, component bg, hover, border, focus ring, solid fill, fill hover, low- and high-contrast text. Don't generate steps nothing uses. Role mapping for Tailwind `50`-`950` and Radix `1`-`12` is in [references/ramps.md](references/ramps.md).
- **Two token tiers.** Primitives name a value (`--blue-500`) and never appear in components. Semantics name a job (`--color-text-secondary`) and are the only tier components use. That seam is what makes theming possible. Naming grammar in [references/tokens.md](references/tokens.md).
- **Use a token only in its role.** Never borrow a separator as a text color because it looks right today; add the missing token.
- **One color, one meaning.** Hues within about 15° read as the same color. If the accent means interactive, don't put it on static text, and don't render an interactive element neutral.
- **One filled action per view** when fill encodes emphasis. Color goes on the background, not the label. Several colored fills are fine when they encode distinct states or categories.

## A well-formed ramp

- Even steps in *perceived* lightness, not HSL lightness (HSL ramps bunch and drift in hue).
- Constant hue end to end.
- Vividness (chroma) peaks mid-ramp and falls toward both ends.
- Denser at the light end: `50`/`100`/`200` close together, `800`-`950` further apart, so `50` and `100` still read as two surfaces.
- Both ends stop short of pure black and white.
- Across hues, match lightness exactly per step and match chroma as a *proportion of each hue's own max*. Copying one chroma number leaves yellow and cyan weak.
- Brand color goes on the solid-fill step (`500` / `9`). If it fails contrast with white text, keep it as is and use a darker step for interactive fills. Never quietly darken the brand.

## Gotchas

- **Dark mode is not the light ramp reversed.** Reverse as a start, then lower chroma a step or two, widen separation at the dark end, and remeasure every pair (contrast is not symmetric).
- **One switching mechanism.** `prefers-color-scheme` alone without a toggle; a `.dark` class once users can override; `light-dark()` needs `color-scheme` set. Mixing them half-themes the UI.
- **Fix contrast with lightness**, not hue. Hold hue and chroma, move L, remeasure.
- **Measure against the real background**: the card, not the page; worst region of an image or gradient; both themes; translucent surfaces against the lightest and darkest content behind them. `color-mix()`, relative color and `/50` alpha resolve at render time, so measure the result.
- **P3 needs an sRGB fallback first**, then override inside `@media (color-gamut: p3)`. Out-of-gamut colors clip and flatten neighboring steps.
- **Gradient space is a look.** `in oklab` is the even default; `in oklch` stays vivid but can sweep through unwanted hues; plain sRGB muddies the midpoint. Opposite hues go gray in a rectangular space: use `oklch` or add a middle stop.
- **Status hue must differ from the accent.** A red brand needs danger moved toward crimson and checked side by side.
- **When a pair fails, report it** (pair, measured value, threshold missed) and leave the colors alone unless asked. They are a design decision.

## References

- [references/ramps.md](references/ramps.md): load when generating a palette, mapping steps to roles, tuning dark mode or auditing an existing palette.
- [references/tokens.md](references/tokens.md): load when naming or restructuring tokens, or setting up Tailwind v4 `@theme`.
- [references/contrast.md](references/contrast.md): load when measuring or fixing a pair (APCA and WCAG thresholds, quick estimates).
- [references/formats-and-gradients.md](references/formats-and-gradients.md): load for conversions, gamut/P3, `color-mix()`, gradients, increased contrast or locale color meaning.

## Reporting

Severity: `HIGH` makes content unreadable or gives a misleading semantic color; `MEDIUM` is a theme, token or gamut failure; `LOW` is polish. One row per root cause, ordered by severity:

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |

`Location` is `file:line`. Mark anything you could not check as `Not verified`. End with `Block` if any `HIGH` remains, otherwise `Approve`. With nothing to report, say "No actionable color findings".
