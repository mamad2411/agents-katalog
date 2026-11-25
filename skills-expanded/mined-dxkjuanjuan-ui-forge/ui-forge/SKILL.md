---
name: ui-forge
description: "5-stage UI design forge: Discover → Tokenize → Compose → Animate → Polish. Integrates 9 sub-skills (ui-ux-pro-max, awesome-design-md, ui-styling, motion-ui, frontend-design-direction, make-interfaces-feel-better, design-system, design, brand) + 9 reference sites (React Bits, Motion Primitives, Aceternity UI, Framer Motion, GSAP, Pageflow, Godly, Animate UI, GSAP Showcase) + Figma MCP. Covers landing pages, SaaS dashboards, mobile UI, component libraries, and advanced motion. Use when building any UI from scratch or from a Figma design."
argument-hint: "[description] [--figma-url URL] [--brand NAME] [--skip phases] [--intensity low|medium|high]"
---

# UI Forge — 5-Stage Design Forge

A production-grade UI design workflow that forges pixel-perfect, accessible, animated interfaces from Figma designs or text descriptions.

## When to Use

- Building any UI from scratch: landing pages, dashboards, mobile apps, component libraries
- Converting a Figma design to code
- Creating branded interfaces that need design system consistency
- Adding motion and micro-interactions to existing components
- When the user says "build me a page", "design a UI", "implement this Figma", or "create a component"

## Arguments

| Arg | Default | Description |
|-----|---------|-------------|
| `--figma-url URL` | — | Figma file URL (triggers Entry A) |
| `--brand NAME` | — | Brand from awesome-design-md (e.g. stripe, vercel, linear) |
| `--skip PHASES` | — | Comma-separated phases to skip (e.g. `animate,polish`) |
| `--intensity LEVEL` | auto | Motion intensity: low/medium/high (auto-detected from product type) |

---

## The 5 Stages

```
Entry A (Figma) ──┐
                   ├─→ Phase 1: Discover → Phase 2: Tokenize → Phase 3: Compose → Phase 4: Animate → Phase 5: Polish → Delivery
Entry B (Text)  ──┘
                                                                                                              ↓
                                                                                                     [Figma writeback?]
```

### Quality Gate Protocol

Each phase has a quality gate. If a gate fails:
1. Roll back to the previous phase and adjust
2. Maximum 2 retries per phase
3. After 2 retries, report the issue and ask user for guidance

---

## Phase 1: Discover — Direction Finding

### Entry A: Figma Design

When `--figma-url` is provided:

1. Use `figma-developer-mcp` → `get_figma_data` to extract node tree, components, styles
2. Map Figma structures:
   - Auto Layout → Flexbox (reliable)
   - Nested Auto Layout → CSS Grid (reliable)
   - Auto Layout wrap → Flex wrap (reliable)
   - Absolute positioning + Constraints → Responsive (needs manual adjustment)
   - Figma Variants → Component variants (partial support)
3. Extract component instances → identify reusable components
4. Extract Figma Variables → direct CSS variable conversion

### Entry B: Text / Brand Description

When no Figma URL:

1. Use `ui-ux-pro-max` to search style direction:
   ```bash
   python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<user description>" --domain style
   python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<user description>" --domain product
   ```
2. Use `awesome-design-md` to match brand tokens — read `~/.claude/skills/awesome-design-md/design-md/<brand>.md`
3. Use `frontend-design-direction` to set: purpose, audience, tone, memorable detail, constraints

### Mixed Mode

When user provides "reference this site + change to dark style":
- Extract layout/structure from the reference
- Take colors/fonts from brand tokens
- Merge both into the design direction

### Reference Sites

| Site | How to use |
|------|-----------|
| **Godly** | Browse similar product sites for visual direction. Use kimi-webbridge to navigate godly.website and filter by category. |
| **Pageflow** | For narrative/scrolling pages, reference scrollytelling structures. Use kimi-webbridge to browse pageflow.app. |

### Accessibility Pre-constraint

- Verify primary color contrast ratio ≥ 4.5:1 at this stage
- Confirm accessibility target: AA or AAA

### Quality Gate Output

```yaml
design-direction.md:
  product_type: SaaS | landing | mobile | component-library
  style_direction: [ui-ux-pro-max style name + AI prompt keywords]
  brand_token_source: [awesome-design-md brand] | [custom]
  reference_sites: [specific pages from Godly/Pageflow]
  figma_node_id: [if applicable]
  tech_stack: [detected from project]
  interaction_mode: SPA | SSR | SSG | native
  accessibility_level: AA | AAA
```

### Skip Condition

- Project has DESIGN.md < 30 days old AND requirements unchanged → skip
- DESIGN.md > 30 days old → suggest re-discovery

---

## Phase 2: Tokenize — Design Token Generation

### Token Generation Flow

