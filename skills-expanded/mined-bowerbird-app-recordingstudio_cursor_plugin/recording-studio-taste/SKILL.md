---
name: recording-studio-taste
description: Critique and compose Recording Studio screens so they do not look templated. Use when reviewing or designing gem, dummy, Admin, or host Flatpack UI. Execution is Flatpack ViewComponents, tokens, and named themes.
---

# Recording Studio taste

Taste and branding are direction. Implementation is always Flatpack ViewComponents, tokens, and named themes. The dummy default is `html data-theme="rounded"` plus core `UsesDefaultLayout`. Hosts get a named theme (for example `featured-in`), not forked CSS. Never Tailwind, shadcn, GSAP, custom CSS kits, or third-party UI libraries on gem, dummy, or Admin screens. If a look is missing, add a Flatpack token or component first.

Adapted from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) `skills/taste-skill` (MIT, Leonxlnx). See `docs/taste-skill-attribution.md`.

Page shape: `recording-studio-ui`. Components: `recording-studio-flatpack`. Words: `recording-studio-text`. Completeness: `recording-studio-output`. Audit an existing screen: `recording-studio-redesign`. Opt-in looks: `recording-studio-soft`, `recording-studio-minimalist`, `recording-studio-brutalist`. Brand or image jobs: `recording-studio-brandkit`, `recording-studio-imagegen-web`, `recording-studio-imagegen-mobile`. Image then code: `recording-studio-image-to-code`.

## When to use

- Composing or improving a gem, dummy, Admin, or host screen
- A review that only said "looks fine" or listed checklist boxes
- A host asking for a distinct look (named theme, not a CSS fork)
- Anyone reaching for Tailwind, shadcn, GSAP, or a custom kit

This skill applies to Recording Studio product UI. Do not skip dummy, gem, or Admin because a source pack said "not for dashboards."

## Four-part critique (required)

A Taste review must return all four parts. Checklist-only is a fail.

1. **Design read** - one line: page kind, audience, vibe, and which Flatpack theme or token family it should lean on.
2. **What already looks good** - keep these. Do not restyle for sport.
3. **3-7 specific notes** - each is "this would look better if…" plus a named owner (see Ownership). Type, space, color, or weight. Not "improve hierarchy."
4. **One highest-leverage change** - the single edit that would lift the screen most.

Pre-flight is the fence after that critique, not a substitute for it.

## Ownership

Every "would look better if…" note must name the owner:

- a Flatpack token or component (looked up first)
- a mixin gem (for example Attachable, Publishable)
- core default layout (`UsesDefaultLayout`)
- this gem or host

If the chrome is a mixin screen (Attachable replace, Publishable badge), say so. Do not recommend a one-off restyle in the reviewing gem.

## Look up Flatpack first

Before naming `PageTitle`, `ButtonGroup`, `Card::Footer`, or any other part, check the live demo at https://flatpack.bowerbird.io/ and follow `recording-studio-flatpack`.

If it is not there, the note is "add this token or component to Flatpack," not a minted helper name.

## Product screens stay on core UsesDefaultLayout

Product screens stay on core `UsesDefaultLayout`. Do not wrap a title plus one-action form in an extra `Card::Component`. Cards only when there is real grouping (for example a photo plus its file actions). Dummy, gem, and Admin stay `data-theme="rounded"` unless opted in.

## Design read (before code)

Infer what the brief actually wants. Do not jump to a default look.

Read: page kind (section, one-action form, empty state, host marketing), vibe words, references, audience, existing brand tokens, quiet constraints (access, trust, regulated copy).

State one line before generating:

`Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <Flatpack theme or token family>.`

Examples:

- *Reading this as: dummy Admin section for operators, with a calm kit language, leaning toward `data-theme="rounded"` plus core `UsesDefaultLayout`.*
- *Reading this as: host marketing page for design-conscious buyers, with an editorial language, leaning toward a named Flatpack theme such as `featured-in` or `minimalist`.*

