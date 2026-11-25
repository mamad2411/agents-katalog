---
name: frontend-design
description: >
  Frontend design standards and aesthetic guidelines. Provides grading criteria
  for visual design quality, originality, craft, and functionality. Referenced by
  the planner and frontend evaluator. Not directly user-invocable.
user-invocable: false
---

# Frontend Design Standards

This skill provides the design evaluation criteria and aesthetic guidelines used by the ganvil planner and frontend evaluator. It encodes design principles that turn subjective judgments like "is this design good?" into concrete, gradable terms.

## Design Thinking Framework

Before making any design decision, understand:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Commit to a BOLD aesthetic direction. Options include (but are not limited to): brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian. Choose one and execute it with precision.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity.

## Design Reference Library

For inspiration and calibration, reference real-world design systems from the [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) collection. Each entry represents a standout design identity:

### High-Caliber Design References (by domain)

| Domain | Reference | Design Character | Why It's Exceptional |
|--------|-----------|-----------------|---------------------|
| Dev Tools | **Linear** | Ultra-minimal, precise, purple accent | Every pixel is intentional. Spacing, typography, and color serve function and mood equally |
| Dev Tools | **Vercel** | Black/white precision, Geist font | Radical restraint used as a design weapon. Nothing extra, nothing missing |
| Fintech | **Stripe** | Purple gradients, weight-300 elegance | Signature gradient meshes create depth and warmth. Typography is light yet legible |
| Fintech | **Revolut** | Sleek dark interface, gradient cards | Premium dark surfaces with vibrant card accents create financial confidence |
| E-commerce | **Shopify** | Dark cinematic, neon green accent | Full-bleed photography, ultra-light display type, unexpected for e-commerce |
| E-commerce | **Airbnb** | Warm coral accent, rounded UI | Photography-driven design with consistently warm, inviting palette |
| Consumer | **Apple** | Premium white space, cinematic imagery | SF Pro font system, dramatic full-viewport product shots |
| Consumer | **Spotify** | Vibrant green on dark, bold type | Album-art-driven layouts that feel alive and dynamic |
| Creative | **Framer** | Bold black/blue, motion-first | Design itself IS the content — every transition and animation communicates |
| Creative | **Figma** | Vibrant multi-color, playful-professional | Rainbow palette that somehow stays cohesive through deliberate constraining |
| Editorial | **The Verge** | Acid-mint, ultraviolet accents | Custom Manuka display type, deliberately jarring and memorable |
| Automotive | **Tesla** | Radical subtraction, cinematic photography | Universal Sans, near-empty black/white canvas, product is the hero |

Use these as comparison anchors when evaluating or generating designs. Ask: "Does this design have the intentionality of Linear? The warmth of Airbnb? The boldness of The Verge?"

## Aesthetic Guidelines

### Typography
Choose fonts that are beautiful, unique, and interesting. **Avoid** generic fonts like Arial, Inter, Roboto, and system fonts. Opt for distinctive choices that elevate the design: unexpected, characterful font choices. Pair a distinctive display font with a refined body font.

### Color & Theme
Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Every color choice should reinforce the chosen tone.

### Motion & Animation
Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.

### Spatial Composition
Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density. The layout itself should be a design decision, not a default.

### Backgrounds & Visual Details
Create atmosphere and depth rather than defaulting to solid colors. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

## Anti-Patterns: What to NEVER Do

The following are telltale signs of generic AI-generated design ("AI slop") and must be actively avoided:

- **Overused fonts**: Inter, Roboto, Arial, system-ui
- **Cliché color schemes**: Purple gradients on white backgrounds, generic blue buttons
- **Template layouts**: Standard card grids, Bootstrap-default spacing, identical shadow depths
- **Stock patterns**: Unmodified component library defaults, generic hero sections
- **Predictable choices**: Every generation converging on the same "safe" look

## Four-Dimension Evaluation Criteria

### 1. Design Quality (Weight: HIGH)
Does the design feel like a coherent whole rather than a collection of parts? Strong work means the colors, typography, layout, imagery, and details combine to create a distinct mood and identity.

Scoring:
- **9-10**: Museum quality. A human designer would be impressed.
- **7-8**: Noticeably polished with clear aesthetic direction.
- **5-6**: Acceptable but unremarkable.
- **3-4**: Disjointed components from different design systems.
- **1-2**: Broken or ugly.