1. **Brand token base** → `awesome-design-md` brand → extract colors/typography/spacing/rounded/shadows
2. **Style enhancement** → `ui-ux-pro-max` search:
   ```bash
   python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<style>" --domain style
   python3 ~/.claude/sskills/ui-ux-pro-max/scripts/search.py "<style>" --domain typography
   python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<style>" --domain color
   python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<style>" --design-system --variance N --motion N --density N
   ```
3. **Token systemization** → `design-system` skill → three-layer tokens (primitive → semantic → component)
4. **Figma variable mapping** (if applicable) → Figma Variables → CSS variables

### Reference Sites

| Site | How to use |
|------|-----------|
| **Animate UI** | Reference for motion timing/easing tokens |
| **GSAP** | Standard motion durations: fast 150ms, normal 300ms, slow 600ms |

### Accessibility Pre-constraint

- All color palettes validated for contrast at generation time
- Dark mode tokens generated simultaneously, not deferred

### Quality Gate Output

Generate `design-tokens.json` with:

```css
/* Primitive tokens */
:root {
  /* Colors — light */
  --color-primary: oklch(68% 0.21 250);
  --color-canvas: oklch(98% 0 0);
  --color-ink: oklch(18% 0 0);
  /* Colors — dark */
  --color-primary-dark: oklch(72% 0.21 250);
  --color-canvas-dark: oklch(15% 0 0);
  --color-ink-dark: oklch(95% 0 0);
  /* Typography */
  --text-display-xl: clamp(3rem, 1rem + 7vw, 8rem);
  --text-body: clamp(1rem, 0.92rem + 0.4vw, 1.125rem);
  /* Spacing */
  --space-xs: 4px; --space-sm: 8px; --space-md: 16px;
  --space-lg: 32px; --space-xl: 64px;
  --space-section: clamp(4rem, 3rem + 5vw, 10rem);
  /* Rounded */
  --rounded-xs: 4px; --rounded-sm: 8px; --rounded-md: 12px;
  --rounded-lg: 16px; --rounded-xl: 24px; --rounded-full: 9999px;
  /* Shadows */
  --shadow-subtle: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-medium: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-prominent: 0 8px 24px rgba(0,0,0,0.12);
  /* Motion */
  --motion-fast: 150ms; --motion-normal: 300ms; --motion-slow: 600ms;
  --ease-default: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-spring: cubic-bezier(0.22, 1, 0.36, 1);
  --stagger-default: 50ms; --stagger-fast: 30ms; --stagger-slow: 80ms;
  --distance-micro: 4px; --distance-small: 8px;
  --distance-medium: 16px; --distance-large: 32px;
}
```

### Skip Condition

- Project has token system + consistent with Phase 1 direction + brand unchanged → skip
- Brand or style changed → do not skip
- Minor tweaks → skip, do incremental update

---

## Phase 3: Compose — Component Building

### Component Generation Order (Strict Priority)

1. **Layout skeleton** → Layout / Header / Main / Footer / Sidebar
2. **Core blocks** → Hero / Data tables / Primary interaction areas
3. **Reusable components** → Button / Card / Badge / Input / Select
4. **Auxiliary components** → Toast / Tooltip / Modal / Dropdown

Build skeleton first, then fill in. Never generate all components at once.

### UI Type Routing

| Type | Strategy | Sub-skills |
|------|----------|-----------|
| Landing page | Hero/CTA/Feature/Testimonial structure | `banner-design` + `ui-styling` |
| SaaS dashboard | Table/Form/Modal/Sidebar/Charts | `ui-styling` + `design-system` |
| Mobile UI | Responsive + platform patterns | `ui-styling` + responsive tokens |
| Component library | shadcn/ui base + custom variants | `ui-styling` |
| Advanced motion | 3D Canvas + particles + Lottie placeholders | `ui-styling` + motion scaffolds |

### Component Reuse Detection

Before generating, scan existing project components:
- Has shadcn Button? → Don't regenerate
- Has custom Card? → Check token compatibility, reuse if compatible
- Use `find` and `grep` to detect existing components

### Accessibility Pre-constraint

- Component skeletons include ARIA attributes from the start
- Interactive components include keyboard navigation from the start
- Touch targets ≥ 44px

### Reference Sites

| Site | How to use |
|------|-----------|
| **React Bits** | Small components + micro-interaction snippets. Browse reactbits.dev for copy-ready patterns. |
| **Aceternity UI** | High-end motion components (3D Card, Spotlight, Beam, etc.). Reference ui.aceternity.com. |
| **shadcn/ui** | Base component specs. Reference ui.shadcn.com for accessible component patterns. |

### Quality Gate Output

