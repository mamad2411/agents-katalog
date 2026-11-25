---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with strong authored visual identity, token-driven systems, accessibility by default, and zero templated AI tropes.
license: Complete terms in LICENSE.txt
---

# Frontend Design Skill

Create distinctive, production grade frontend interfaces that feel authored by a strong human designer, not averaged from template patterns.

## Success Criteria

- Distinct visual identity with a clear narrative and signature element
- Production grade functionality with complete states and responsive behavior
- Accessibility by default with WCAG AA intent
- Token driven design system rather than one off styling
- Zero reliance on recognizable AI tropes

## Before Writing Code

### 1. Understand the Context

**Purpose**  
What problem does this interface solve and who uses it

**Constraints**  
Framework, performance budget, accessibility requirements

**Brand Anchors if provided**  
Adjectives, references, taboos

If critical information is missing, request only what blocks correct execution.

### 2. Commit to a Radical Art Direction

Pick one extreme and execute it with precision.  
Bold maximalism and refined minimalism both work. Intentionality is mandatory.

Example directions for inspiration only:

- **Editorial magazine**  
  Asymmetric grids, typographic authority, dramatic whitespace
- **Neo brutalist industrial**  
  Hard edges, utilitarian labels, raw materials
- **Luxury refined**  
  Restraint, premium materials, invisible complexity
- **Retro futurist CRT**  
  Scanlines, angular geometry, phosphor glow
- **Organic tactile**  
  Paper grain, irregular shapes, handmade warmth
- **Punk zine rebellion**  
  Collage energy, raw texture, deliberate imperfection
- **Bauhaus precision**  
  Geometric discipline, functional clarity, primary colors
- **Psychedelic surreal**  
  Controlled chaos, vivid contrast, fluid forms

**CRITICAL**  
No two designs should converge on the same choices.  
Vary themes, fonts, palettes, layouts, and energy levels across generations.

### 3. Invent a Signature Element

Every build must include one unforgettable hook that is functional, not decorative.

Valid signature elements include:

- Morphing border or frame responding to scroll or state
- Typographic hero with deliberate kerning and optical rhythm
- Navigation pattern with spatial logic and animated affordances
- Custom cursor behavior that improves discoverability
- Texture system that supports hierarchy and focus
- Branded data visualization language
- Scroll triggered reveal with orchestrated timing

## Design Tokens

Define tokens before layout.

```css
:root {
  /* Color */
  --color-bg:;
  --color-surface:;
  --color-text:;
  --color-muted:;
  --color-accent:;
  --color-focus:;
  --color-success:;
  --color-warning:;
  --color-danger:;

  /* Typography */
  --font-display:;
  --font-body:;
  --font-mono:;
  --text-xs:;
  --leading-xs:;
  --text-sm:;
  --leading-sm:;
  --text-base:;
  --leading-base:;
  --text-lg:;
  --leading-lg:;
  --text-xl:;
  --leading-xl:;
  --text-2xl:;
  --leading-2xl:;

  /* Spacing */
  --space-1:;
  --space-2:;
  --space-3:;
  --space-4:;
  --space-6:;
  --space-8:;

  /* Radius and Shadow */
  --radius-sm:;
  --radius-md:;
  --radius-lg:;
  --shadow-sm:;
  --shadow-md:;
  --shadow-lg:;

  /* Motion */
  --duration-fast:;
  --duration-base:;
  --duration-slow:;
  --ease-out:;
  --ease-spring:;
}
```

## Aesthetics Rules

### Typography

Hard rules:

- Avoid Inter, Roboto, Arial, and system defaults
- Pair a characterful display face with a refined body face
- Tune letter spacing and line height intentionally
- Use typographic contrast as a primary design tool
- Provide robust fallbacks that preserve tone

### Color and Palette

Hard rules:

- No emoticon icons anywhere on the site.
- No default purple gradient on white SaaS aesthetic
- One dominant hue plus one to three accents with defined roles
- Contrast and focus colors must be functional
- Dark mode only if it strengthens the direction

### Layout and Composition

Hard rules:

- No predictable center hero followed by three cards and icon row
- Use consistent grid logic plus at least one intentional grid break
- Asymmetry encouraged when it clarifies hierarchy
- Responsive design must preserve narrative and rhythm

### Motion

Hard rules:

- Motion communicates structure, feedback, and affordances
