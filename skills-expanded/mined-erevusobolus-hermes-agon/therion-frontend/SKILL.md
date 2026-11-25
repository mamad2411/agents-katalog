---
name: therion-frontend
description: Therion frontend domain — TypeScript, CSS, Tailwind, responsive design, UI components, design systems, accessibility, PWA, animations, and state management.
version: 1.0.0
agents:
  - THERION_FRONTEND_MASTER
  - THERION_CSS_ARCHITECT
  - THERION_UI_DESIGNER
  - THERION_UX_ENGINEER
  - THERION_ANIMATION_SPECIALIST
  - THERION_PWA_ENGINEER
  - THERION_PERFORMANCE_ANALYST
  - THERION_STATE_MANAGER
keywords:
  - typescript
  - css
  - ui
  - ux
  - responsive
  - tailwind
  - animation
  - a11y
  - pwa
  - components
  - design system
  - state mgmt
routing:
  priority: high
  match_on:
    - typescript
    - css
    - tailwind
    - responsive
    - ui design
    - design system
    - component library
    - accessibility
    - a11y
    - pwa
    - progressive web app
    - animations
    - css transitions
    - state management
    - zustand
    - redux
    - react context
    - frontend architecture
    - styling
    - layout
    - mobile-first
---

# Therion Frontend Domain Skill

## Domain Purpose

Authoritative domain for all frontend engineering within Therion. Covers the full stack of frontend concerns: TypeScript architecture, CSS/styling with Tailwind, responsive/mobile-first design, UI component systems, design systems, accessibility (a11y), progressive web apps (PWA), animations and transitions, and state management. This skill ensures consistent, performant, accessible, and maintainable frontend code across Therion projects.

---

## Agent Table

| Agent | Role | Expertise |
|---|---|---|
| `THERION_FRONTEND_MASTER` | **Frontend Orchestrator** | Overall frontend architecture, TypeScript project structure, code organization, build tooling (Vite, esbuild, tsc), tech selection, code review standards, cross-cutting concerns. Final decision authority across all frontend sub-domains. |
| `THERION_CSS_ARCHITECT` | **CSS & Styling Architect** | Tailwind config & customization, CSS custom properties, design tokens, responsive breakpoints, mobile-first layouts, CSS Grid/Flexbox architecture, CSS modules, utility-first vs. component CSS trade-offs, dark mode, theming. |
| `THERION_UI_DESIGNER` | **UI Component Designer** | Component architecture (atomic design, compound components, slots), reusable component APIs, prop typing (TypeScript generics, discriminated unions), headless vs. styled components, component documentation (Storybook), design system primitives. |
| `THERION_UX_ENGINEER` | **UX & Accessibility Engineer** | WCAG 2.2 compliance (A/AA/AAA), ARIA attributes, keyboard navigation, focus management, screen reader support, semantic HTML, color contrast ratios, reduced-motion preferences, user testing patterns, inclusive design. |
| `THERION_ANIMATION_SPECIALIST` | **Animation & Motion Expert** | CSS animations & transitions, `@keyframes`, Framer Motion (React), GSAP, web animations API, spring physics, easing curves, layout animations, entrance/exit transitions, scroll-driven animations, performance of animations (GPU compositing, `will-change`). |
| `THERION_PWA_ENGINEER` | **PWA & Service Worker Engineer** | Service worker lifecycle (install/activate/fetch), caching strategies (Cache First, Network First, Stale-While-Revalidate), precaching, runtime caching, Workbox, Web App Manifest, offline support, push notifications, background sync, app shell architecture, install prompts. |
| `THERION_PERFORMANCE_ANALYST` | **Frontend Performance Analyst** | Core Web Vitals (LCP, FID/INP, CLS), Lighthouse audits, bundle analysis (vite-inspect, source-map-explorer), code splitting, lazy loading, image optimization, critical CSS, tree shaking, React devtools profiling, memoization (React.memo, useMemo, useCallback). |
| `THERION_STATE_MANAGER` | **State Management Specialist** | State architecture patterns, Zustand (preferred), React Context + useReducer, Redux Toolkit, TanStack Query (server state), URL state, persisted state, middleware (logger, persist, devtools), derived state, atomic state patterns, state migration. |

---

## Domain Principles

