---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, Svelte, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Components & primitives

**Reach for shadcn primitives before hand-rolling UI.** If a project has `components.json`, the design system is already wired up: tokens, CSS variables, accessible primitives, an icon library. Compose from those building blocks instead of recreating them — you inherit a11y, keyboard handling, focus management, and theme integration for free.

**Detect the setup before writing UI.** Read `components.json` and glance at the existing `components/ui/` folder so you know what's already installed and what's available to add. Add missing pieces through the registry CLI rather than re-implementing them.

**Customise through the `class` prop, not by forking.** Override colour, spacing, radius, and typography from the caller. Leave the primitive untouched so future upgrades apply cleanly. Only edit the primitive itself for a structural change — and prefer adding a variant to rewriting the existing one.

**Compose primitives into small feature components — one job each.** Don't reach for a primitive when none is needed; a `<div>` with two utility classes is fine.

**Hand-roll only when no primitive fits.** Bespoke visualisations (canvas, SVG graphs/trees/charts) or structural shapes the primitive can't express. Even then, lean on the design tokens and Tailwind utilities so the custom piece reads as part of the same system.

**Tokens over magic numbers.** Use the design-system CSS variables and the configured Tailwind theme. If you need a new colour or scale step, add it to the token layer once and reuse it — don't sprinkle hex values across components.

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Pair a distinctive display font with a refined body font. If a shadcn project already ships Inter/system fonts, layer a characterful display face for headings rather than fighting the default — intentional pairings beat a wholesale replacement of an established token.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency, and lean on the shadcn token layer (`--primary`, `--accent`, `--muted`, `--destructive`) so dark/light modes work for free. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available; in Svelte use the built-in transitions or `motion`. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER ship generic AI-generated aesthetics: lazy default font stacks unchanged from the framework starter (Inter/Roboto/Arial with no display face), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Using Inter as a body font *with intent* — paired with a distinctive display face, tuned weights, and a confident palette — is fine; using it because it's the default is not.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## Implementation

Always use data-testid attributes to identify elements in automated tests.
Prefer the use of Shadcn primitives over hand-rolling UI.