```yaml
component-tree.md:
  tech_stack: [detected]
  generation_order: [layout → core → reusable → auxiliary]
  component_tree:
    Layout → Header / Main / Footer
    Header → Nav / Logo / CTA
    Main → Hero / Features / CTA
  reusable_components: [list with token compatibility check]
  file_structure: src/components/{hero,features,ui}/
  responsive_breakpoints: 320 / 768 / 1024 / 1440
  code_skeletons: [props + structure + class names only, not full implementation]
```

### Skip Condition

- Existing component library compatible with token system → skip
- Only needs animation/polish → skip

---

## Phase 4: Animate — Motion Injection

### Motion Intensity Auto-Detection

| Product Type | Intensity | Typical Motion |
|-------------|-----------|---------------|
| Landing page | **High** | Scroll narrative, parallax, entrance, particles |
| SaaS dashboard | **Low** | Micro-interactions, state transitions, skeleton screens |
| Mobile UI | **Medium** | Gestures, page transitions, haptic feedback |
| Component library | **Micro** | hover, focus, active, loading states |

Override with `--intensity high|medium|low`.

### Motion Pattern Matching

| Motion Type | Implementation | Reference |
|-------------|---------------|-----------|
| Entrance | `motion/react` whileInView / GSAP ScrollTrigger | Motion / Motion Primitives |
| State transition | AnimatePresence + motion variants | Framer Motion |
| Scroll narrative | GSAP Timeline + ScrollTrigger | GSAP / Pageflow |
| Micro-interaction | CSS transitions / `motion/react` whileHover/whileTap | Animate UI / React Bits |
| 3D / Particles | Three.js / ts-particles / Lottie | GSAP Showcase |

### Using ui-ux-pro-max for GSAP Patterns

```bash
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "scroll reveal" --domain gsap
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "stagger entrance" --domain gsap
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "page transition" --domain gsap
```

### Tech Stack Motion Mapping

| Stack | Motion Library |
|-------|---------------|
| React + Tailwind | motion/react + GSAP (for complex) |
| Next.js + Tailwind | motion/react + GSAP (for complex) |
| Vue + Nuxt | @vueuse/motion |
| Svelte | svelte/motion + svelte/transition |
| SwiftUI | .animation() + withAnimation |
| Flutter | AnimationController + ImplicitlyAnimatedWidget |

### Accessibility Pre-constraint

- ALL motion must support `prefers-reduced-motion`
- Reduced motion fallback: opacity transitions only, duration: 0ms
- Implement via:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

```tsx
// motion/react
const shouldReduceMotion = useReducedMotion()
```

### Reference Sites

| Site | How to use |
|------|-----------|
| **Framer Motion** | React motion standard library. Reference motion.dev for API patterns. |
| **Motion Primitives** | Base animation modules (entrance, exit, spring). Reference motion-primitives.com. |
| **GSAP** | Professional animation (ScrollTrigger, Timeline, SVG path). Reference gsap.com. |
| **GSAP Showcase** | Top-tier motion case studies. Reference gsap.com/showcase. |
| **Animate UI** | Pure CSS motion fallback (hover, scroll-triggered). Reference animate-ui.com. |

### Quality Gate Output

```yaml
animation-spec.md:
  intensity: high | medium | low
  entrance: { type, duration, stagger, easing }
  scroll: { type, trigger, scrub }
  micro: { hover, focus, active }
  states: { loading, success, error, empty }
  reduced_motion: { fallback, duration }
  implementation: [motion code per component]
```

### Skip Condition

- `--skip animate` flag
- SaaS dashboard + user explicitly declines motion
- Simple utility page with no interaction

---

## Phase 5: Polish — Micro-interaction Refinement

### 1. Visual Polish (`make-interfaces-feel-better`)

**Concentric radius:** outer radius = inner radius + padding
**Optical alignment:** offset asymmetric icons by 1-2px
**Layered shadows:** transparent, subtle, background-compatible
**Text wrapping:**
- `text-wrap: balance` on headings and short titles
- `text-wrap: pretty` on body text, captions, descriptions
- Neither on long prose or code
**Tabular numbers:** `font-variant-numeric: tabular-nums` for counters, prices, timers
**Image outlines:** `outline: 1px solid rgba(0,0,0,0.1); outline-offset: -1px`
**Font smoothing:** `-webkit-font-smoothing: antialiased` on macOS

### 2. Interaction State Completion

Every interactive component must have:
- **hover** — visual feedback on mouse-over
- **focus** — visible focus ring (2px offset, brand color)
- **active** — pressed/engaged state
- **disabled** — reduced opacity + not-interactive
- **loading** — skeleton or spinner
- **error** — error message + red accent
- **empty** — empty state illustration or message

Touch targets ≥ 44px. Keyboard navigation complete.

### 3. Brand Consistency Check (`brand`)

- Token usage: all colors/fonts/spacing strictly follow tokens
- Tone: copywriting style matches brand voice
- Dark mode: all components have complete dark mode variants
- No hardcoded values outside the token system

