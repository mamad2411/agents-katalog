---
name: product-design
description: Use when shaping a new product, materially redesigning a user flow, choosing a web or app stack, or turning a product concept into an implementation-ready design.
---

# Product design

Turn an early product idea into a user experience and an implementation boundary before code is written.

## 1. Users and flows first

Settle who it is for and what they must get done before any technology: the primary user, the platform, the problem removed, the two or three highest-value flows, and the minimum states (and screens, if visual) that complete them. Start from the job, not a feature list; invent no needs. Wireframes or exact flow maps set the implementation boundaries: an unresolved UX decision is an unresolved requirement, not a detail.

## 2. Stack from the product

Tie every choice to a product constraint: a server-rendered or hybrid framework for SEO-heavy public content; an SPA for an authenticated dashboard; a native or cross-platform stack for device-heavy mobile; the smallest runtime for a local developer tool. Among fitting stacks, prefer the one with a mature component ecosystem; do not rebuild standard UI primitives. Weigh build speed, maintenance, hosting, accessibility and ecosystem; scale only when scale is a real requirement.

## 3. Frontend first

Build screens and states with mocked data, run the main flows end to end, derive the data contracts the UI actually needs, then build backend, storage and auth against them and replace the mocks. The frontend exposes missing product decisions before the backend hardens around them. For a coupled product built with AI help, default to one monorepo (`apps/`, `packages/`, `docs/product/`); split only for real deployment, ownership or security boundaries.

## Output

Use what is known; ask only what would change the architecture. For a full brief return, in order (for a narrow question, only the relevant part; for CLI, API or background products, commands, requests and failure paths instead of screens):

1. **Flows and screens:** each flow as `entry → state → action → next state → completion/failure`, then the minimum screen set and each screen's purpose.
2. **Stack:** the choice, each part justified by a product need, and one credible alternative with why it lost.
3. **Build order:** from mocked interface to integrated product, marking where backend, persistence, auth, external APIs, tests and deployment first become necessary.
4. **Repository layout:** the minimum useful structure.

Keep the first build small enough to test the core assumption; no roadmap before the core flows work.
