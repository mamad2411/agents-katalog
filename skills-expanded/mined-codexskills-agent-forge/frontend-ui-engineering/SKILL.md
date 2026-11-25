---
name: frontend-ui-engineering
description: Build production-grade user interfaces with component architecture, design systems, state management, accessibility compliance, responsive design, and performance budgets.
---

# Frontend UI Engineering

## Overview

Frontend UI engineering bridges design and infrastructure. It is the practice of building user interfaces that are not just visually correct but also accessible, performant, maintainable, and resilient across devices, network conditions, and user contexts. This skill provides a systematic framework for producing production-quality frontend code.

Production UIs must satisfy five dimensions: correctness (matches design), accessibility (works for everyone), performance (loads and responds fast), reliability (handles errors gracefully), and maintainability (can be changed without breaking). This skill addresses all five.

## When to Use

- Building new UI components or pages
- Establishing or extending a design system
- Implementing responsive layouts
- Adding interactive features (forms, modals, drag-and-drop, etc.)
- Performing accessibility audits and remediation
- Performance optimization of existing UI
- Setting up state management architecture
- Cross-browser compatibility work
- Before shipping any user-facing feature
- Code review of frontend changes

## Process

### Step 1: Design System Alignment

Before writing any UI code, establish the design system context:

1. **Identify tokens**:
   - Colors (background, text, border, accent, error, success)
   - Typography (family, weight, size, line-height scale)
   - Spacing (4px/8px/12px/16px/24px/32px/48px/64px scale)
   - Shadows (elevation levels)
   - Border radius (none, sm, md, lg, full)
   - Breakpoints (mobile, tablet, desktop, wide)

2. **Verify implementation**:
   - Are tokens defined in CSS custom properties? (`--color-primary: #...`)
   - Are tokens used consistently? (No magic numbers in component code)
   - Are there any drift between design tokens and implementation?

3. **Component inventory**:
   - What existing components can be composed for this UI?
   - Is there a gap that requires a new component?
   - Does the new component fit the existing pattern?

### Step 2: Component Architecture

Every UI component follows the same structure:

```
Component/
├── Component.tsx          # Presentation logic only
├── Component.hooks.ts     # State and side effects
├── Component.css          # Scoped styles (or CSS-in-JS)
├── Component.test.tsx     # Unit tests
└── index.ts               # Public API (re-exports)
```

**Component types** with strict rules:

1. **Atoms** (Button, Input, Icon):
   - Receive props, render HTML, handle basic interaction
   - No business logic
   - No data fetching
   - Fully controlled

2. **Molecules** (SearchBar, FormField, Card):
   - Compose 2+ atoms
   - Handle composition logic (layout, focus management)
   - No business logic
   - Call callbacks for actions

3. **Organisms** (Header, ProductList, CheckoutForm):
   - Compose molecules + atoms
   - May contain business logic
   - May fetch data (via hooks)
   - Define layout regions

4. **Templates** (PageLayout, DashboardLayout):
   - Define layout structure
   - Placeholder slots for organisms
   - No business logic
   - No data dependencies

5. **Pages** (HomePage, ProductPage):
   - Compose templates + organisms
   - Orchestrate data fetching
   - Handle routing/URL state
   - One page per route

### Step 3: State Management Patterns

Choose and enforce a state management pattern:

| State Type | Pattern | Tool Examples |
|------------|---------|---------------|
| Server state | React Query / SWR | `useQuery`, `useMutation` |
| URL state | Router state | `useSearchParams`, `useParams` |
| Form state | Form libraries | React Hook Form, Formik |
| UI state | Local state + context | `useState`, `useReducer`, zustand |
| Global state | Minimal, prefer composition | zustand, Jotai, Context |

**Rules:**
- Server state is never duplicated in local state (use cache invalidation instead)
- URL state is the source of truth for page-level filters and pagination
- Form state stays in form libraries (not lifted to parent unless needed for multi-step forms)
- Context API for low-frequency updates only (theme, locale, auth user)
- For high-frequency updates, use zustand/Jotai or local state

### Step 4: Responsive Design Implementation

Use a consistent breakpoint system:

```css
/* Mobile-first breakpoints */
:root {
  --bp-sm: 640px;   /* Mobile landscape */
  --bp-md: 768px;   /* Tablet */
  --bp-lg: 1024px;  /* Desktop */
  --bp-xl: 1280px;  /* Wide desktop */
  --bp-2xl: 1536px; /* Ultra-wide */
}
```

**Rules:**
- Mobile-first: Base styles are mobile, media queries add complexity for larger screens
- Test at every breakpoint, not just the ones you design for
- Never hide content on mobile that's available on desktop (responsive = adapted, not gimped)
- Touch targets: minimum 44×44px (WCAG 2.5.8)
- Use CSS Grid for page-level layouts, Flexbox for component-level layouts
- Container queries for component-level responsiveness

### Step 5: WCAG 2.2 AA Compliance Checklist

Every UI must pass these checks:

**Perceivable:**
- [ ] All images have meaningful alt text
- [ ] Color is not the only way to convey information
- [ ] Color contrast: 4.5:1 for normal text, 3:1 for large text (18px+ bold or 24px+ regular)
- [ ] Non-text content has text alternatives
- [ ] Captions provided for video/audio content
- [ ] Content does not flash more than 3 times per second

**Operable:**
- [ ] All functionality available via keyboard
- [ ] Focus indicator is visible (minimum 2px outline, 3:1 contrast against adjacent background)
- [ ] Focus order follows visual order
- [ ] Skip navigation link present
- [ ] Touch targets are 44×44px minimum
- [ ] No keyboard traps
- [ ] Motion/animation can be disabled (prefers-reduced-motion)
- [ ] Timeouts have warning and extend option

