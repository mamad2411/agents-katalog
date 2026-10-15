---
name: ns-code-frontend-design
description: (NS) Distinctive production UI — layout, typography, motion, and component polish that avoids generic AI-slop aesthetics. Use whenever the user builds or refines pages, components, dashboards, forms, or design-brief work, or asks for better UI/UX — even if they do not say "design". Load docs/context/design-brief.md when present. Do NOT use for backend-only work, requirements writing, or full SDD orchestration (use ns-spec-driven).
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.0"
depends:
  - ns-harness
---

# Frontend Design

Ship **distinctive, production-grade UI** — not interchangeable template aesthetics.

## Harness discovery

See `../ns-harness/references/harness-discovery.md`. Read `{harness_root}/rules/architecture-rules.md` and layer-specific frontend rules when present.

## Context to load

| File | When |
| ---- | ---- |
| `docs/context/design-brief.md` | Always check first — tokens, typography, motion |
| `docs/context/stack-confirmed.md` | Framework and CSS approach |
| `{harness_root}/rules/*frontend*` | Project conventions |

If `design-brief.md` is missing, infer stack from architecture rules and ask **one** focused question on brand direction before large UI work.

## When to use

- New pages, layouts, or component libraries
- Visual refresh of existing screens
- Design-brief alignment or token application
- Reducing "generic AI UI" (purple gradients, identical card grids)

## Workflow

1. **Audit** — screenshot or read existing UI patterns in the codebase; note framework (React, Vue, Blade, etc.).
2. **Anchor** — apply `design-brief.md` or establish a minimal direction (type scale, spacing, accent, motion level).
3. **Design** — composition, hierarchy, states (hover, focus, empty, error), responsive breakpoints.
4. **Implement** — minimal diff; match project file structure and naming.
5. **Verify** — keyboard focus, contrast, reduced-motion respect.

See `references/anti-slop.md` and `references/checklist.md`.

## Principles

- **One strong visual idea** per screen — not every trend at once.
- **Typography carries hierarchy** — do not rely on color alone.
- **Motion with purpose** — micro-interactions for feedback, not decoration loops.
- **Accessible by default** — semantic HTML, labels, focus rings.

## Integration with ns-spec-driven

When invoked from the SDD face skill, stay scoped to UI tasks — do not expand into requirements or task generation.

## Forbidden

- Backend API design or database schema
- Replacing `ns-code-reviewer` for MR gates
- Ignoring project CSS/component conventions when they exist
