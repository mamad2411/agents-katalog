---
name: marketing-motion-systems
description: "Choreograph landing motion with reduced-motion fallbacks, hero budgets, and transform-only rules."
category: frontend
tags: ["motion", "landing", "a11y", "choreography"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Marketing Motion Systems

> **RU:** Системы motion для маркетинга - Motion лендингов: reduced-motion, hero budget и только transform/opacity.

## 1. Skill Meta
**Name:** Marketing Motion Systems
**Description:** Choreograph landing motion with reduced-motion fallbacks, hero budgets, and transform-only rules.
**When to load:** Use this skill whenever the user asks for help with UI/UX, design systems, web performance, or product frontend agents, especially tasks matching: motion, landing, a11y, choreography.
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
1. A concrete architecture or workflow for **Marketing Motion Systems** tailored to the user's stack.
2. A step-by-step implementation plan with validation gates.
3. Explicit anti-patterns to refuse or rewrite.
4. A short checklist the agent must pass before claiming done.
5. Sample configs, schemas, or code sketches when they unlock speed (complete, not stubbed).


## 5. Execution Sequence
1. Clarify scope for Marketing Motion Systems: inputs, outputs, constraints, and success metrics.
2. Inventory existing data, services, and ownership boundaries.
3. Propose the minimal viable architecture that still meets production constraints.
4. Implement in thin vertical slices with tests or evals at each gate.
5. Measure against the success metrics; document residual risks and follow-ups.


## 6. Domain Depth: Marketing Motion Systems

### Focus
Deliver expert guidance for **Marketing Motion Systems** with production constraints, measurable validation, and explicit risks.

### Approach
1. Frame the problem, success metrics, and non-goals.
2. Inventory constraints (data, latency, compliance, budget, locale).
3. Choose the smallest architecture that meets production bars.
4. Implement/validate in thin slices with gates.
5. Document operations, failure modes, and rollback.

### Domain anchors
- `motion`
- `landing`
- `a11y`
- `choreography`

### Outputs
Architecture/workflow, validation plan, anti-patterns refused, checklist, and concrete configs or sketches when they unlock speed.

## 7. Anti-Patterns (Hard Failures)
- AI-purple gradients, Inter-by-default, three equal feature cards, em-dashes as flourish.
- Cards in the hero; scroll cues; decorative locale/weather strips.
- Animating layout properties (top/left/width/height) or scroll listeners on window.
- Shipping inaccessible charts or keyboard traps in dense desks.
- Optimistic UI without rollback or conflict honesty.

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
- `motion`
- `landing`
- `a11y`
- `choreography`

---
*Syntedge Skills Library - frontend / marketing-motion-systems*