### 2. Originality (Weight: HIGH)
Is there evidence of custom design decisions, or is this templates, library defaults, and AI-generated patterns? A human designer should recognize deliberate creative choices. Unmodified stock components or telltale AI patterns fail here.

Scoring:
- **9-10**: Unique and memorable throughout.
- **7-8**: Several distinctive choices, minor generic elements.
- **5-6**: Mix of custom and generic.
- **3-4**: Mostly defaults, AI patterns evident.
- **1-2**: Pure template with zero customization.

### 3. Craft (Weight: STANDARD)
Technical execution: typography hierarchy, spacing consistency, color harmony, contrast ratios, animation smoothness and purpose. This is a competence check. Most competent implementations score 6-8 by default; below 5 means broken fundamentals.

### 4. Functionality (Weight: STANDARD)
Usability independent of aesthetics. Can users understand what the interface does, find primary actions, and complete tasks without guessing? Are error states handled?

## Calibration Examples

Use these examples to anchor your scoring. Re-read them before every evaluation round to prevent score drift.

### Example A: Generic Task Manager (FAIL)
**Scores: DQ=4, OG=3, CR=6, FN=7**

What the evaluator observed:
- White background, Bootstrap-like card grid with equal padding on all sides
- Purple gradient header bar → classic AI slop pattern
- Inter font at system-default sizes, no typographic hierarchy variance
- Card shadows all identical depth, no visual differentiation between card types
- Button styles are default Tailwind `bg-blue-500 hover:bg-blue-600`
- Form inputs use browser-default focus rings
- Functionally complete: CRUD works, navigation is clear, form validation responds

Score rationale:
- **DQ=4**: Components feel assembled from different sources. The purple header clashes with the blue buttons. No cohesive mood.
- **OG=3**: Every element screams "AI-generated default". A human designer would immediately spot the template origins. Zero custom decisions.
- **CR=6**: Spacing IS consistent and contrast ratios pass WCAG. The fundamentals work — this is pure technical competence without artistry.
- **FN=7**: All features work. Users can complete tasks. Error messages appear on invalid input. Navigation is intuitive.

### Example B: Portfolio Site with Editorial Aesthetic (PASS)
**Scores: DQ=8, OG=8, CR=7, FN=7**

