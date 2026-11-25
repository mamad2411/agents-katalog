---
name: pericles-frontend-foundations
version: 2026.05.0
description: >
  The frontend foundation for Pericles — stack, structure, component pattern, state,
  realtime, and the "intuitive, no onboarding" + accessibility bar. Use this WHENEVER
  you build or change any UI (a page, component, store, or provider) in frontend/.
  Encodes Next.js 16 App Router + React 19, Tailwind + Radix/shadcn-style ui, zustand
  stores, socket.io-client realtime, the existing component layout, and persona framing
  via the Persona Layer.
doctrine_refs: [§6; Atlas/Intelligence/Admin PRDs]
depends_on: [pericles-persona-layer, pericles-tenant-isolation]
last_reconciled: 2026-05-28
---

# Pericles Frontend Foundations (build skill)

Pericles must be usable by a VP of Supply Chain with 30 minutes and no training — the
UI bar is "intuitive, no onboarding." This skill sets the shared conventions so every
surface (Atlas, Intelligence, Plans, Admin, Co-Pilot) feels like one product.

## When to use this skill

Building/changing any page, component, store, or provider in `frontend/`.

## The stack (verified against frontend/package.json)

- **Next.js 16.1 (App Router)** + **React 19.2**. Routes in `src/app/` with groups
  `(auth)` and `(portal)`.
- **Tailwind** (+ `tailwind-merge`, `clsx`, `class-variance-authority`) with **Radix UI**
  primitives and **lucide-react** icons → shadcn/ui-style components in
  `src/components/ui`.
- **zustand** for client state (`src/stores`); **providers** in `src/providers`; shared
  helpers in `src/lib`.
- **@react-google-maps/api** (Atlas), **reactflow** (Plans graph), **socket.io-client**
  (realtime feeds).

## Project structure (as built)

```
frontend/src/
  app/(auth)/   app/(portal)/   app/auth/     # App Router route groups
  components/{ auth, layout, monitoring, ui, workflow }
  lib/   providers/   stores/
```

`components/monitoring` and `components/workflow` already exist (events UI and the Plans
graph builder). Extend these rather than starting parallel trees.

## Component pattern (.claude/rules/08-frontend.md)

Typed functional components with a props interface and Tailwind `className`:

```tsx
interface XProps { /* ... */ className?: string }
export const X: React.FC<XProps> = ({ /* ... */ className = '' }) => { /* ... */ };
```

Compose from `components/ui` primitives; keep server/client component boundaries
explicit (App Router); fetch via the API layer (`pericles` backend; `.claude/rules/09-api.md`).

## Persona framing (not per-persona UIs)

Surfaces differ by persona (Global Risk Manager / Supply Chain Manager / Business
Stakeholder) in **output shape, data scope, default module, vocabulary** — driven by the
**Persona Layer** (`pericles-persona-layer`), not forked components. Build one surface
that renders per persona; enforce data scope (e.g. financial impact to Risk Manager+).

## Tenant & realtime

All data is tenant-scoped server-side (`pericles-tenant-isolation`); never trust a
client-supplied `organization_id`. Realtime feeds (events, monitoring) come over
`socket.io-client`; subscribe per tenant and clean up on unmount.

## Accessibility & quality

WCAG AA (contrast, keyboard nav, focus, ARIA via Radix); responsive; 60 FPS for
interactive surfaces (esp. Atlas). Run `npm run lint` + `type-check` (frontend) before
done.

## What this forbids

Per-persona forked components (use the Persona Layer); trusting a client `organization_id`;
parallel component trees instead of extending `components/*`; inline styles over Tailwind
tokens; shipping a surface that needs onboarding to understand.

## Verification

Components follow the typed-FC + Tailwind pattern; persona differences are
configuration; data is tenant-scoped server-side; realtime subscriptions are
per-tenant and cleaned up; WCAG AA and lint/type-check pass.

## Existing standards (read alongside)

`.claude/rules/08-frontend.md`, `09-api.md`; `.cursor/rules/400-frameworks/{401-next.js,402-react,403-tailwind,416-shadcn-ui}-*`; `frontend/src/components/*`.

## Open questions

- Whether `mobx-react-lite` (in `.cursor/rules`) is used anywhere or if `zustand` is the
  sole store — confirm; the deps show zustand only.
- The API/BFF boundary (Next.js route handlers vs the Express backend) — confirm with
  `.claude/rules/09-api.md`.

## Changelog

- 2026.05.0 — Initial draft; verified the Next.js 16/React 19 stack, structure, and
  existing components against `frontend/`.
