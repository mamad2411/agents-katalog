---
description: FINAL OBJECTIVE — TitanOS is an operating system, not a feature pile
alwaysApply: true
---

# FINAL OBJECTIVE

TitanOS must feel like a **cohesive, enterprise-grade operating system** for workers, contractors, drivers, businesses, and teams — not a web app with many features bolted together.

## Experience bar

Every interaction is:

| Trait | Meaning |
|-------|---------|
| Fast | No junk work; live paths stay responsive |
| Intuitive | Three-question UI; ≤3 taps; clear domain home |
| Visually consistent | Shared chrome, tokens, motion ≤200ms |
| Reliable | Fail closed; honest empty/error/offline |
| Purposeful | Every control earns its place; progressive disclosure |

## Architecture bar

| Trait | Meaning |
|-------|---------|
| Modular | pages → components → `*Api` / barrels → api → shared → migrations |
| Low cognitive load | Domains (Live/History/…), not a flat feature dump |
| AI that helps | Allowlisted, data-grounded, productivity-first — not novelty |
| Scalable | Bounded reads, indexes, rate limits, cloud trips |
| Maintainable for years | MODULE.md, ARCHITECTURE, onboarding, no parallel engines |

## Guiding Principle (ship gate)

**No feature ships until it is secure, performant, intuitive, accessible, thoroughly tested, visually polished, and integrated seamlessly with the rest of TitanOS.**

Incomplete if any of those are “later,” if the screen ignores IA domains / shared chrome, or if Labs/stubs look more live than they are.

## How to apply

1. Place work in the correct **OS domain** (`nav-items.js` group).
2. Reuse **PageShell / PageHeader / Empty·Loader·Error / ExportMenu**.
3. Satisfy the matching product laws under `.cursor/rules/` (security, performance, a11y, testing, visual, …).
4. Prove with tests + honesty banners; document residual risk in `docs/FINAL_QA.md` when ops remains.

Map: `docs/FINAL_OBJECTIVE.md` · QA: `docs/FINAL_QA.md`.
