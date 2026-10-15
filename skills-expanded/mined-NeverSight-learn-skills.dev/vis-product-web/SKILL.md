---
name: vis-product-web
description: "Design and build a complete production-grade web experience from project requirements: product analysis, information architecture, UI/UX direction, CSS-variable design system, component architecture, data-driven rendering, theme and state mapping, motion system, responsive layout, accessibility, and runnable HTML/CSS/JavaScript with a built-in self-review gate. Use when generating a full web page, dashboard, landing page, admin console, or product UI at commercial quality instead of a template demo."
---

# Product Web Experience Designer & Builder

Turns raw project requirements into a real, usable, commercially polished web product. The delivery bar is a Production-ready Web Experience, never a running HTML demo.

## Priority Ladder

Resolve every design conflict upward through this ladder:

```text
Product Quality > Visual Tricks
Hierarchy > Decoration
Consistency > Complexity
Usability > Effects
Clarity > Information Density
Purposeful Motion > Decorative Animation
Real Product Feel > AI Generated Feel
```

## Hard Rules

1. **Parameterize everything variable**: names, regions, dates, times, numbers, amounts, units, statuses, categories, titles, descriptions, and metrics stay `[PARAMETER]` placeholders or render from the data layer. Business content never hardcodes into structure.
2. **Derive instead of stalling**: missing colors, fonts, layouts, animation, components, icons, or themes get decided from project type, business goal, target users, scenario, brand position, content structure, and platform. Ask questions only when a missing fact blocks correct implementation.
3. **Recompute per project**: data models, fields, states, components, themes, motion, and visuals derive fresh per project; migrating one project's skeleton into another is out of contract.
4. **Keep layers separate**: Data ≠ UI, Theme ≠ Component, Component ≠ Page.
5. **Stay premium**: cheap gradients, heavy glassmorphism, excess glow, radius, shadows, particles, meaningless decoration, cartoon styling, template feel, and visual noise are design defects.

## Delivery Pipeline

```text
Step 1  Requirement Intake        fill the parameter contract (references/parameter-contract.md)
Step 2  Product Analysis          answer seven ranking questions, build information tiers
Step 3  Information Architecture  choose the layout family that fits the content
Step 4  Design System             tokenize via CSS Variables (references/design-system-reference.md)
Step 5  Component Architecture    independent structure/style/state/interaction/responsive/animation
Step 6  Data Model                DATA -> STATE -> THEME -> COMPONENT -> RENDER -> INTERACTION
Step 7  Theme & State Mapping     statuses and categories become theme classes
Step 8  Motion System             purposeful, CSS-first, reduced-motion aware
Step 9  Responsive & A11y & Perf  recompose for breakpoints; semantic, focusable, fast
Step 10 Implementation            runnable HTML5/CSS3/Vanilla JS/SVG by default
Step 11 Self-Review Gate          audit five lenses, fix findings, deliver (references/self-review-gate.md)
```

### Step 1: Requirement Intake

Extract every parameter group from `[PROJECT_REQUIREMENTS]` using the contract in `references/parameter-contract.md`: project identity, business goal, users and scenarios, platform and device range, data source and content structure, brand and visual direction, palette, typography, components, interaction and motion intensity, responsive rules, tech stack, output format. Unspecified values are inferred, recorded, and applied consistently.

### Step 2: Product Analysis

Answer before writing any code:

1. What is this project ([PROJECT_TYPE])?
2. Who are the users ([TARGET_USER])?
3. What outcome matters most to them ([BUSINESS_GOAL])?
4. Which information is primary and deserves the strongest visual weight?
5. Which information is secondary?
6. Which content can be de-emphasized?
7. What action will users take most often?

The answers define an explicit hierarchy; equal weight for everything is a defect.

### Step 3: Information Architecture

Start from Header, Hero or Overview, Primary Content, Secondary Content, Supporting Content, Utility and Footer, then adjust to reality. Pick the arrangement the content earns: Grid, Flex, Bento Grid, Split Layout, Card Layout, Table, List, Timeline, Kanban, Dashboard, Data Visualization, Map, Gallery, Form, Detail View.

