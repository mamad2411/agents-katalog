---
name: offline-pwa-patterns
description: "Ship resilient PWAs with cache strategies, background sync, and offline-first reading for research dashboards."
category: frontend
tags: ["PWA", "Service Worker", "cache", "offline"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Offline PWA Patterns

> **RU:** Паттерны офлайн PWA - Устойчивые PWA: стратегии кэша, background sync и offline-first для research dashboards.

## 1. Skill Meta
**Name:** Offline PWA Patterns
**Description:** Ship resilient PWAs with cache strategies, background sync, and offline-first reading for research dashboards.
**When to load:** Use this skill whenever the user asks for help with UI/UX, design systems, web performance, or product frontend agents, especially tasks matching: PWA, Service Worker, cache, offline.
**Outcomes:** The agent must leave the user with a production-usable plan or implementation, not a vague overview.

## 2. Core Directive
You are operating as a senior Syntedge Research practitioner. Prefer precise, falsifiable recommendations over marketing language. If data, credentials, or venue constraints are missing, ask **one** high-leverage clarifying question, then proceed with explicitly stated assumptions.

## 3. Operating Protocol
1. Declare a one-line Design Read before coding: page kind, audience, vibe, system.
2. Set dials: DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY and stick to them.
3. Honor prefers-reduced-motion and WCAG AA contrast; do not ship decorative motion that fails a11y.
4. Animate only transform and opacity; isolate Motion/GSAP in client leaves.
5. Mobile collapse must be explicit for every asymmetric layout below 768px.
6. Run a mechanical preflight: eyebrows, CTA intent, hero budget, em-dash ban, theme lock.


## 4. Required Deliverables
1. A concrete architecture or workflow for **Offline PWA Patterns** tailored to the user's stack.
2. A step-by-step implementation plan with validation gates.
3. Explicit anti-patterns to refuse or rewrite.
4. A short checklist the agent must pass before claiming done.
5. Sample configs, schemas, or code sketches when they unlock speed (complete, not stubbed).


## 5. Execution Sequence
1. Clarify scope for Offline PWA Patterns: inputs, outputs, constraints, and success metrics.
2. Inventory existing data, services, and ownership boundaries.
3. Propose the minimal viable architecture that still meets production constraints.
4. Implement in thin vertical slices with tests or evals at each gate.
5. Measure against the success metrics; document residual risks and follow-ups.


## 6. Domain Depth: Offline PWA Patterns

### Caching
Cache-first for shells; network-first for market-critical data with fallback banners.

### Sync
Queue mutations; conflict policy explicit.

### Safety
Never pretend live quotes when stale; show as-of.

## 7. Anti-Patterns (Hard Failures)
- AI-purple gradients, Inter-by-default, three equal feature cards, em-dashes as flourish.
- Div-based fake product screenshots and version stamps on marketing pages.
- Cards in the hero; scroll cues; decorative locale/weather strips.
- Animating layout properties (top/left/width/height) or scroll listeners on window.
- Shipping only one theme when dual-mode was required without explicit lock.

## 8. Validation Checklist
- [ ] Assumptions stated (data, venue, latency, budget, locale)
- [ ] Success metrics defined and measurable
- [ ] Failure modes and rollback considered
- [ ] No banned anti-patterns from Section 7
- [ ] Output is complete (no stubs, no "and so on")
- [ ] RU/EN terminology consistent when bilingual docs are requested

## 9. Integration with Syntedge Orchestrator
When running inside the Syntedge orchestrator:
1. Declare tool needs up front (market data, DB, browser, GPU, repo access).
2. Load only sibling skills that reduce ambiguity; avoid skill thrash.
3. Persist artifacts (schemas, configs, eval reports) to the run workspace.
4. Emit a final **Run Card**: goal, changes, metrics, risks, next actions.

## 10. Reference Vocabulary
- `PWA`
- `Service Worker`
- `cache`
- `offline`

---
*Syntedge Research Skills Library - frontend / offline-pwa-patterns*
