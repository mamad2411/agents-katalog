---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
compatibility: opencode
metadata:
  tags: ["frontend", "design", "ui"]
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
---

## The 7 Context Artifacts for Premium Design

AI needs context to produce premium results. These 7 documents form your "design contract":

**What**: Single document explaining what you're building, why, and for whom.
**Purpose**: Gives AI direction and understanding of the project.

```markdown
# Project Brief: [Product Name]

## What We're Building
[Description of the product/website]

## Primary Target Audience
- [Persona 1]: [Description]
- [Persona 2]: [Description]

## Goals
1. [Primary goal - e.g., drive signups]
2. [Secondary goal - e.g., build trust]
3. [Tertiary goal - e.g., explain the product]

## Requirements
- Fully responsive (mobile-first)
- Blazing fast performance
- Accessible (WCAG 2.1 AA)
- [Other requirements]

## Sections
1. Hero
2. Trust Logos
3. Features
4. [etc.]
```

**Key Insight**: Think of AI as a new team member. You wouldn't tell them "build me a website" without context.

---

### 2. Content Files (One Per Section)
**What**: Separate file for each section containing all copy/content.
**Purpose**: Focuses AI on content separately from design.

```markdown
# Hero Section Content

## Headline
[Main headline text]

## Subheadline
[Supporting text]

## CTA Primary
Text: [Button text]
Action: [What happens on click]

## CTA Secondary
Text: [Link text]
Action: [What happens on click]

## Social Proof (optional)
[Trust indicators, stats, etc.]
```

---

### 3. General Vibe Mood Board
**What**: Visual inspiration for the overall site aesthetic.
**Purpose**: Answers "What should the whole site FEEL like when we land on it?"

```markdown
# General Vibe

## Overall Aesthetic
- Theme: [Dark/Light/Mixed]
- Feel: [Modern, Professional, Playful, etc.]
- Color Direction: [Primary color family and why]

## Inspiration References

### Reference 1: [Site Name]
- URL: [link]
- What I Like:
  - [Specific element 1]
  - [Specific element 2]
- Screenshot: [embedded image]

### Reference 2: [Site Name]
- URL: [link]
- What I Like:
  - [Specific element 1]
  - [Specific element 2]
- Screenshot: [embedded image]

## Color Psychology
- Primary Color: [Color] - [Why this color for this audience]
  Example: Turquoise/blue evokes professionalism and trust (important for security products)

## Typography Direction
- Headlines: [Font family, weight, style]
- Body: [Font family, size range]
```

**Research Sources**:
- Dribbble (search "[industry] SaaS landing page")
- Awwwards
- SaaS Landing Page examples
- Competitor sites

---

### 4. Section-Specific Mood Boards
**What**: Detailed specs for each section - the "Frankenstein" approach.
**Purpose**: Gives AI precise visual direction for every section.

```markdown
# Hero Section Specs

## Layout Reference
- URL: [Reference site]
- Screenshot: [embedded]
- What to Copy:
  - Text alignment: [left/center/right]
  - Font hierarchy
  - Button placement

## Navigation Bar
### Components
- Logo: [Position, size]
- Menu Links: [Style, hover effects]
- CTA Button: [Shape, color, glow effects]

### Code Reference (from component library)
```tsx
// Include actual component code from shadcn/21st.dev
```

## Hero Content Area
### Layout
- [Left/Right/Center aligned]
- [Split layout description]

### 3D Element (if applicable)
- Source: [Three.js / Sketchfab link]
- Position: [Where in layout]
- Animation: [Type of movement]
- Code:
```tsx
// Include Three.js or animation code
```

## Components from Libraries
### Primary Button
- Source: 21st.dev
- Style: [pill shaped, glow outline, etc.]
- Code:
```tsx
// Component code
```

### Background Effects
- Type: [Gradient, particles, grid, etc.]
- Source: [Library link]
- Code:
```tsx
// Effect code
```

## Animations
- Scroll Effects: [Parallax, fade-in, etc.]
- Hover States: [What elements animate]
- Entrance Animations: [Staggered, sequential, etc.]
```

**Critical**: Be VERY granular. This is where premium separates from generic.

---

### 5. Style Guide (Living Document)
**What**: Single source of truth for all design specs.
**Purpose**: Ensures consistency across the entire project.