If the read genuinely diverges, ask **one** question. If you can infer, declare the read and proceed.

Do not default to AI-purple gradients, three equal feature cards, glass on everything, Inter plus slate, or infinite micro-motion. Reach past those using the read.

Dummy, gem, and Admin stay on rounded plus `UsesDefaultLayout` unless this chat explicitly opts a surface into a direction pack. Hosts pick a named theme. Kitchen-sink `/demo` is not a product screen.

## Three dials

After the read, set three dials. Overrides happen in conversation, not by editing this file.

- `DESIGN_VARIANCE` - 1 = symmetry, 10 = asymmetry
- `MOTION_INTENSITY` - 1 = static, 10 = cinematic
- `VISUAL_DENSITY` - 1 = airy, 10 = packed

Baseline: `6 / 3 / 4` for gem, dummy, and Admin. Marketing or portfolio hosts may rise toward `8 / 6 / 4`. Trust-first or regulated surfaces stay low (`3-4 / 2-3 / 4-5`).

| Signal | Variance | Motion | Density |
| --- | --- | --- | --- |
| Dummy / gem / Admin kit | 4-6 | 2-3 | 4-5 |
| Minimalist / editorial / calm | 5-6 | 2-4 | 2-3 |
| Soft / premium / Apple-adjacent | 7-8 | 4-6 | 3-4 |
| Brutalist / experimental host | 8-10 | 3-5 | 3-5 |
| Redesign, preserve | match existing | +1 | match existing |
| Redesign, overhaul | +2 | +2 | match existing |

### How dials land in Flatpack

Variance is alignment and scale through Flatpack layout components and theme tokens, not a custom grid kit. High variance on a host theme can offset a title or mix media ratios. Gem and Admin stay closer to the core default layout: title, optional subtitle, one primary action.

Motion is Flatpack hover, focus, active, and enter states. Honor `prefers-reduced-motion`. Animate transform and opacity only. Never GSAP, Motion/`framer-motion`, scroll hijacks, or `window` scroll listeners.

Density is padding, gap, and type-scale tokens. High density is tighter tokens and fewer cards, not a cockpit of custom boxes. Cards exist only when elevation is real hierarchy.

## Type

Headlines should feel heavy and intentional: larger display size, tighter tracking, shorter line-height. Body stays readable, roughly 65 characters, relaxed leading.

Use the theme type stack. Do not import webfonts beside Flatpack. Do not default to Inter. Serif only when the named theme or brand actually calls for it. Do not inject a random serif word into a sans headline; emphasize with italic or weight of the same family.

Use medium and semibold, not only regular and bold. Tabular figures for numbers. Negative tracking on large titles, a little positive tracking on small labels. Sentence case over Title Case On Every Header. `text-wrap: balance` or `pretty` for orphans when the theme supports it.

Italic display words with descenders (`y g j p q`) need enough line-height so tails are not clipped.

## Color and surface

One accent. Saturation under 80% unless the brand is the accent. Neutral bases, not AI purple or blue glow. One gray family (warm or cool, not both). Once an accent is chosen, it is the accent on the whole page.

No pure `#000` or `#fff` unless the named theme requires it. Tint shadows to the surface hue. One corner-radius scale from the theme: all-sharp, all-soft, or documented mixed rule (for example buttons pill, cards 16px). Mixed radii with no rule look broken.

Premium-consumer beige plus brass plus espresso is a repeated AI tell. Do not reach for it unless the brand names those colors. Rotate: cold luxury, forest, black and tan, cobalt and cream, terracotta and slate, or monochrome plus one pop.

Page has one theme. Sections do not invert from light to dark mid-scroll unless the brief asks for a single deliberate color-block. Host dark mode uses Flatpack theme tokens, not a per-section override.

## Space and layout

