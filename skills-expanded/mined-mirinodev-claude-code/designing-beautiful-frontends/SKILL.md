---
name: designing-beautiful-frontends
description: Create distinctive, production-grade frontend interfaces with high
  design quality that avoid generic AI aesthetics. Adapt to ANY aesthetic direction
  the user provides. Use when building web components, pages, or applications
  (websites, landing pages, dashboards, components, HTML/CSS layouts, or when
  styling/beautifying any web UI). Use when the user mentions UI/UX design,
  beautiful UI, frontend design, component creation, cool UI, impressive design,
  or Japanese equivalents like UI/UXデザイン/美しいUI/フロントエンドデザイン/
  コンポーネント作成/かっこいいUI/印象的なデザイン.
---

# Designing Beautiful Frontends

## Contents

- Source and attribution
- Why AI-generated UIs look the same
- Design thinking workflow
- Frontend aesthetics guidelines
- Anti-convergence rules
- Recommended tech stack
- Reference files
- The most important principle

## Source and Attribution

This skill is based on the design philosophy from:
- [Improving frontend design through Skills](https://claude.com/blog/improving-frontend-design-through-skills) (Official Anthropic blog)
- [anthropics/skills/frontend-design](https://github.com/anthropics/skills) (Official Skills repository)

## Why AI-Generated UIs Look the Same

Language models suffer from **distributional convergence**: they default to patterns that dominate training data. Without intervention, Claude gravitates toward Inter/Roboto fonts, purple gradients on white backgrounds, predictable hero-features-CTA layouts, and minimal animations. The result is "AI slop" — interfaces that are technically correct but visually indistinguishable from each other.

This skill exists to break that pattern. Every design decision must be intentional and context-specific, not a safe default.

## Design Thinking Workflow

### Step 1: Understand the Context

Before writing any CSS or markup, gather context about the project. If the user has already provided clear direction (aesthetic, brand, constraints), proceed directly. Otherwise, use `AskUserQuestion` to clarify:

- **Purpose**: What problem does this interface solve? Who is the audience?
- **Tone**: What feeling should it evoke? (e.g., playful, authoritative, warm, cutting-edge, luxurious, raw)
- **Constraints**: Technical requirements, browser support, performance budget, existing design system?
- **Differentiation**: What should make this UI memorable and distinct?

Example question structure:
```
Questions to ask:
1. "What aesthetic direction fits this project?" — Offer 3-4 *diverse* directions as examples (not a fixed list), tailored to the project context
2. "Are there reference sites or styles you admire?"
3. "Any technical constraints I should know about?"
```

### Step 2: Choose an Aesthetic Direction

**Do NOT pick from a fixed menu.** The space of possible aesthetics is infinite. Instead, think about extremes along multiple axes:

- **Density**: Sparse minimalism ... dense maximalism
- **Formality**: Corporate polish ... raw brutalism
- **Era**: Retro nostalgia ... bleeding-edge futurism
- **Warmth**: Cold geometric precision ... organic hand-crafted warmth
- **Color intensity**: Monochrome restraint ... chromatic explosion

Pick a strong position. **The middle is the worst place to be.** Bland, uncommitted design is the hallmark of AI slop.

When suggesting directions to the user, generate options that are **specific to their project context**, not recycled presets.

### Step 3: Implement with Full Commitment

Once a direction is chosen, commit fully. Every implementation detail — font choice, color, spacing, animation, texture — must reinforce the chosen aesthetic vision.

**Adjust implementation complexity to match the aesthetic vision.** A brutalist one-page site needs different techniques than a rich editorial experience. Do not over-engineer simple aesthetics or under-deliver complex ones.

## Frontend Aesthetics Guidelines

### Typography

#### Fonts to AVOID (convergence traps)
- Inter, Roboto, Arial, Helvetica, Open Sans, Lato, system-ui
- These are not bad fonts — they are overused defaults that signal "no design thought"

#### Font Selection Principles
- **Choose fonts that reinforce the aesthetic direction** — there is no universal "good" font list
- Every project should use different typography. If you used a font recently, pick a different one
- Pair fonts with extreme contrast: display + monospace, serif + geometric sans
- Weight contrast: 100/200 vs 800/900 (not 400 vs 600)
- Size jumps: 3x+ between hierarchy levels (not 1.5x)
- Use Google Fonts or Fontsource for access to distinctive typefaces

#### NEVER Converge on Familiar Alternatives
Even with instructions to avoid defaults, there is a tendency to fall back on the same "alternative" fonts repeatedly. **Do not always reach for the same replacements.** Vary deliberately every time.

### Color and Theme

#### Principles
- **Dominant color + sharp accent** outperforms timid, evenly-distributed palettes
- Use CSS custom properties (`--color-*`) for systematic theming
- Draw inspiration from unexpected sources: IDE themes, cultural aesthetics, nature, architecture, film, fashion

#### Palette Construction Thinking
- Start from the aesthetic direction, not from a color picker
- Ask: "What colors would this aesthetic naturally live in?"
- Consider: What cultural or emotional associations do these colors carry?
- Ensure sufficient contrast ratios for accessibility (WCAG AA minimum)

#### Combinations to AVOID
- Purple gradient + white background (generic SaaS)
- Blue + gray only (corporate template)
- Bootstrap/Material default colors
- Any palette you have used in a recent project

### Motion and Animation

#### Priority Order
1. **CSS-only animations** (performance first)
2. **Motion library** (for complex orchestration in React/Vue/JS)

#### High-Impact Moments
Focus animation budget on moments that matter most:
- Page load: staggered reveal animations (animation-delay)
- Hover: surprising micro-interactions
- Scroll-triggered transitions
- State changes and transitions

One well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions everywhere.

#### Always include `prefers-reduced-motion` media query handling.

### Spatial Composition

#### Layout Principles
- **Embrace unexpected layouts** — break the template
- Asymmetry, overlapping elements, diagonal flow
- Strategically place **grid-breaking elements**
- Generous negative space OR controlled density (pick one, commit)

#### Layout to AVOID
- Header → Hero → 3-column features → CTA → Footer (the template layout)
- Perfectly symmetrical, evenly-spaced card grids
- Any layout that looks like a Bootstrap/Tailwind template

### Backgrounds and Visual Details

Never use plain solid backgrounds as the default. Consider:
- Gradient meshes
- Noise textures / grain overlays
- Geometric patterns
- Layered transparency
- Dramatic shadows
- Decorative borders
- Custom cursors (where appropriate)

## Anti-Convergence Rules

These are the most critical rules in this skill:

1. **No two designs should look the same.** Every project gets a unique visual identity
2. **Use different fonts every time.** Never default to the same "safe alternative"
3. **Use different color palettes every time.** Never recycle a previous palette
4. **Vary layouts across projects.** If the last project used asymmetric grids, try something different
5. **Question every "default" choice.** If a decision feels automatic, it is probably convergent

### Self-Check During Implementation

Before finalizing any design, ask yourself:
- "Would a human designer make this exact same combination of choices?"
- "Could someone tell this was AI-generated by looking at it?"
- "Have I used any of these fonts/colors/patterns in a recent project?"
- "Is there anything surprising or distinctive about this design?"

If the answer to any of these raises concern, revise.

For detailed anti-convergence thinking patterns, see [references/anti-convergence-patterns.md](references/anti-convergence-patterns.md).

## Recommended Tech Stack

Default recommendations (confirm with user via `AskUserQuestion` if project setup is unclear):

- **React 19** + **TypeScript**
- **Next.js 16** (App Router, Turbopack, React Compiler)
- **Tailwind CSS v4** + **shadcn/ui**
- **Motion** (formerly Framer Motion, for animations)
- **Google Fonts** or **Fontsource**

If the user is working with an existing project, adapt to their stack. Do not assume or impose a stack without confirmation.

## Reference Files

Consult these when you need deeper guidance:

| File | When to read |
|------|-------------|
| [references/design-system-guide.md](references/design-system-guide.md) | When building a complete design system or need detailed typography/color/motion/spatial principles |
| [references/anti-convergence-patterns.md](references/anti-convergence-patterns.md) | When you catch yourself making "default" choices, or need thinking frameworks to break convergence |
| [references/implementation-checklist.md](references/implementation-checklist.md) | Before delivering any UI implementation — run through the quality checklist |

## The Most Important Principle

**Claude is capable of extraordinary creative work. Do not self-censor or play it safe.**

Bold maximalism and refined minimalism are both valid — what matters is **intentional execution with full commitment**, not intensity. Every design should be a deliberate creative statement, never a safe default.

**No two projects should ever look the same.**
