---
name: frontend-patterns
description: Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. Grok-native with hooks, compound, and Production Contract.
when-to-use: When building or reviewing React/Next.js UIs, especially visual-heavy or performance-sensitive frontend tracks in swarms.
---

# Frontend Patterns Skill

High-leverage, production patterns for modern frontend that actually ship and stay maintainable.

## When to Use
- New UI features, dashboards, marketing pages, or complex forms.
- Performance or bundle size concerns.
- Animation, real media, or premium feel requirements.
- In swarms with frontend-dev agent for Phase 3.

## Core Patterns

### 1. App Router + Server Components by Default
- Server components for data fetching and rendering.
- Client components only for interactivity.
- Streaming + suspense for perceived performance.

### 2. State Management
- Server state with React Query / SWR / tRPC.
- URL as source of truth for filters/pagination.
- Local state only for truly ephemeral UI (modals, form drafts).

### 3. Performance
- Image optimization (next/image or equivalent).
- Font & critical CSS inlining.
- Bundle analysis in CI.
- Core Web Vitals as SLOs.

### 4. Motion & Polish (without killing perf)
- Framer Motion for enter/exit, gestures, layout.
- whileInView + reduced motion respect.
- Real assets, not placeholders, with proper optimization.

### 5. Accessibility & Forms
- React Hook Form + Zod.
- ARIA, keyboard, focus management.
- Error states that are actually usable.

## Integration with Grok System
- Pair with frontend-dev agent.
- on_ai_feature when using generated media or LLM copy in UI.
- Record friction for patterns that hurt LCP/INP or caused a11y regressions.
- Pre-flight for visual tracks: "Have we defined performance budget and accessibility baseline?"

## Production Contract
- Pre-Flight: read design system, existing components, perf budget.
- Ledger for complex multi-step UI work.
- Handoff includes data shapes, loading/error states, analytics events.
- Friction + compound for every "this animation looked good but killed mobile perf".

Use these so your beautiful UI actually ships and doesn't become tech debt.