### Step 4: Design System

Build Color, Typography, Spacing, Grid, Radius, Border, Shadow, Elevation, Icon, Motion, Component, State, and Responsive scales as CSS variables first; components reference tokens and never re-declare values. Token menus live in `references/design-system-reference.md`. For numeric products, make core metrics the focal point through size, weight, tabular alignment, units, and trend treatment.

### Step 5: Component Architecture

Identify components from project needs: Header, Navigation, Hero, Search, Filter, Card, List, Table, Chart, Stat, Form, Modal, Tooltip, Empty/Loading/Error states, Footer, and whatever else the domain demands. Every component carries its own Structure, Style, State set, Interaction behavior, Responsive rules, and Animation. Repeated markup renders from data, never through copy-paste HTML.

### Step 6: Data-Driven Rendering

Model content once and render many:

```js
const projectData = [
    {
        id: "[ID]",
        type: "[TYPE]",
        title: "[TITLE]",
        value: "[VALUE]",
        unit: "[UNIT]",
        status: "[STATUS]",
        category: "[CATEGORY]",
        icon: "[ICON]",
        theme: "[THEME]",
        metadata: {}
    }
];
```

Fields adapt to the domain. The runtime chain stays DATA -> STATE -> THEME -> COMPONENT -> RENDER -> INTERACTION.

### Step 7: Theme & State Mapping

Map every real status, category, environment, or mode to a theme class that adjusts accent, surface, gradient, glow, iconography, illustration, or motion while preserving one visual system:

```css
.theme-[STATE] {
    --accent: [STATE_ACCENT];
    --surface: [STATE_SURFACE];
    --glow: [STATE_GLOW];
}
```

Cover the applicable states from default, hover, active, focus, selected, disabled, loading, empty, error, success, warning with unified feedback; skip states the project lacks.

### Step 8: Motion System

Motion serves feedback, hierarchy, state change, navigation, data updates, and atmosphere at Natural, Soft, Responsive, Purposeful, Premium quality. Animate opacity, transform, scale, translate, rotate, filter, blur, gradients, and SVG paths through CSS first; JavaScript orchestrates timing and never runs high-frequency frame loops.

### Step 9: Responsive, Accessibility, Performance

Define desktop, tablet, and mobile breakpoints that recompose grid, spacing, typography, card size, navigation, density, and component arrangement; mobile is an information redesign rather than a shrink. Ship semantic HTML, ARIA where structure needs it, full keyboard paths, visible focus, sufficient contrast, and a `@media (prefers-reduced-motion: reduce)` downgrade for non-essential animation. Favor transform, opacity, CSS animation, SVG, and pseudo-elements over DOM bloat, interval spam, and layout thrash.

### Step 10: Implementation

Default stack: HTML5 + CSS3 + Vanilla JavaScript + SVG, directly runnable with no build step. Small projects may ship one file; larger ones split into index.html, styles.css, app.js plus assets. Add framework, UI kit, icon, or chart libraries only when the project genuinely benefits.

### Step 11: Self-Review Gate

Run the five-lens audit in `references/self-review-gate.md` covering Product, UI, UX, Motion, Engineering. Fix every finding before delivering; the gate decides whether output ships.

---

## Checkable Completion Criteria

- [ ] Zero hardcoded business values; every varying value is a parameter or renders from the data layer.
- [ ] Product analysis produced an explicit hierarchy of primary, secondary, and de-emphasized content.
- [ ] All visual constants route through CSS variables with one authoritative definition each.
- [ ] Components carry independent structure, style, states, interaction, responsive, and animation.
- [ ] Repeated UI blocks render from the unified data model rather than duplicated markup.
- [ ] Real statuses and categories map to themes inside one coherent visual system.
- [ ] Desktop, tablet, and mobile recompose the layout; keyboard, focus, contrast, and reduced-motion handled.
- [ ] Self-review gate completed with findings fixed and zero console errors.
- [ ] Final code runs directly as delivered.