What the evaluator observed:
- Dark charcoal (#1a1a1a) base with cream (#f5f0eb) text, warm amber (#d4a574) accents
- Custom Newsreader serif for headings paired with Karla for body text — distinctive and intentional
- Asymmetric two-column layout: narrow text column (40%) with full-bleed image column (60%)
- Hover effects: images desaturate on mouseout, saturate + subtle scale on hover
- Navigation is a vertical left-edge stack with 90-degree rotated text labels
- Page transitions use CSS `clip-path` reveal animations, staggered by 80ms
- One issue: mobile layout collapses the asymmetry into a generic single-column stack

Score rationale:
- **DQ=8**: Clear "editorial photography" mood executed consistently. Color palette, typography, and layout all support the same identity. Deducted from 9 because the mobile layout loses the aesthetic coherence.
- **OG=8**: Multiple standout decisions: rotated navigation, asymmetric columns, desaturation hover effect. These aren't template defaults — they're deliberate creative choices. Minor: footer uses a generic three-column grid.
- **CR=7**: Typography hierarchy works well at desktop. Spacing is generous and intentional. The clip-path animations are smooth. Deducted: some body text line-heights are too tight at smaller sizes.
- **FN=7**: Portfolio items are browsable, filtering works, contact form submits. The rotated navigation is learnable but not immediately obvious to first-time users.

### Example C: 3D Art Gallery Experience (EXCEPTIONAL)
**Scores: DQ=9, OG=10, CR=8, FN=6**

> ⚠️ **Example C is a *design* ceiling, not a *product* ceiling.** It anchors Originality/Craft. A real app with C's functional gaps (FN=6: no keyboard nav, awkward scrolling, non-intuitive doorways) would now **FAIL on Functional Completeness** under the closed-loop standard — a persistence break or broken core loop is a hard veto regardless of how striking the visuals are. High DQ/OG cannot buy off a broken loop; see the frontend-evaluator's FuncComp calibration.

What the evaluator observed:
- CSS 3D perspective room with checkered marble floor rendered via CSS gradients
- Artwork "hung" on walls using absolute positioning with transform: perspective()
- Navigation between gallery rooms via doorway-shaped click targets
- Dramatic lighting: CSS `radial-gradient` spotlights on each artwork piece
- Custom cursor changes to a pointing hand near artwork, a walking figure in corridors
- Sound icon in corner (non-functional — visual element only)
- Completely breaks the expected "gallery website" mold

Score rationale:
- **DQ=9**: The spatial experience IS the design. Every visual choice serves the gallery metaphor. The marble floor, spotlight gradients, and doorway navigation create genuine atmosphere. Almost 10, but some texture rendering is rough at high DPI.
- **OG=10**: Nobody expects a 3D room built in CSS. This is the kind of creative leap that makes you want to show it to someone. Every design decision is a surprise that works in context.
- **CR=8**: The CSS perspective math is correct, animations are smooth, gradients render cleanly. The checkered floor pattern has some aliasing artifacts. Cursor changes work.
- **FN=6**: Navigation works but isn't immediately intuitive. First-time users might not realize doorways are clickable. Artwork detail view requires awkward scrolling within the 3D space. No keyboard navigation support.

### Example D: Beautiful but Hollow — Kanban that loses data on refresh (FAIL)
**Scores: DQ=8, OG=7, CR=7, UX=7 — but Functional Completeness = 3 → FAIL**

The visual antithesis of Example C's lesson: this one looks *almost* shippable, which is exactly why it's dangerous.

What the evaluator observed:
- A Kanban board with crisp column layout, tasteful card shadows, a coherent muted palette — genuinely polished surface (DQ=8)
- Drag-and-drop is visually smooth; cards animate between columns with a satisfying spring (UX=7)
- Create-card and edit-card modals work, validation messages appear on empty input
- **But on a hard refresh, every card snaps back to its initial position — the board state was never persisted.** Drag/create/edit were optimistic-only updates against in-memory state; no localStorage, no API round-trip.

Score rationale:
- **DQ/OG/CR/UX all pass their thresholds** — the surface really is well-crafted.
- **FuncComp=3**: the persistence stage (4) of every P0 feature is `🔗` (fake closed loop). Anti-inflation rule fires: *any P0 feature with persistence 🔗 → FuncComp ≤ 4.*
- **Verdict: FAIL.** Aesthetics cannot buy off a broken core loop. The generator's correct response is **Wire** (connect a persistence layer, remove the optimistic-only fakery) — **not** a visual Pivot.

> **The contrast that matters**: Example C scores FN=6 yet anchors the *design* ceiling — its gaps are usability rough edges, not fake loops. Example D scores DQ=8 yet **FAILS** — because a hollow persistence loop is a hard veto. Pretty ≠ done. See the frontend-evaluator's Feature Loop Matrix + FuncComp calibration for the scoring mechanics.

### How to Use These Examples

1. **Before scoring**: Re-read Example A (the floor) and Example C (the ceiling) to reset your internal scale
2. **When uncertain about Design Quality**: Ask "Is this closer to Example A's assembled-from-parts feel, or Example B's cohesive editorial mood?"
3. **When uncertain about Originality**: Ask "Would a human designer recognize deliberate choices here, like in Example C? Or would they say 'I've seen this exact output from ChatGPT' like Example A?"
4. **Guard against inflation**: Example A's DQ=4 is for something that technically works and doesn't look broken. A 7 must be actively polished, like Example B. Reserve 9+ for genuine creative leaps like Example C.
5. **Don't let a polished surface buy off a broken loop** (Example D): any P0 feature whose persistence stage is `🔗` (optimistic-only / mocked / hardcoded) caps **Functional Completeness ≤ 4** and FAILs the sprint — regardless of how high DQ/OG/Craft score. Pretty is not done.

## How Planner Should Use This

When creating the visual design language section of a product spec:
1. Choose a bold aesthetic direction from the tone options above
2. Reference a specific design from the Design Reference Library as an inspiration anchor (e.g., "Aim for Linear's spatial precision with Spotify's bold color energy")
3. Specify exact font choices, color palette, spacing philosophy
4. Define animation approach and interaction patterns
5. Include anti-patterns to avoid
6. Set the bar high — the best designs are museum quality

## How Frontend Evaluator Should Use This

When scoring design quality and originality:
1. **Re-read the Calibration Examples** before every scoring session to reset your scale
2. Compare against the anti-patterns list — any match reduces the score
3. Compare against the Design Reference Library — the best designs approach this level of intentionality
4. Look for intentional design decisions vs. defaults
5. Check if the design feels cohesive or assembled from parts
6. Weight design quality and originality more heavily than craft and functionality
7. Be skeptical — LLMs naturally want to praise LLM output