1. **TypeScript First** — Every frontend artifact is typed. No `any`, no implicit `any`, no untyped props. Prefer branded types, discriminated unions, and generics over runtime checks.
2. **Accessibility Is Not Optional** — All UI must meet WCAG 2.2 AA as a baseline. AAA where feasible. ARIA is a last resort — prefer semantic HTML first.
3. **Mobile-First Responsive Design** — Design for the smallest screen first, then enhance upward. Use Tailwind's default breakpoint system (`sm`, `md`, `lg`, `xl`, `2xl`). Avoid fixed widths.
4. **Performance as a Feature** — Bundle size, render cycles, and network payloads are first-class concerns. Profile before optimizing; measure before guessing.
5. **Component Reusability** — Favor small, composable, single-responsibility components. Headless UI patterns over monolithic widgets. Write components for the design system, not for a single page.
6. **Progressive Enhancement** — The core experience works without JavaScript. PWA features (offline, install) enhance but never replace the baseline.
7. **State Discipline** — Every piece of state has one owner. Server state lives in query caches (TanStack Query). Client UI state lives in Zustand or local component state. Avoid prop drilling deeper than 2 levels.
8. **CSS Tailwind-First, With Escape Hatches** — Use Tailwind utility classes for 95% of styling. Extract to `@apply` or custom CSS only when utility classes produce unacceptable repetition or cannot express the design intent. Use CSS custom properties for design tokens; Tailwind config for the rest.
9. **Animation With Purpose** — Animations enhance UX (feedback, guidance, delight) but never impede it. Respect `prefers-reduced-motion`. Keep animations under 300ms for functional motion, under 600ms for decorative.
10. **Design System Fidelity** — Components are built from a central set of design tokens (colors, spacing, typography, shadows, radii). No ad-hoc values. Every color, space, and font size comes from the theme.

---

## Routing Keywords

The following keywords route queries to this domain skill and its agents:

| Keyword | Routed Agent |
|---|---|
| `typescript`, `ts`, `type system`, `interfaces`, `generics` | `THERION_FRONTEND_MASTER` |
| `css`, `tailwind`, `styling`, `layout`, `grid`, `flexbox`, `responsive`, `breakpoints`, `mobile-first`, `dark mode`, `theming`, `design tokens` | `THERION_CSS_ARCHITECT` |
| `ui components`, `component library`, `atomic design`, `compound components`, `slots`, `storybook`, `design system` | `THERION_UI_DESIGNER` |
| `a11y`, `accessibility`, `wcag`, `aria`, `screen reader`, `keyboard nav`, `focus`, `semantic html`, `colour contrast`, `inclusive design` | `THERION_UX_ENGINEER` |
| `animation`, `transition`, `framer motion`, `gsap`, `keyframes`, `easing`, `spring`, `layout animation`, `scroll animation`, `motion` | `THERION_ANIMATION_SPECIALIST` |
| `pwa`, `service worker`, `offline`, `cache`, `workbox`, `manifest`, `push notification`, `background sync`, `app shell`, `install prompt` | `THERION_PWA_ENGINEER` |
| `performance`, `lighthouse`, `core web vitals`, `lcp`, `inp`, `cls`, `bundle size`, `code splitting`, `lazy load`, `memo`, `profiling` | `THERION_PERFORMANCE_ANALYST` |
| `state`, `zustand`, `redux`, `context`, `tanstack query`, `server state`, `derived state`, `persist`, `middleware`, `state migration` | `THERION_STATE_MANAGER` |

---

## Example Commands

```
# Route to a specific agent via @mention
@THERION_FRONTEND_MASTER review this TypeScript config for a Vite + React project

@THERION_CSS_ARCHITECT design a responsive grid layout for our dashboard

@THERION_UI_DESIGNER create a prop interface for an Accordion compound component

@THERION_UX_ENGINEER audit this page for WCAG 2.2 AA compliance

@THERION_ANIMATION_SPECIALIST write a Framer Motion spring animation for a modal entrance

@THERION_PWA_ENGINEER set up a service worker with Stale-While-Revalidate for API calls

@THERION_PERFORMANCE_ANALYST analyze this bundle and find the biggest culprits

@THERION_STATE_MANAGER design a Zustand store for a multi-step wizard form

# Cross-cutting queries (routes to THERION_FRONTEND_MASTER, may delegate)
How should I structure TypeScript types for a component library with Tailwind?
What's the best approach for theming — CSS variables or Tailwind dark: variants?
Design a PWA offline-first strategy for our React dashboard application
Set up a complete design token pipeline from Figma to Tailwind config

# Multi-agent coordination
@THERION_FRONTEND_MASTER coordinate: @THERION_UI_DESIGNER design the component API,
@THERION_CSS_ARCHITECT style it with Tailwind tokens, @THERION_UX_ENGINEER add a11y support
```
