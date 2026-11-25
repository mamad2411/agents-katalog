---
name: recording-studio-redesign
description: Audit an existing Recording Studio screen and upgrade it without a rewrite. Use when a dummy, gem, Admin, or host page looks generic or dated. Execution is Flatpack ViewComponents, tokens, and named themes.
---

# Recording Studio redesign

Taste and branding are direction. Implementation is always Flatpack ViewComponents, tokens, and named themes. The dummy default is `html data-theme="rounded"` plus core `UsesDefaultLayout`. Hosts get a named theme (for example `featured-in`), not forked CSS. Never Tailwind, shadcn, GSAP, custom CSS kits, or third-party UI libraries on gem, dummy, or Admin screens. If a look is missing, add a Flatpack token or component first.

Adapted from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) `skills/redesign-skill` (MIT, Leonxlnx). See `docs/taste-skill-attribution.md`.

Direction and critique: `recording-studio-taste`. Completeness: `recording-studio-output`. Page shape: `recording-studio-ui`. Components: `recording-studio-flatpack`. Words: `recording-studio-text`. Opt-in looks: `recording-studio-soft`, `recording-studio-minimalist`, `recording-studio-brutalist`. Brand boards: `recording-studio-brandkit`.

## When to use

- An existing screen works but looks generic, dated, or AI-default
- A host wants a visual refresh without changing routes or jobs
- A review found weak type, space, color, or missing states

Do not migrate stacks. Do not "use any CSS framework." Stay on Flatpack.

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

## Sequence

1. **Scan** - Read the views and the active theme (`data-theme` on `html`, layout helper, Flatpack components in use).
2. **Diagnose** - Run the audit. List every generic pattern, weak point, and missing state. Then write the four-part Taste critique (`recording-studio-taste`). Checklist-only is a fail.
3. **Fix** - Targeted upgrades through Flatpack tokens and components. Improve what is there. Do not rewrite from scratch.

## Detect the mode

- **Preserve** - modernise without breaking the brand. Audit first. Extract tokens. Evolve.
- **Overhaul** - new visual language on existing content. Treat visuals as greenfield; keep jobs, copy voice, and IA unless asked.
- **Greenfield** - no existing screen, or the brand itself is changing. Use `recording-studio-taste` and compose in Flatpack.

If ambiguous, ask once: preserve the existing brand, or start visually from scratch?

## Audit before touching

Document current state:

- Brand tokens: colors, type, logo, radii, active named theme
- Information architecture: routes, primary nav, conversion or job paths
- Content blocks: what exists, what works, what is filler
- Patterns to keep: signature interactions, recognisable hero, copy voice
- Patterns to retire: AI tells, broken layout, dead links, generic stock, missing states
- Dial reading of the current screen (`DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY`)
- Accessibility wins already present (focus, alt, contrast, keyboard)

Dummy, gem, and Admin stay on rounded plus `UsesDefaultLayout` unless this chat opts that surface into a direction pack.

## Design audit

Each finding must say what would look better and name the owner (Flatpack token or component, mixin gem, core default layout, or this gem/host). Look up Flatpack first.

### Typography

- Browser default or Inter everywhere → theme type stack
- Headlines lack presence → display size, tighter tracking, shorter leading
- Body too wide → measure near 65 characters
- Only 400 and 700 → add medium and semibold
- Proportional numbers in data → tabular figures
- Missing tracking → negative on large titles, slight positive on labels
- All-caps subheaders everywhere → sentence case, small-caps, or a single italic
- Orphans → balance or pretty wrap

### Color and surfaces

- Pure `#000` or `#fff` → off-black / off-white tokens
- Oversaturated accents → one accent, saturation under 80%
- More than one accent, or mixed warm and cool grays → lock one family
- AI purple / blue glow → neutrals plus one considered accent
- Generic black shadows → tinted shadow tokens
- Random dark band in a light page → one theme, or a slightly deeper shade of the same surface
- Empty flat sections on a marketing host → real image, tint, or pattern token, not a custom wash

### Layout

- Everything centered → offset through layout components when variance allows
- Three equal feature cards → asymmetric grid or a different Flatpack grouping
- No max width on a marketing host → theme container
- Cards of forced equal height when content varies → let height follow content, or pick a list
- Uniform radius with no rule → one theme radius scale
- Missing whitespace on a marketing page → larger gap and padding tokens
- Product screen fighting the default layout → return to `UsesDefaultLayout` and one primary action
- Title plus one-action form wrapped in `Card::Component` → drop the extra card; the default layout is the chrome
- Misaligned titles, prices, or buttons across a row → shared Flatpack list or table, or a card only when items are a real group

### States

- No hover, press, or focus → Flatpack interactive states
- Instant changes with no duration → theme transition tokens
- Missing loading / empty / error → Flatpack skeleton, empty, inline error
- Dead `#` links → real path or a disabled control
- No current-page state in nav → active item
- Animating top / left / width / height → transform and opacity only

### Content

- Jane Doe, Acme, Nexus, Lorem Ipsum → real draft copy (`recording-studio-text`)
- Fake-round metrics → organic numbers or labeled samples
- Elevate / Seamless / Unleash / Next-Gen → concrete verbs
- "Oops!" → direct: "Connection failed. Try again."
- Title Case On Every Header → sentence case

### Components

- Card used only because every block is a card → spacing, a divider, or `UsesDefaultLayout`
- Mixin chrome (Attachable replace, Publishable badge) looking off → fix the mixin gem, not a one-off in the reviewing gem
- Accordion FAQ as the only help pattern → list, search, or one extra-info popover
- Modal for a one-field edit → inline or a small dedicated screen
- Footer link farm → main paths plus legal links

## Upgrade order

Maximum lift, minimum risk:

1. Type tokens (biggest visual change, lowest risk)
2. Color cleanup (one accent, one gray family)
3. Hover, press, focus
4. Spacing and default-layout rhythm
5. Replace generic groupings with the right Flatpack component
6. Loading, empty, error
7. Type scale and tracking polish

On a preserve redesign, stop when the brief is satisfied. Do not keep restyling.

## Preservation

Do not silently change:

- URL structure or slugs
- Primary nav labels
- Form field names or order
- Brand logo or wordmark
- Legal, consent, or cookie copy
- Existing accessibility wins
- Analytics event names tied to buttons or fields

Copy voice stays unless asked for a rewrite. Visual modernisation is not a content rewrite.

## Rules

- Work in Flatpack. Do not add Tailwind, shadcn, GSAP, or a CSS kit "because the old file used CSS."
- Look up https://flatpack.bowerbird.io/ before naming a component. Missing parts go to Flatpack, not a minted helper.
- Do not break jobs. Exercise the flow after each change.
- Keep diffs reviewable. Small targeted improvements over a rewrite.
- Host looks ship as a named theme. Dummy / gem / Admin stay rounded unless opted in.
- Product screens stay on `UsesDefaultLayout`. Cards only for real grouping.
