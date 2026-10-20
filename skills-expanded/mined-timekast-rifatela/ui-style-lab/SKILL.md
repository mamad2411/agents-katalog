# UI Style Lab

## Purpose

This skill helps select and define a coherent visual style family for a product UI.
It should be used when the task involves choosing or refining a product's aesthetic direction, skin, surface language, visual tone, or premium feel.

## Use This Skill When

- the user wants the app to look more premium
- the UI feels generic or too template-like
- a new app needs a clear visual direction
- the team needs skin recommendations
- the product needs different themes/skins
- the system must decide between executive, editorial, operator, or accent-driven looks

## Do Not Use This Skill For

- low-level React implementation details
- API or backend decisions
- data modeling
- performance profiling
- generic CRUD implementation without visual direction work

## Required Process

When invoked, the skill must:

1. identify the product posture
2. identify trust vs novelty requirements
3. identify density requirements
4. recommend a skin family
5. define surface behavior
6. define typography posture
7. define icon treatment (see § Iconography System)
8. define motion profile (see § Motion Profile)
9. list anti-patterns to avoid

---

## Supported Skin Families

### 1. Midnight Executive

**Intent:** premium, trustworthy, dark-mode-forward interface for finance, admin, analytics, or governance tools.

**Best for:**

- fintech
- admin systems
- dashboards
- investor portals
- internal tools that need polish

**Avoid when:**

- the product should feel playful or warm
- the app is mostly editorial content

**Visual traits:**

- deep navy/charcoal backgrounds
- restrained accents
- layered but subtle surfaces
- strong hierarchy
- premium dark mode
- clean, stable navigation

**Tables:**

- crisp
- dense but legible
- strong row hierarchy
- minimal decorative styling

**Icons:**

- mostly neutral outlines
- accent only in KPI or highlighted surfaces

**Motion:**

- crisp, restrained, premium

---

### 2. Editorial Premium

**Intent:** typography-led, brand-aware, polished composition with less chrome and more character.

**Best for:**

- AI products
- premium content platforms
- founder tools
- high-end B2B landing/dashboard hybrids

**Avoid when:**

- extremely dense operational software dominates the product

**Visual traits:**

- stronger heading presence
- more composition rhythm
- fewer generic cards
- better whitespace discipline
- elegant hierarchy

---

### 3. Dense Operator

**Intent:** high-clarity interface for serious multi-step operational work.

**Best for:**

- ops tools
- logistics
- trading-like UIs
- internal consoles
- monitoring systems

**Avoid when:**

- the product should feel soft, aspirational, or luxurious

**Visual traits:**

- compact surfaces
- strong zoning
- stable shells
- hierarchy through density and grouping
- less decorative styling

---

### 4. Soft Glass Accent

**Intent:** modern premium feel using restrained translucency and elevated overlays as accents, not as the entire system.

**Best for:**

- premium dashboards
- AI apps
- consumer-facing modern products
- command/search-heavy shells

**Avoid when:**

- the interface is highly dense
- accessibility contrast is already fragile

**Rules:**

- do not make every panel glass
- prefer glass on overlays, highlighted widgets, topbars, or command surfaces
- maintain strong contrast and readable boundaries

---

### 5. Warm Productive

**Intent:** human, approachable, calm interface for wellness, education, creator, or family-oriented products.

**Best for:**

- education
- creator tools
- wellness products
- family-focused apps

**Avoid when:**

- the brand must feel highly formal and institutional

---

## Motion Profile

> Defines how the UI moves and responds. Not animation for decoration, but to improve clarity, responsiveness, and premium feel.

### Motion Tone

Choose one per product:

| Tone           | Description                 | Best for                        |
| -------------- | --------------------------- | ------------------------------- |
| **Calm**       | Slow, gentle, breathing     | Wellness, education             |
| **Crisp**      | Fast, snappy, immediate     | Admin, operator tools           |
| **Premium**    | Smooth, deliberate, elegant | Fintech, executive dashboards   |
| **Restrained** | Minimal, functional only    | Dense data tools                |
| **Reduced**    | Near-zero motion            | Accessibility-first, monitoring |

### Interaction Feedback

Define behavior for each state:

- **Hover:** subtle scale, shadow lift, or background shift
- **Pressed:** inward motion (scale down) or color shift
- **Selected:** persistent indicator (underline, fill, ring)
- **Focused:** visible focus ring, meets WCAG
- **Disabled:** reduced opacity, no interaction feedback

### Container Transitions

| Element               | Recommendation                 |
| --------------------- | ------------------------------ |
| Modal                 | Scale + fade from center       |
| Drawer                | Slide from edge                |
| Tooltip               | Fade with slight offset        |
| Page transitions      | Cross-fade or slide (if SPA)   |
| Tab/content switching | Fade or slide within container |

### Data UI Motion Rules

- **Tables:** row highlight on hover, sort animation optional
- **Charts:** staggered entrance on load, tooltip follows cursor
- **KPI cards:** count-up animation on first paint
- **Filters:** smooth height transitions when toggling
- **Empty states:** gentle fade-in

### Reduced Motion Strategy

When `prefers-reduced-motion: reduce` is active:

- remove all decorative transitions
- keep state-change indicators (selected, focus)
- use instant visibility changes instead of animated ones

---

## Iconography System

> Defines how icons should be selected, styled, grouped, and elevated so the UI feels coherent and premium.

### Recommended Library Strategy

Use a tiered approach:

1. **Base System Icons**
   - **Lucide** or Tabler
   - for navigation, actions, utilities, CRUD, settings

2. **Accent / Expressive Icons**
   - **Phosphor** or custom SVG
   - for KPI cards, highlights, marketing surfaces, premium callouts

3. **Brand / Domain Icons**
   - custom SVG for product-specific entities
   - use sparingly and deliberately

### Icon Policy Rules

- Navigation icons should usually remain neutral and consistent
- KPI cards may use richer icon treatment (filled, duotone, gradient container)
- Avoid mixing too many icon families in the same surface
- Use glow and gradients only in accent contexts
- Outline icons are usually safer for system-level navigation
- Filled or duotone icons should be limited to emphasis roles
- If the interface handles money or dense data, preserve trust and precision

### Icon Anti-Patterns

- ❌ random mixing of icon sets
- ❌ inconsistent stroke weights
- ❌ over-glowing every icon
- ❌ decorative icons in dense tables
- ❌ duotone everywhere
- ❌ icons without role distinction

---

## Output Format

Always return:

- chosen skin
- rationale
- visual tone
- surface rules
- typography posture
- icon strategy (base + accent library, allowed styles)
- motion profile (tone + interaction feedback)
- anti-patterns
- optional fallback skin

## Anti-Patterns

- generic "clean SaaS" with no character
- overusing cards until the UI loses hierarchy
- all surfaces at the same depth
- neon accents without strong rationale
- glassmorphism as the full system default
- neumorphism for dense productivity tools
- trendy style choices that weaken trust
