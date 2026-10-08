---
name: interface-polish
description: A checklist of concrete UI craft rules covering border radius, shadows, animation timing, typography, color tokens, accessibility, layout spacing, and microcopy. Use this skill whenever building, reviewing, or refining any web UI, component, page, landing page, or design system code, even if the user only says "make it look better", "polish this", "review my component", or asks for a button, menu, modal, form, or any frontend work. Also use it when writing UI copy like button labels, empty states, or confirmation dialogs. Distilled from the interfaces.dev cheat sheet.
---

# Interface Polish

Practical rules for making interfaces clearer, easier to use, and more polished. Apply these by default when writing or reviewing frontend code. Each rule is short; when one applies, just do it rather than asking.

Adapted and condensed from the [interfaces.dev cheat sheet](https://interfaces.dev/cheat-sheet) by [Jakub Krehel](https://x.com/jakubkrehel), published here with his permission. For deeper typography, color, or motion work, pair this with the better-typography, better-colors, apple-design, and emil-design-eng skills if available.

## Visual details

**Concentric radii on nested elements.** Inner radius = outer radius minus the gap between them. A card with `16px` radius and `8px` padding gives its inner element `8px` radius. Never give a nested element the same radius as its parent.

**Optical over geometric alignment.** Center things by eye, not just by math. Play icons, arrows, and asymmetric glyphs usually need a 1–2px nudge to look centered.

**Asymmetric button padding with icons.** When a button has an icon plus text, reduce the padding on the icon side slightly (the icon carries visual weight that text doesn't).

**Layered shadows over borders for depth.** Stack 2–3 `box-shadow` layers (a tight low-opacity ring plus softer larger shadows) instead of a flat `1px` border when you want elevation.

**Hairline outlines on images.** Give images a subtle inset ring so light images don't bleed into light backgrounds: `outline: 1px solid rgb(0 0 0 / 0.08); outline-offset: -1px;` (use white at 8% in dark mode).

**Match icon stroke to adjacent text weight.** An icon next to `font-weight: 500` text should have a stroke width that reads at the same weight. Thin icons next to medium text (or vice versa) look mismatched.

## Animation

**Animate from the trigger, not the center.** Set `transform-origin` based on where the trigger sits relative to the popover/menu (e.g., a menu opening below-left of a button gets `transform-origin: top right`).

**Frequently opened menus: skip the enter animation.** Context menus and other high-frequency surfaces should appear instantly and only animate on exit.

**Exits are subtler than entrances.** On exit, move a shorter distance while fading `opacity` and adding a small blur (~`4px`). Don't mirror the entrance exactly.

**Never `transition: all`.** Name the exact properties: `transition: background-color 150ms ease, color 150ms ease`. `all` causes accidental animations and jank.

**Press feedback on buttons.** Scale to `0.95`–`0.98` on `:active` with `transition: scale 200ms ease-out`.

**Icon swaps crossfade.** New icon: scale `0.25 → 1`, opacity `0 → 1`, blur `4px → 0`. Old icon reverses the same values. Don't hard-swap.

**Transitions for interactions, keyframes for sequences.** CSS transitions can reverse mid-flight (hover off before hover animation ends); keyframes can't. Use keyframes only for one-shot sequences.

**Kill transitions during theme switches.** Temporarily disable all transitions when toggling light/dark mode so hundreds of properties don't animate at once.

**Fix 1–2px jitter with `will-change: transform`.** If an element shifts randomly while animating (common in iOS Safari), add it. Don't sprinkle it everywhere preemptively.

**Stagger entrances in small groups.** Animate sections in with short delays between groups rather than one giant block or every element individually.

**No animations on page load** unless intentional. Guard mount animations so a page refresh doesn't replay every transition (e.g., only animate after first paint or on state change).

**Frequent interactions are instant.** Hover color changes and similar high-frequency feedback should have zero or near-zero duration.

## Typography

**Only `.woff2` on the web.** Never ship `.ttf` or `.otf`; `.woff` only as a legacy fallback.

**`font-variant-numeric: tabular-nums`** for timers, counters, prices, and table columns so digits don't cause layout shift. Unnecessary in monospace fonts.

**Line length 60–75 characters** for articles and long-form text. Cap the measure with `max-width` (e.g., `65ch`).

**`text-wrap: balance` on headings, `text-wrap: pretty` on short descriptions.** Neither on long-form body text.

**Contain overflow.** `overflow-wrap: break-word` keeps long URLs, IDs, and API keys inside their container. `white-space: nowrap` keeps labels and badges from wrapping.

**Root-level font smoothing.** `-webkit-font-smoothing: antialiased` and `-moz-osx-font-smoothing: grayscale` on the root layout for crisper text.

**Write in normal case, transform with CSS.** Store "Typographic detail" and apply `text-transform: uppercase` for display; don't hardcode shouting case in content.

**Smart punctuation.** Curly quotes, en dash for ranges (2010–2020), em dash for asides, real ellipsis character instead of three periods. (If the user's own writing preferences forbid em dashes, their preference wins for copy they'll publish.)

**Clean underlines.** `text-underline-position: from-font` with `text-decoration-skip-ink: auto` so descenders like g and y aren't crossed.

**Truncation needs an escape hatch.** Any text cut with an ellipsis must be readable in full via tooltip or an expanded view.

## Color

**Every palette step earns its place.** Map each step to a purpose (page background, hover, border, solid fill, body text). Delete steps nothing uses.

**Semantic tokens in components, never primitives.** Components reference `--color-text-secondary`, not `--blue-500`. Primitives feed tokens; tokens feed components.

**Name tokens by purpose, not appearance or location.** `--color-accent-solid`, not `--color-blue-button` (breaks when the brand goes violet) or `--color-sidebar-gray` (breaks when reused elsewhere).

**Reserve `accent` for brand color.** Don't let `primary` mean both "brand color" and "primary text" — use `--color-text-primary` and `--color-accent-solid` as separate namespaces.

**Measure contrast against the immediate background.** Text on a card is measured against the card surface, not the page behind it.

**Dark mode gets its own palette.** Never invert the light palette; shadows, saturation, and hierarchy behave differently on dark surfaces.

**One theming mechanism.** Pick either `prefers-color-scheme` media queries or a `.dark` class for all tokens. Mixing both causes surfaces and text to disagree.

**Choose gradient interpolation deliberately.** `in oklab` for even brightness, `in oklch` for vivid midpoints, `in srgb` for muted midtones.

## Accessibility

**Native elements first.** `<button>` for actions, `<a href>` for navigation. A div with a click handler loses middle-click, right-click menus, focus behavior, and screen reader semantics for free.

**Style `:focus-visible`, not `:focus`.** Never remove the outline without providing a replacement.

**`tabindex` is only ever `0` or `-1`.** Positive values scramble the natural focus order.

**Icon-only buttons get `aria-label`.** Never `aria-hidden="true"` on anything focusable.

**Alt text describes purpose and content.** Decorative images get `alt=""` (empty, not missing).

**Every input gets a visible `<label>`.** Placeholders are not labels — they vanish on input. Set `type` and `inputmode` so touch keyboards match the expected content (email, numeric, etc.).

**Never block paste.** People paste passwords and one-time codes.

**Form validation pattern.** Keep submit enabled until the request starts; validate on submit; mark bad fields `aria-invalid="true"`; link error text with `aria-describedby`; move focus to the first invalid field.

**Hit areas: 24×24px minimum**, aim for 44×44 on touch and 40×40 on desktop. They must never overlap.

**`pointer-events: none` on decorative layers** (glows, gradients, overlays) so they never swallow clicks.

**Hover styles inside `@media (hover: hover)`.** On touch screens, `:hover` sticks after a tap and makes items look selected.

**Respect reduced motion.** Wrap animations in `@media (prefers-reduced-motion: no-preference)` so they only run for people who haven't reduced motion.

**Live region roles.** `role="status"` for routine updates ("Link copied"), `role="alert"` only for urgent errors.

**Never color alone for status.** Pair color changes with an icon, label, or underline.

**Skip link first.** The skip-to-content link is the first Tab stop. Add `scroll-margin-top` to headings so anchor jumps don't land flush against the viewport edge.

## Layout

**Group spacing ≥ 2× item spacing.** If items within a group are `8px` apart, groups are at least `16px` apart. Proximity is what communicates grouping.

## Writing (microcopy)

**Buttons start with a verb.** "Save draft", "Delete project" — never "OK!" or a bare "Yes".

**Confirmation buttons state the outcome.** "Delete project" next to "Cancel", not "Yes"/"No".

**One continue label per flow.** Pick "Continue" or "Next" and use it on every step; don't rotate through synonyms.

**Links describe their destination.** "Read the docs", never "Click here".

**One capitalization style everywhere.** Sentence case ("Save changes") is the safest default for buttons, headings, and labels.

**Toggles are labeled by their on-state.** "Send read receipts", never "Disable read receipts".

**Empty states explain and offer one action.** Say what belongs there and give a single starter action ("No projects yet… Create a project"), not just "No results."

**Address the reader as "you".** "You'll receive an email", never "The user will receive an email."

## How to apply this skill

When **writing** new UI code: treat every rule above as a default. Don't announce each rule; just produce code that already follows them.

When **reviewing** UI code: scan against the categories in order (visual → animation → typography → color → accessibility → layout → writing) and report only violations, each with the concrete fix.

When rules conflict with an explicit user instruction or an established design system in their codebase, the user's system wins — note the deviation once and move on.