```markdown
# Style Guide

## Design Philosophy
[Brief statement about the visual approach]

## Target Audience
[Who this design serves]

## Color Palette

### Primary
- Main: #[hex] - [Usage: CTAs, key highlights]
- Light: #[hex] - [Usage: hover states]
- Dark: #[hex] - [Usage: pressed states]

### Neutral
- Background: #[hex]
- Surface: #[hex]
- Border: #[hex]
- Text Primary: #[hex]
- Text Secondary: #[hex]

### Accent
- Success: #[hex]
- Warning: #[hex]
- Error: #[hex]

### Do's and Don'ts
DO: [Guidance]
DON'T: [Anti-patterns]

## Typography

### Font Families
- Headlines: [Font name], [fallbacks]
- Body: [Font name], [fallbacks]
- Monospace: [Font name] (for code)

### Scale
- Display: [size]px / [line-height]
- H1: [size]px / [line-height]
- H2: [size]px / [line-height]
- H3: [size]px / [line-height]
- Body: [size]px / [line-height]
- Small: [size]px / [line-height]

## Spacing System
- xs: [value]
- sm: [value]
- md: [value]
- lg: [value]
- xl: [value]
- 2xl: [value]

## Border Radius
- sm: [value]
- md: [value]
- lg: [value]
- full: 9999px

## Shadows
[Shadow definitions]

## Animation
- Duration: [fast/medium/slow values]
- Easing: [easing functions]
- Motion Preferences: Respect prefers-reduced-motion

## Component Patterns
[Common patterns used across the site]
```

**Important**: This is a LIVING document. AI should update it as learnings emerge.

---

### 6. Project Requirements Document (PRD)
**What**: Technical specification for the entire project.
**Purpose**: Tells AI exactly what tech to use and how.

```markdown
# Project Requirements Document

## Project Overview
[Brief description]

## Tech Stack
- Framework: [Next.js / Remix / etc.]
- Styling: [Tailwind CSS / CSS Modules / etc.]
- UI Components: [shadcn/ui, Radix, etc.]
- Animation: [Framer Motion / GSAP / etc.]
- 3D: [Three.js / React Three Fiber]
- Icons: [Lucide / Heroicons / etc.]

## Dependencies
```json
{
  "dependencies": {
    // List all required packages
  }
}
```

## File Structure
```
src/
├── app/
│   └── page.tsx
├── components/
│   ├── ui/           # shadcn components
│   ├── sections/     # Page sections
│   └── 3d/           # Three.js components
├── lib/
│   └── utils.ts
└── styles/
    └── globals.css
```

## Design System
- See: style-guide.md

## Page Sections
| Section | Spec File | Priority |
|---------|-----------|----------|
| Hero | hero-section.md | P0 |
| Features | features-section.md | P1 |
| [etc.] | [etc.] | [etc.] |

## Responsiveness
- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px+

## Performance Requirements
- LCP: < 2.5s
- FID: < 100ms
- CLS: < 0.1

## Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support
```

---

### 7. Tasks Document
**What**: Step-by-step implementation plan.
**Purpose**: Gives AI a clear execution path.

```markdown
# Implementation Tasks

## Phase 1: Project Setup
- [ ] Initialize Next.js project
- [ ] Install dependencies
- [ ] Configure Tailwind CSS
- [ ] Set up shadcn/ui
- [ ] Create folder structure
- [ ] Configure fonts
- [ ] Set up color variables

## Phase 2: Core Components
- [ ] Build navigation bar
- [ ] Create button variants
- [ ] Set up typography components
- [ ] Create layout components

## Phase 3: Section Building
- [ ] Build Hero section
- [ ] Build Trust Logos section
- [ ] Build Features section
- [ ] [Continue for each section]

## Phase 4: Polish
- [ ] Add animations
- [ ] Optimize images
- [ ] Add loading states
- [ ] Mobile responsiveness pass
- [ ] Accessibility audit

## Phase 5: Launch
- [ ] Performance optimization
- [ ] SEO metadata
- [ ] Final review
```

---

## Component Resources

### shadcn/ui
The foundational component library. Copy-paste components with full customization.
- Website: https://ui.shadcn.com
- Usage: Base components (buttons, inputs, cards, etc.)

### 21st.dev
Premium components built on top of shadcn/ui.
- Website: https://21st.dev
- Usage: Advanced components with animations
- **Key Feature**: Each component includes preview, code, and AI prompt for installation

### Three.js / React Three Fiber
3D graphics in the browser.
- Three.js Examples: https://threejs.org/examples/
- Usage: Hero 3D elements, interactive backgrounds

### Sketchfab
Community 3D models and animations.
- Website: https://sketchfab.com
- Usage: Download 3D assets for hero sections

---

## Premium Design Best Practices

### Section Isolation
Build each section independently with its own component and styles. This prevents conflicts and allows AI to focus on one piece at a time without breaking others.

### Screenshot-to-Iteration Workflow
After building each section:
1. Take screenshot
2. Compare to mood board
3. List specific differences
4. Fix differences
5. Repeat until match

This systematic comparison catches subtle details AI might miss.

### Auto-Update Style Guide
As you build, update the style guide with:
- New color values discovered
- Spacing patterns that emerge
- Component variants created
- Animation timings that work

The style guide is a LIVING document that grows with the project.

