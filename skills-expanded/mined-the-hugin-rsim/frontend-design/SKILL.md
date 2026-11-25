---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Pre-flight: Design System Generation

**Before any aesthetic decision**, run the ui-ux-pro-max design system generator:

```bash
py ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
```

Extract from the user request:
- **Product type**: SaaS, dashboard, landing page, e-commerce, portfolio, etc.
- **Industry**: fintech, healthcare, gaming, beauty, etc.
- **Style keywords**: minimal, playful, dark mode, elegant, etc.

The generator returns: pattern, style, color palette, typography pairing, effects, and anti-patterns to avoid. **Use this as the foundation** — then apply the bold aesthetic direction below to make it distinctive and unforgettable.

To persist the design system across sessions (recommended for multi-page projects):
```bash
py ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

---

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## Server-Side Templates (Jinja2, Django, Flask, FastAPI)

This skill applies equally to server-rendered HTML. When the context is a Jinja2/Django/Flask template:
- Treat `{% block %}` / `{% for %}` / `{{ var }}` as the data layer — design lives in CSS, not in template logic
- Put all design in CSS variables + class-based components in `base.html`
- Keep JS minimal: progressive enhancement only (no SPA patterns)
- Preferred pattern: `base.html` design system → page templates extend it

## Dashboard Pattern

When building admin/monitoring dashboards (KPI + table + detail pages), use this structure:

```
base.html        — CSS variables, nav, global components
├── list page    — KPI row (colored stat cards) + filterable table
├── detail page  — entity card (score/ring/metric-row) + sub-tables
└── stats page   — chart panels (bar charts) + ranking tables
```

**Component vocabulary for dark dashboards:**

| Class | Purpose |
|-------|---------|
| `.kpi` / `.kpi-row` | Stat cards with top color strip |
| `.s-ring` (SVG) | Score ring: `r=13`, circumference=82, `stroke-dasharray="{{dash}} 82"`, `rotate(-90deg)` |
| `.badge-SEVERITY` | Severity pill chips (CRITICAL / HIGH / MEDIUM / LOW) |
| `.sig-col` / `.sig-row` | Horizontal signal bars (width proportional to score%) |
| `.bchart` / `.brow` | Bar chart rows (label + track + fill + stat) |
| `.sec-hdr` | Section header with decorative right-extending line |
| `.panel` / `.panel-hdr` | Surface card with uppercase header |
| `.t-buy` / `.t-sell` | BUY/SELL direction indicators |
| `.res-won` / `.res-lost` | Outcome result indicators (✓/✗) |

**SVG score ring formula:** `dash = floor(score / 100 × 82)`, where 82 = `floor(2π × 13)`. For larger rings scale proportionally: `r=20 → C=126`.