Core product pages follow `recording-studio-ui` and stay on `UsesDefaultLayout`: title, optional subtitle, one primary action, no competing shell. Do not wrap that page in an extra `Card::Component`. Do not invent a sidebar or kitchen-sink dashboard.

Hero or first viewport (host marketing only): headline two lines max, supporting line about 20 words, primary action visible without scroll. Max four text elements in that first moment (optional eyebrow, headline, support, actions). Trust logos live under the hero, not inside it.

Avoid: three equal feature cards, zigzag image-text more than twice in a row, split headers that park filler text in the right column, eyebrows on every section (at most one per three sections), decoration strips (`TYPE / FORM / MOTION`), scroll cues, version stamps, locale-weather toys.

Bento or feature grids have exactly as many cells as there is content. At least some cells need real visual variation (image, tint, pattern token), not a row of identical empty cards.

Long lists need the right Flatpack component (table, definition list, accordion, cards), not a hairline under every row.

## States and contrast

Implement the full cycle with Flatpack: loading skeletons that match the layout, composed empty states, inline errors. Pressed feedback on buttons (`scale` or a 1px press via theme). Visible focus rings.

Button text must read against the button fill (WCAG AA). Ghost buttons over photos need a scrim or stroke. Labels stay on one line. One label per intent on a page ("Get in touch" and "Let's talk" are the same intent).

Label above input, error below, no placeholder-as-label. Form text and focus rings pass AA against the section.

## Motion (Flatpack only)

Before adding motion, say what it communicates: hierarchy, sequence, feedback, or state change. "It looked cool" is not a reason.

`MOTION_INTENSITY` 1-3: hover and active only. 4-7: short theme transitions on enter and press. 8-10 only on a host theme that already has those tokens. If you cannot ship working motion inside Flatpack, drop the dial and ship a still page.

Reduced motion is mandatory above intensity 3. Infinite loops, parallax, and magnetic cursors are out of scope.

## Anti-slop

Banned unless the brief asks for them: neon outer glows, oversized shouting H1s, three equal cards, generic glass, custom cursors, div-based fake screenshots, hand-rolled decorative SVGs as the default, pills overlaid on photos, section-number eyebrows (`01 / Capabilities`), decorative status dots, em-dash as a design flourish in on-screen copy, filler verbs (Elevate, Seamless, Unleash, Next-Gen), Jane Doe / Acme / Nexus names, fake-precise specs the brand does not claim.

Real images when the page is visual: generate or use real assets. A text-only marketing page is incomplete, not minimal. Product screens can be typographic if the job is a form.

Copy: re-read every visible string. Rewrite grammar breaks, unclear referents, and LLM-cute phrases. Prefer a plain sentence. Follow `recording-studio-text`.

## What not to do

- Do not restyle dummy, gem, or Admin off rounded unless the user opts that surface in
- Do not fork CSS to fake a look; add a Flatpack token or named theme
- Do not install generic frontend taste packs as Cursor plugins
- Do not treat kitchen-sink `/demo` as the product
- Do not return a checklist instead of the four-part critique

## Pre-flight

Run after the four-part critique. If a box fails, the page is not done.

- [ ] Design read declared
- [ ] Dials explicit and reasoned
- [ ] Critique has 3-7 "would look better if…" notes, each with a named owner
- [ ] Named parts exist on https://flatpack.bowerbird.io/ or the note is "add this to Flatpack"
- [ ] Product screens stay on `UsesDefaultLayout`; no extra card around a title plus one-action form
- [ ] Dummy / gem / Admin still rounded plus `UsesDefaultLayout` unless opted in
- [ ] Host look is a named theme, not forked CSS
- [ ] No Tailwind, shadcn, GSAP, or custom CSS kit
- [ ] One accent, one radius scale, one theme
- [ ] Contrast AA on buttons, body, and form chrome
- [ ] Motion is Flatpack-only and reduced-motion safe
- [ ] No AI tells from the anti-slop list
- [ ] Words follow `recording-studio-text`
