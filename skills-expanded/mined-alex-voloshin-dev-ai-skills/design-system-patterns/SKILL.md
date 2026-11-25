---
name: design-system-patterns
description: Use this skill when designing UI, defining or auditing a design system, reviewing UX deliverables, specifying components, evaluating accessibility, or producing redlines and tokens for engineering handoff — the UI/UX knowledge base covering user research, personas, jobs-to-be-done, user journeys, usability testing, information architecture, wireframing, prototyping, visual design, typography, color theory, grid systems, visual hierarchy, micro-interactions, animation, design systems, atomic design, design tokens, Figma workflows, WCAG 2.2 accessibility, responsive and mobile-first design, Material Design 3, Apple HIG, Nielsen heuristics, Gestalt principles, conversion-centered design, and design-to-code handoff.
disable-model-invocation: true
---

# Design System Patterns

Human-centered design knowledge: user research, IA, visual + interaction design, design systems, accessibility, responsive behavior, platform guidelines, and design-to-code handoff. Combines cognitive psychology (Gestalt, Nielsen heuristics) with platform conventions (Material 3, Apple HIG) to produce accessible, conversion-optimized interfaces. Use this knowledge when applying the `ui-ux-designer` role or any workflow that needs UX rigor.

## User Research

Design Thinking phases: Empathize → Define → Ideate → Prototype → Test.

### Personas + Jobs-to-Be-Done
- **Personas**: evidence-based, not invented. Capture goals, frustrations, context, technical proficiency.
- **JTBD**: frame features as the job a user hires the product to do. Reduces feature inventory bias.

### User Journeys
End-to-end touchpoints with emotions, pain points, and opportunities mapped per stage. Reveals friction invisible at the single-screen level.

### Research Methods
Interviews, contextual inquiry, card sorting, tree testing, surveys, A/B testing, heatmaps. Choose by question: discovery (interviews), structure (card sort), validation (A/B).

### Usability Testing
Task-based, think-aloud protocol. 5 users surface ~85% of issues (Nielsen). Test on real devices, not desktop simulations.

## Information Architecture

- **Content hierarchy**: most important first. Progressive disclosure for complexity.
- **Navigation**: global, local, breadcrumbs, contextual. Cap top-level items at 7±2.
- **Mental models**: match user expectations, not org chart. Validate via card sorting.
- **Wayfinding**: user always knows where they are, where they can go, how to return.
- **Search**: prominent on content-heavy sites; autocomplete + filters + facets.
- **Scan patterns**: F-pattern for text-heavy pages; Z-pattern for landing pages.

## Visual Design

### Typography
- Maximum 2 typefaces per system.
- Type scale ratio 1.2–1.5 (modular scale).
- Line height 1.4–1.6 for body text.
- Line length 45–75 characters for readability.

### Color
- 60-30-10 rule (dominant / secondary / accent).
- Semantic status colors (success, warning, error, info) mapped to primitive tokens.
- WCAG contrast: 4.5:1 body text, 3:1 large text + UI components.
- Never use color alone to convey meaning — pair with icon, text, or pattern.
- Dark mode: semantic tokens decouple light/dark from component code.

### Grid + Layout
- 4px or 8px base unit.
- 12-column grid for desktop.
- Consistent gutters per breakpoint.
- Whitespace is functional — generous spacing improves readability and trust.

### Visual Hierarchy
Establish importance order via size, color, contrast, spacing, position, typography weight. Apply Gestalt principles:
- **Proximity**: grouped items perceived as related.
- **Similarity**: consistent styling implies consistent function.
- **Continuity**: aligned elements scan as a flow.
- **Closure**: implied shapes complete in perception.
- **Figure-ground**: foreground vs background separation drives focus.
- **Common region**: containers (cards, boxes) group implicitly.

### Elevation
Consistent shadow scale (sm → xl). Shadows encode hierarchy, not decoration.

## Interaction Design

### Micro-interactions
Trigger → Rules → Feedback → Loops. Visible feedback within 100ms keeps users oriented.

### States
Design every state: default, hover, focus, active, disabled, loading, error, success, empty. Skipping any state = bug.

### Transitions
150–300ms. Ease-out on enter, ease-in on exit. Motion supports comprehension, never decoration alone.

### Affordances
Interactive elements must look interactive. Clear clickability, editability, draggability cues.

### Fitts's Law
Larger targets faster to acquire; nearer targets faster still. Touch targets ≥44×44px; WCAG 2.2 minimum 24×24px.

### Error Prevention
Constraints over confirmations. Undo over warnings. Inline validation on blur, not on every keystroke.

### Progressive Disclosure
Essentials first. Details on demand. Reduces cognitive load.

### Loading
Skeletons over spinners. Optimistic UI for predictable success. Progress indicators when >1s.

## Design Systems (Atomic Design + Tokens)

### Atomic Design
Atoms (tokens, icons, buttons) → Molecules (input groups, cards) → Organisms (headers, forms) → Templates → Pages.

### Design Tokens (3 tiers)
- **Primitive**: raw values (`blue-500: #3B82F6`).
- **Semantic**: purpose-mapped (`color-primary: {blue-500}`, `color-error: {red-500}`).
- **Component**: component-scoped (`button-bg: {color-primary}`).

Token categories: color, spacing, typography, elevation, border-radius, motion duration + easing.

### Component Specs
Document props, variants, sizes, all states, accessibility requirements, usage guidelines, do/don't examples. Every component has anatomy + behavior + a11y + code example.