**Understandable:**
- [ ] Page language is set (`<html lang="en">`)
- [ ] Form inputs have associated `<label>` elements
- [ ] Error messages are clear and suggest corrections
- [ ] Navigation is consistent across pages
- [ ] Components with similar functions have consistent labeling

**Robust:**
- [ ] Semantic HTML used (landmarks: `<nav>`, `<main>`, `<aside>`, etc.)
- [ ] ARIA attributes used correctly and only when needed
- [ ] Custom elements have appropriate roles, states, and properties
- [ ] Valid HTML (no duplicate IDs, proper nesting)

### Step 6: Accessibility Testing

Run these tests on every component:

1. **Automated** (CI gate):
   - axe-core integration (jest-axe for unit tests, cypress-axe for e2e)
   - Lighthouse accessibility audit (score must be 95+)
   - eslint-plugin-jsx-a11y for static analysis
   - Color contrast checker in the build pipeline

2. **Manual** (QA gate):
   - Keyboard navigation through every interactive element
   - Screen reader test (VoiceOver on Mac, NVDA on Windows, TalkBack on Android)
   - Zoom test (200% zoom without losing content)
   - Focus order verification
   - prefers-reduced-motion test

3. **User testing**:
   - Test with actual assistive technology users at least once per quarter
   - Document known issues and workarounds

### Step 7: Performance Budgets

Set and enforce these budgets:

**Loading performance (Lighthouse, CI):**
- [ ] First Contentful Paint (FCP) < 1.5s
- [ ] Largest Contentful Paint (LCP) < 2.5s
- [ ] Total Blocking Time (TBT) < 200ms
- [ ] Cumulative Layout Shift (CLS) < 0.1
- [ ] First Input Delay (FID) / Interaction to Next Paint (INP) < 200ms
- [ ] Time to Interactive (TTI) < 3.5s

**Asset budgets:**
- Total JavaScript < 300KB (compressed)
- Total CSS < 50KB (compressed)
- Initial HTML < 50KB (compressed)
- Fonts < 100KB total (WOFF2)
- Images: Largest contentful image < 200KB

**Runtime budgets:**
- No long tasks (>50ms) on the main thread
- No layout thrashing (batch DOM reads/writes)
- Animation frame budget: < 10ms per frame
- Component render time: < 5ms (dev tools profiler)

**Tools to enforce:**
- `webpack-bundle-analyzer` or `vite-bundle-visualizer`
- Lighthouse CI in the pipeline
- `perf-budget` config in Lighthouse
- Chrome DevTools Performance panel (every PR)
- React Profiler for component render costs

## Anti-Rationalization Table

| Excuse | Rebuttal |
|--------|----------|
| "I'll add accessibility later" | Later never comes. Accessibility retrofits cost 3-5x more than building it in from the start. And shipping inaccessible UI excludes 15% of the population. Add it now. |
| "This is just a small component, it doesn't need tests" | Small components are the cheapest to test. A Button test takes 30 seconds to write. An untested Button that breaks in production takes hours to debug and deploy. |
| "The design doesn't have mobile mockups, I'll just guess" | Don't guess. Use established responsive patterns: stack vertically, reduce padding, increase touch targets. Default to accessible, one-column layouts. |
| "Performance isn't critical for this internal tool" | Internal tools are used all day, every day. A 500ms slower page load × 1000 employees × 50 loads/day = 7 hours of lost productivity per day. Performance matters everywhere. |
| "Our users all use Chrome, I don't need to test other browsers" | Even if true, browser rendering differences in CSS Grid, font rendering, and scroll behavior affect every user. Test at minimum Chrome + Firefox + Safari. |
| "We can't match the design exactly because of accessibility contrast requirements" | The design needs to be updated, not the accessibility requirement. WCAG 4.5:1 is non-negotiable. Work with designers to find accessible alternatives that preserve the visual intent. |
| "This animation is essential and I won't honor prefers-reduced-motion" | Motion can cause vestibular disorders, nausea, and migraines. Honor prefers-reduced-motion by default, and provide an explicit opt-in for animation. |

## Red Flags

- **Magic numbers in CSS** (not using design tokens): Design system drift
- **Component > 300 lines**: Needs decomposition
- **No accessibility attributes on custom interactive elements**: Keyboard and screen reader will fail
- **Large images without srcset**: Mobile bandwidth waste
- **No loading/error state**: Component will fail silently
- **Direct DOM manipulation in React/Vue/Angular**: Framework anti-pattern
- **Fonts loaded without `font-display: swap`**: Invisible text during load
- **No `<meta name="viewport">` tag**: Mobile rendering failure

## Verification

- [ ] Test: Run axe-core on every component and verify zero critical/serious violations
- [ ] Test: Navigate every interactive element using keyboard only (Tab, Enter, Escape, Arrow keys)
- [ ] Test: Run Lighthouse on every page and verify all scores 90+
- [ ] Test: Verify responsive layout at 320px, 640px, 768px, 1024px, and 1440px
- [ ] Test: Measure bundle size and verify within budget
- [ ] Test: Load page on Slow 3G throttling and verify FCP < 3s
- [ ] Test: Verify all form inputs have associated labels
- [ ] Test: Verify prefers-reduced-motion disables all non-essential animations
- [ ] Test: Verify color contrast meets WCAG AA for all text elements
- [ ] Test: Verify no console errors or warnings in any browser
