---
name: impeccable-design
description: "Create distinctive, production-grade frontend interfaces with high design quality. Generates creative, polished code that avoids generic AI aesthetics. Use when the user asks to build web components, pages, artifacts, or applications, or when any design skill requires project context."
user-invocable: true
argument-hint: "[component or page to design]"
license: Apache 2.0. Based on pbakaus/impeccable frontend-design skill. Original based on Anthropic's frontend-design skill. See pbakaus/impeccable NOTICE.md for attribution.
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Context Gathering Protocol

Design skills produce generic output without project context. You MUST have confirmed design context before doing any design work.

**Required context** — every design task needs at minimum:
- **Target audience**: Who uses this product and in what context?
- **Use cases**: What jobs are they trying to get done?
- **Brand personality/tone**: How should the interface feel?

**CRITICAL**: You cannot infer this context by reading the codebase. Code tells you what was built, not who it's for or what it should feel like. Only the creator can provide this context.

**Gathering order:**
1. **Check current instructions (instant)**: If your loaded instructions already contain a **Design Context** section, proceed immediately.
2. **Check .impeccable.md (fast)**: If not in instructions, read `.impeccable.md` from the project root. If it exists and contains the required context, proceed.
3. **Ask the user (REQUIRED)**: If neither source has context, ask the user directly for target audience, use cases, and brand personality before doing anything else.

---

## Design Direction

Commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work—the key is intentionality, not intensity.

Then implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

### Typography
Choose fonts that are beautiful, unique, and interesting. Pair a distinctive display font with a refined body font.

**DO**: Use a modular type scale with fluid sizing (clamp)
**DO**: Vary font weights and sizes to create clear visual hierarchy
**NEVER**: Inter, Roboto, Arial, Open Sans, system defaults
**NEVER**: Monospace typography as lazy shorthand for "technical/developer" vibes
**NEVER**: Large icons with rounded corners above every heading

### Color & Theme
Commit to a cohesive palette. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

**DO**: Use modern CSS color functions (oklch, color-mix, light-dark) for perceptually uniform palettes
**DO**: Tint your neutrals toward your brand hue
**NEVER**: Gray text on colored backgrounds — use a shade of the background color instead
**NEVER**: Pure black (#000) or pure white (#fff) — always tint
**NEVER (The AI Color Palette)**: cyan-on-dark, purple-to-blue gradients, neon accents on dark backgrounds
**NEVER**: Gradient text on metrics or headings
**NEVER**: Default to dark mode with glowing accents

### Layout & Space
Create visual rhythm through varied spacing — not the same padding everywhere.

**DO**: Create visual rhythm through varied spacing — tight groupings, generous separations
**DO**: Use fluid spacing with clamp() that breathes on larger screens
**DO**: Use asymmetry and unexpected compositions; break the grid intentionally for emphasis
**NEVER**: Wrap everything in cards
**NEVER**: Nest cards inside cards
**NEVER**: Use identical card grids — same-sized cards with icon + heading + text, repeated endlessly
**NEVER**: Use the hero metric layout template — big number, small label, supporting stats, gradient accent
**NEVER**: Center everything

### Visual Details
**NEVER**: Glassmorphism everywhere — blur effects, glass cards, glow borders used decoratively
**NEVER**: Rounded elements with thick colored border on one side
**NEVER**: Sparklines as decoration
**NEVER**: Rounded rectangles with generic drop shadows
**NEVER**: Modals unless truly no better alternative

### Motion
Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions.

**DO**: Use motion to convey state changes — entrances, exits, feedback
**DO**: Use exponential easing (ease-out-quart/quint/expo) for natural deceleration
**DO**: For height animations, use grid-template-rows transitions
**NEVER**: Animate layout properties (width, height, padding, margin) — use transform and opacity only
**NEVER**: Bounce or elastic easing

### Interaction
**DO**: Use progressive disclosure — start simple, reveal sophistication through interaction
**DO**: Design empty states that teach the interface
**DO**: Make every interactive surface feel intentional and responsive
**NEVER**: Repeat the same information
**NEVER**: Make every button primary

### Responsive
**DO**: Use container queries (@container) for component-level responsiveness
**DO**: Adapt the interface for different contexts — don't just shrink it
**NEVER**: Hide critical functionality on mobile

---

## The AI Slop Test

**Critical quality check**: If you showed this interface to someone and said "AI made this," would they believe you immediately? If yes, that's the problem.

A distinctive interface should make someone ask "how was this made?" not "which AI made this?"

---

## Implementation Principles

Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations. Minimalist designs need restraint, precision, careful attention to spacing and subtle details.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics.

Claude is capable of extraordinary creative work. Don't hold back — show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