### 4. Responsive Verification

- 320px / 768px / 1024px / 1440px breakpoints
- No text overflow, no image clipping, no layout shift
- `clamp()` for fluid typography and spacing
- `min()` / `max()` for boundary constraints

### 5. Accessibility Final Verification

- `prefers-reduced-motion` all motion degrades correctly
- All text meets AA (4.5:1) or AAA (7:1) contrast
- ARIA attributes complete on all interactive elements
- Keyboard navigation reaches every interactive element
- Screen reader order matches visual order

### Reference Sites

| Site | How to use |
|------|-----------|
| **React Bits** | Micro-interaction detail patterns. Reference reactbits.dev. |

### Quality Gate Output

```yaml
polish-checklist.md:
  visual: [concentric-radius ✓ optical-align ✓ shadows ✓ text-wrap ✓ tabular-nums ✓ image-outlines ✓ font-smoothing ✓]
  interaction: [hover ✓ focus ✓ active ✓ disabled ✓ loading ✓ error ✓ empty ✓]
  brand: [token-consistency ✓ tone ✓ dark-mode ✓]
  responsive: [320 ✓ 768 ✓ 1024 ✓ 1440 ✓ no-overflow ✓]
  accessibility: [reduced-motion ✓ focus-ring ✓ contrast ✓ ARIA ✓ keyboard ✓]
```

### Final Deliverables

```
src/components/**/*.tsx    — Component code
src/styles/tokens.css      — CSS variables
src/styles/tokens.json     — Token JSON (for Figma writeback)
DESIGN.md                  — Design direction document
polish-checklist.md        — Polish checklist
```

### Figma Writeback (when Entry A was used)

- New tokens → write back to Figma Variables
- Component variants → update Figma component library
- Forms Figma ↔ Code bidirectional loop

### Skip Condition

- `--skip polish` flag

---

## Sub-Skill Call Map

| Phase | Sub-Skills | Reference Sites |
|-------|-----------|----------------|
| Discover | frontend-design-direction, ui-ux-pro-max, awesome-design-md, figma-developer-mcp | Godly, Pageflow |
| Tokenize | design-system, ui-ux-pro-max, awesome-design-md | Animate UI, GSAP |
| Compose | ui-styling, banner-design, design-system | React Bits, Aceternity UI, shadcn/ui |
| Animate | motion-ui, ui-ux-pro-max(--domain gsap) | Framer Motion, Motion Primitives, GSAP, GSAP Showcase, Animate UI |
| Polish | make-interfaces-feel-better, brand | React Bits |

## 9 Reference Sites — Complete Assignment

| # | Site | Phases | Role |
|---|------|--------|------|
| 1 | React Bits | 3, 5 | Component snippets + micro-interaction details |
| 2 | Motion Primitives | 4 | Base animation modules |
| 3 | Aceternity UI | 3 | High-end motion component reference |
| 4 | Framer Motion | 4 | React motion standard library |
| 5 | GSAP | 2, 4 | Token standards + professional animation |
| 6 | Pageflow | 1, 4 | Narrative structure + scroll narrative |
| 7 | Godly | 1 | Similar product visual direction |
| 8 | Animate UI | 2, 4 | Motion tokens + CSS motion fallback |
| 9 | GSAP Showcase | 4 | Top-tier motion case studies |

## Usage Examples

```
# Full pipeline from text
ui-forge "Build a Stripe-style pricing page for my SaaS"

# From Figma design
ui-forge --figma-url https://figma.com/design/abc123/My-Design

# Skip animation for a dashboard
ui-forge "Admin dashboard with user management" --skip animate

# Specific brand with high motion
ui-forge "Product launch landing page" --brand vercel --intensity high

# Component library only
ui-forge "Design system button variants" --skip animate,polish
```

## Accessibility Throughout

Not just Phase 5 — every phase has pre-constraints:

| Phase | Constraint |
|-------|-----------|
| Discover | Primary contrast ≥ 4.5:1, confirm AA/AAA target |
| Tokenize | All palettes contrast-validated, dark mode generated simultaneously |
| Compose | Skeletons include ARIA + keyboard navigation |
| Animate | All motion supports prefers-reduced-motion |
| Polish | Final verify: contrast + ARIA + focus + keyboard + reduced-motion |

## Tech Stack Adaptation

| Stack | Phase 3 Source | Phase 4 Library |
|-------|---------------|----------------|
| React + Tailwind | shadcn/ui + Radix | motion/react |
| Next.js + Tailwind | shadcn/ui + Radix | motion/react + GSAP |
| Vue + Nuxt | Nuxt UI | @vueuse/motion |
| Svelte + SvelteKit | shadcn-svelte | svelte/motion |
| SwiftUI | Native components | .animation() |
| Flutter | Material/Cupertino | Flutter animations |
