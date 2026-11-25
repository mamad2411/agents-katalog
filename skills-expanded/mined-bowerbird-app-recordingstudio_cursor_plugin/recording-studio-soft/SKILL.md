---
name: recording-studio-soft
description: Soft, expensive-feeling direction for Recording Studio host themes. Use when a host wants haptic depth, quiet luxury, or agency-like polish. Execution is a named Flatpack theme with ViewComponents and tokens, not custom CSS.
---

# Recording Studio soft

Taste and branding are direction. Implementation is always Flatpack ViewComponents, tokens, and named themes. The dummy default is `html data-theme="rounded"` plus core `UsesDefaultLayout`. Hosts get a named theme (for example `featured-in`), not forked CSS. Never Tailwind, shadcn, GSAP, custom CSS kits, or third-party UI libraries on gem, dummy, or Admin screens. If a look is missing, add a Flatpack token or component first.

Adapted from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) `skills/soft-skill` (MIT, Leonxlnx). See `docs/taste-skill-attribution.md`.

This is a direction pack. Critique and dials: `recording-studio-taste`. Audit: `recording-studio-redesign`. Completeness: `recording-studio-output`. Page shape: `recording-studio-ui`. Components: `recording-studio-flatpack`. Other packs: `recording-studio-minimalist`, `recording-studio-brutalist`. Brand: `recording-studio-brandkit`.

## When to use

- A host marketing or brand surface should feel soft, haptic, and expensive
- The brief says Apple-adjacent, quiet luxury, agency polish, or "make it feel costly"
- Soft is opted in. Dummy, gem, and Admin stay rounded unless this chat says otherwise

Do not apply this pack as a global restyle of the kit.

## Direction (not a CSS kit)

Pick one vibe and one layout idea, then map both onto a named Flatpack theme.

### Vibe (pick one)

1. **Ethereal glass** - deep near-black, restrained glow, hairline borders, wide grotesk. Glass only if Flatpack already has a surface token for it. Do not invent `backdrop-filter` kits.
2. **Editorial luxury** - warm cream or espresso, high-contrast display type, faint paper grain only if the theme ships it.
3. **Soft structuralism** - silver or white, bold grotesk, airy floating surfaces, highly diffused shadows.

### Layout (pick one)

1. **Asymmetric bento** - mixed cell sizes, collapse to one column on small viewports
2. **Layered cascade** - stacked elevation, no decorative rotation on touch targets
3. **Editorial split** - large type beside media; stack on small viewports

Variance still follows `recording-studio-taste`. Product jobs stay on `UsesDefaultLayout`.

## What "expensive" means here

- Type does the luxury: display size, tracking, weight. Not Inter, Roboto, or Arial as a default
- Shadows are tinted and soft, never harsh gray `shadow-md` equivalents
- Borders are hairlines or nested theme surfaces, not 1px generic gray on everything
- Motion is Flatpack spring or ease tokens, not linear fades and not GSAP
- Spacing is generous on marketing surfaces (large section padding tokens)
- Icons stay one light, consistent family from the host theme

Banned as cheap tells: generic thick icon sets as the only language, edge-glued sticky bars with no theme, three equal Bootstrap-style columns, instant state changes.

## What would look better

A Soft review still uses the four-part Taste critique. Examples of useful notes:

- "The hero would look better if the title used the theme display size and tracking-tighter, not the section title token."
- "The cards would look better if they used one elevated Flatpack surface instead of a border plus a drop shadow."
- "The primary button would look better if the trailing icon sat in the theme's nested icon slot, not as loose text."

Nested "double-bezel" or island buttons are allowed only when Flatpack has those parts. Otherwise add the token or component first. Do not hand-roll concentric radii in custom CSS.

## Motion

Soft motion is quiet mass: short enter fades, press scale, staggered lists via theme delay tokens. Honor reduced motion. Animate transform and opacity only. No scroll hijack, no magnetic cursor libraries.

## Execution

1. Declare the design read and the Soft vibe / layout pick.
2. Name the host theme. Do not fork CSS.
3. Compose Flatpack. Ask before adding a new component.
4. Return the four-part critique, then implement.

Dummy / gem / Admin remain `data-theme="rounded"` plus `UsesDefaultLayout` unless explicitly opted in.
