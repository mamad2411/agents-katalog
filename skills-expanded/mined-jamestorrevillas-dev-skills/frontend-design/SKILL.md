---
name: frontend-design
description: Use this skill when building UI components, designing frontend architecture, implementing styling systems, optimizing performance, ensuring accessibility, or creating production-grade interfaces. Trigger on keywords: frontend, component, UI, styling, React, Next.js, Angular, Tailwind, CSS, responsive, accessibility, performance, animation, design system.
---

# Frontend Design

## Design Philosophy

**Avoid distributional convergence** — the tendency for AI to default to generic purple gradients, Inter font, and rounded-corner cards. Every interface should have a deliberate aesthetic based on its purpose and audience.

Before writing a single line of CSS, define:
- What emotion should this interface convey?
- Who is the user and what context are they in?
- What is the single most important action on this screen?

---

## Component Architecture

### Atomic Design Hierarchy
```
Atoms      → Button, Input, Label, Icon
Molecules  → SearchBar (Input + Button), FormField (Label + Input + Error)
Organisms  → Header, ProductCard, UserProfile
Templates  → PageLayout, DashboardLayout
Pages      → Specific instances with real data
```

### Component Rules
- One component = one responsibility
- Props should be explicit, not inferred
- Use composition over prop-drilling
- Default to server components; use client components only for interactivity

---

## Styling System

### Tailwind Best Practices
```tsx
// Extract repeated patterns into components, not custom CSS
// BAD: Duplicating classes everywhere
<div className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg">

// GOOD: Extract to a component
<Button variant="primary">Click me</Button>
```

### Design Tokens (Custom Properties)
```css
:root {
  --color-primary: #your-brand-color;
  --color-surface: #f8f9fa;
  --spacing-unit: 4px;
  --radius-default: 8px;
  --font-heading: 'Your Chosen Font', sans-serif;
}
```

### Typography That Avoids Generic AI Look
- Don't default to Inter or Roboto — they signal "AI generated"
- Consider: Geist, Instrument Sans, Plus Jakarta Sans, DM Sans
- Mix weights deliberately: 400 for body, 600 for emphasis, 800 for headlines
- Establish a clear type scale before building

---

## Performance Optimization

### Core Web Vitals Targets
| Metric | Target | What It Measures |
|---|---|---|
| LCP | < 2.5s | Largest Contentful Paint — loading |
| FID/INP | < 100ms | Interaction responsiveness |
| CLS | < 0.1 | Layout stability |

### Key Techniques
- **Images:** Use `next/image` or native lazy loading, modern formats (WebP/AVIF)
- **Fonts:** `font-display: swap`, preload critical fonts
- **JS:** Code splitting, dynamic imports for heavy components
- **CSS:** Purge unused styles in production
- **Server Components:** Move data fetching to the server, reduce client JS

---

## Accessibility (WCAG 2.1 AA)

### Non-Negotiables
- [ ] All interactive elements reachable by keyboard (Tab order)
- [ ] Focus visible on all focusable elements
- [ ] Color contrast ratio ≥ 4.5:1 for normal text, 3:1 for large
- [ ] All images have meaningful alt text (or `alt=""` for decorative)
- [ ] Form inputs have associated labels
- [ ] Error messages are associated with their fields
- [ ] ARIA roles used correctly (don't add ARIA unnecessarily)

### Semantic HTML First
```tsx
// BAD: div soup
<div onClick={...} className="button">Click</div>

// GOOD: semantic HTML
<button type="button" onClick={...}>Click</button>
```

---

## State Management Decision Guide

| Need | Solution |
|---|---|
| Local UI state | useState |
| Shared local state | useContext or prop drilling |
| Server state / caching | TanStack Query / SWR |
| Complex client state | Zustand (lightweight) or Redux Toolkit |
| Form state | React Hook Form |
| URL state | useSearchParams / nuqs |

**Rule:** Start with the simplest option. Reach for complexity only when you feel the pain.

---

## Animation Guidelines

- Animations should have purpose — convey state change, guide attention, provide feedback
- Duration: 150-300ms for UI transitions, 400-600ms for page transitions
- Easing: ease-out for entrances, ease-in for exits, ease-in-out for emphasis
- Respect `prefers-reduced-motion` — always provide a no-animation fallback
```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; }
}
```

---

## Next.js Specific (App Router)

- Default to **Server Components** — fetch data server-side
- Use **Client Components** only for: event handlers, browser APIs, hooks, real-time updates
- Place `'use client'` as low in the tree as possible
- Use **Server Actions** for form submissions and mutations
- Route handlers (`route.ts`) for custom API endpoints
