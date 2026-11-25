---
id: "frontend.ui-engineering"
name: "Frontend Architecture & UI/UX Engineering"
version: "1.2.0"
domain: "frontend"
description: "Engineer production-grade frontend architectures, design systems, accessible UI components, state machines, and optimal Core Web Vitals with minimal token overhead."
triggers:
  - "Designing UI component hierarchies or design systems"
  - "Building interactive web applications or frontend features"
  - "Optimizing Core Web Vitals (LCP, CLS, INP) and client performance"
  - "Implementing responsive layouts, dark mode, or accessibility (WCAG 2.1 AA)"
prerequisites:
  - "architecture.system-design"
risk_profile: "medium"
---

# Frontend Architecture & UI/UX Engineering

## Overview
This skill encodes the standards of a Principal Frontend Architect and Staff Design Systems Engineer. It guides AI agents in authoring resilient, accessible, high-performance UI components while minimizing prompt/context bloat through concise architectural patterns.

## 🎯 Token Conservation & High-Yield Heuristics
1. **Component Boundary Precision**: Do not generate 500-line monolithic components. Decompose into focused subcomponents: Presentational (pure UI), Container (data/hooks), and Compound Components.
2. **Deterministic Prop Interfaces**: Define strict TypeScript interfaces for component props before implementation. Prefer discriminated unions for polymorphic components (`type ButtonProps = PrimaryBtn | SecondaryBtn`).
3. **Zero Hallucinated CSS**: Use design tokens or validated utility classes (Tailwind CSS / CSS Variables). Do not output arbitrary pixel values or inline style clutter.
4. **Lean Context State**: Avoid global state dumpsters. Colocate state as close as possible to where it is consumed; use URL search params for bookmarkable UI state.

## 📐 Core Engineering Directives

### 1. Component Architecture & Design Systems
- **Atomic Design Principles**: Organize UI into Atoms (buttons, inputs), Molecules (form fields, search bars), Organisms (navbars, cards, tables), and Templates/Pages.
- **Compound Components Pattern**: Provide flexible composition (`<Dialog>`, `<Dialog.Title>`, `<Dialog.Body>`, `<Dialog.Close>`) rather than ballooning boolean props (`showCloseButton`, `hasHeaderDivider`, etc.).
- **Headless UI Primitives**: Separate logic and accessibility from styling. Leverage Radix UI, Headless UI, or native HTML5 elements (`<dialog>`, `<details>`) whenever possible.

### 2. Accessibility (WCAG 2.1 AA Compliance)
- **Keyboard Navigation**: All interactive elements must be focusable, show distinct focus rings (`focus-visible:ring-2`), and support standard keyboard interactions (`Enter`, `Space`, `Escape`, arrow keys).
- **ARIA Semantics**: Use native semantic HTML elements (`<button>`, `<nav>`, `<main>`, `<article>`) before applying ARIA attributes. Never place click handlers on non-interactive `<div>` or `<span>` without `role="button"`, `tabIndex={0}`, and `onKeyDown`.
- **Color Contrast**: Maintain minimum 4.5:1 contrast for normal text and 3:1 for large text / UI controls.

### 3. Performance & Core Web Vitals
- **Largest Contentful Paint (LCP < 2.5s)**: Preload hero images, avoid client-side rendering cascades for above-the-fold content, use modern image formats (WebP/AVIF).
- **Cumulative Layout Shift (CLS < 0.1)**: Always provide explicit `width` and `height` (or aspect-ratio containers) on images, skeletons, and dynamic embeds.
- **Interaction to Next Paint (INP < 200ms)**: Defer heavy computations off the main thread; use `useTransition` or `startTransition` for non-urgent state updates; avoid synchronous re-renders of huge lists (use virtual scrolling).

### 4. Hydration Safety & Rendering Boundaries
- Avoid accessing `window`, `localStorage`, or `document` during server-side rendering (SSR). Guard with `useEffect` or client-only components.
- Never render non-deterministic content during SSR (e.g. `Date.now()`, random numbers) without proper hydration isolation.

## 🛑 Anti-Rationalization Matrix

| Agent Excuse / Shortcut | Frontend Engineering Reality | Mandatory Action |
|---|---|---|
| *"I'll use a `div` with an `onClick` because it's easier to style."* | Breaks screen readers, keyboard navigation, and browser accessibility trees. | Use a native `<button>` element with appropriate CSS reset or accessibility props. |
| *"I'll store all UI state in global Redux/Zustand."* | Triggers unnecessary re-renders across the entire component tree and bloats memory. | Colocate state in local component state, URL search params, or atomic context. |
| *"I'll skip responsive layout testing; desktop view is fine."* | Over 55% of web traffic is mobile. Layout will break on viewport resize. | Implement mobile-first responsive breakpoints (`sm:`, `md:`, `lg:`) and test touch targets ($\ge 44 \times 44\text{px}$). |
| *"I'll generate inline SVG paths directly in the JSX."* | Clutters code and consumes massive prompt context tokens. | Extract SVGs into standalone icon components or use established icon libraries (Lucide, Heroicons). |

## ✅ Frontend Verification Checklist
- [ ] No layout shift (CLS = 0) during page load or font loading.
- [ ] Full keyboard navigation verified without mouse assistance.
- [ ] Responsive across 320px, 768px, 1024px, and 1440px viewports.
- [ ] Zero console warnings regarding missing keys, duplicate IDs, or hydration mismatches.
- [ ] Strict TypeScript prop contracts with zero `any` types.