### Versioning
Semantic versioning per release. Changelog every update. Breaking changes require migration guide.

## Accessibility (WCAG 2.2 AA)

- **Perceivable**: alt text, captions, contrast (4.5:1 / 3:1), resizable to 200% without loss.
- **Operable**: full keyboard navigation, no traps, skip links, focus management, target ≥24×24px.
- **Understandable**: consistent navigation, predictable behavior, error suggestions, clear labels.
- **Robust**: valid HTML, ARIA only when native semantics insufficient. Test with NVDA, VoiceOver, JAWS.
- **Focus**: visible indicators ≥2px, logical tab order, trap inside modals, restore on close.
- **ARIA**: follow WAI-ARIA Authoring Practices for tabs, dialogs, menus, comboboxes, listboxes.

## Responsive + Mobile-First

- **Breakpoints**: 320 (mobile), 640 (sm), 768 (md), 1024 (lg), 1280 (xl), 1536 (2xl).
- **Fluid typography**: `clamp(min, preferred, max)` scales smoothly between breakpoints.
- **Flexible layouts**: CSS Grid for page layout; Flexbox for component layout. Avoid fixed widths.
- **Content reflow**: stack columns on mobile, expand on desktop. Never hide critical content on mobile.
- **Touch vs pointer**: larger targets, swipe gestures, bottom-reachable primary actions on mobile.
- **Hover**: enhances only — never gates functionality.
- **Container queries**: component-level responsiveness independent of viewport.

## Platform Guidelines

### Material Design 3
Dynamic color (user-themable palette derived from a seed), expressive motion, adaptive layouts. Primary reference for Android + cross-platform web.

### Apple HIG
Clarity, deference, depth. SF Symbols for iconography. Primary reference for iOS + macOS. Respect platform conventions (swipe-back gesture, safe areas, status bar contrast).

### Fluent Design
Depth, motion, material, scale. Reference for Windows surfaces.

### Web Conventions
Underlined links, top-left logo → home, search/cart top-right. Violate only with deliberate cause.

## Heuristics

### Nielsen 10 (apply during review)
1. Visibility of system status
2. Match between system and real world
3. User control + freedom (undo, exits)
4. Consistency + standards
5. Error prevention
6. Recognition over recall
7. Flexibility + efficiency (shortcuts for experts)
8. Aesthetic + minimalist design
9. Help users recognize, diagnose, recover from errors
10. Help + documentation

### Gestalt (apply during composition)
Proximity, similarity, continuity, closure, figure-ground, common region — see Visual Hierarchy.

## Conversion-Centered Design

- **Hierarchy directs action**: primary CTA stands out via size, color, contrast, position, surrounding whitespace.
- **Above the fold**: clear headline, supporting subhead, visual, single primary CTA. One job per screen.
- **Social proof**: testimonials, ratings, logos, case studies — placed near decision points.
- **Friction reduction**: minimal form fields, progress indicators on multi-step forms, autofill support, one-click actions when safe.
- **Trust signals**: security badges, guarantees, transparent pricing, privacy assurances near conversion.
- **Urgency + scarcity**: only when genuine. Fabricated timers and fake stock counts are dark patterns.
- **A/B testing**: one variable at a time. Reach statistical significance before declaring a winner.

## Design-to-Code Handoff

- **Tokens → CSS variables**: `--color-primary`, `--spacing-4`, `--font-size-lg`.
- **Component specs**: every variant, every state, responsive behavior, animation timing.
- **Spacing**: multiples of base unit (4 or 8 px). No arbitrary values.
- **Assets**: SVG for icons, WebP/AVIF for photos, 1× + 2× raster fallbacks when needed.
- **Animation specs**: property, duration, easing, delay. Prefer CSS transitions over JS.
- **Figma mappings**: Auto Layout ↔ Flexbox, variants ↔ component props, tokens ↔ CSS variables, components ↔ Storybook stories.

## Anti-Patterns

- Designing only the happy path — always specify empty, loading, error, edge-case states.
- Pixel-perfect obsession at the expense of responsive resilience.
- Ignoring platform conventions — users expect familiar patterns.
- Decorative complexity without purpose.
- Fixed layouts that break on unexpected screen sizes or content lengths.
- Color as the sole indicator — always pair with icon, text, or pattern.
- Tiny touch targets — frustrating for mobile + motor-impaired users.
- Inconsistent spacing + alignment — destroys visual rhythm and trust.
- Bypassing the design system with one-off values — creates unmaintainable UI.

## When this applies

| Workflow | Apply this knowledge |
|---|---|
| `Agent(ui-ux-designer)` invocation | Auto-loaded |
| `/feature-design` Wave 2 UX-FLOW | Spawned designer loads this |
| `/architecture` (UX-FLOW step) | Architect references for IA + flows |
| `/seo-review` (accessibility section) | SEO reviewer references WCAG checks |
| `/content-creation` (visual direction) | Content designer references tokens + hierarchy |
| `/code-review` (UI changes) | Reviewer checks tokens + states + a11y |

## Integration

- **Consumed by**: `ui-ux-designer` (primary), `frontend-engineer` (implementation handoff), `content-designer` (visual direction), `seo-engineer` (a11y + Core Web Vitals), `content-writer` (UI microcopy).
- **External references**: WCAG 2.2, Material Design 3, Apple HIG, Microsoft Fluent, Nielsen Norman Group heuristics, WAI-ARIA Authoring Practices.
