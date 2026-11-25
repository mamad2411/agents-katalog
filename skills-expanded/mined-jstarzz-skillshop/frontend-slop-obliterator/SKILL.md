---
name: frontend-slop-obliterator
description: "Remove generic AI-generated UI slop and replace it with deliberate product-specific hierarchy, density, components and iconography. Use when AI slop UI, too many cards, generic dashboard."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "frontend"
  version: "0.2.0"
  maintainer: "SkillShop maintainers"
  maturity: "beta"
---

# Frontend Slop Obliterator

Fix the product, not merely its CSS. Start from the user loop and existing design truth, then pull in the smallest specialist source needed for the remaining gap.

## First: classify the surface

Choose one dominant mode before touching component libraries:

- **operate** — dashboard/admin/CRM/ops; optimize hierarchy, density, scan speed, keyboard/touch efficiency;
- **persuade** — landing/marketing; optimize thesis, identity, visual rhythm and selective motion;
- **read** — docs/editorial; optimize typography, measure, navigation and content hierarchy;
- **experience** — immersive/creative/3D; interaction/visual effect may itself be part of the product.

Do not turn an `operate` surface into a marketing page because a flashy component exists.

## Resource budget

Default to **1-3 external resources** for a focused task. Use a fourth only when it owns a distinct job. Never stack several overlapping taste/design skills and call the conflict "more context."

Use local truth first:

```text
existing code/tokens/components
  -> one direction/taste source if needed
  -> one implementation/component source if needed
  -> one verification source if needed
```

Search summaries before source. Fetch/install only the finalist.

## Frontend specialist router

| Need | Route | Notes |
|---|---|---|
| New visual direction | Anthropic `frontend-design` | Good general direction specialist; do not override an existing authoritative product language |
| Searchable palette/type/style/UX knowledge | UI/UX Pro Max | Use when those decisions are unresolved, not as permanent background context |
| Landing/portfolio/redesign anti-slop taste | Taste Skill `design-taste-frontend` | Strong fit for marketing/portfolio/redesign; explicitly not the default for dense dashboards/data tables |
| Normal application primitives | existing project -> shadcn/ui | Behavior/semantics first, then skin to project tokens |
| Wider component discovery/generation | current unified 21st MCP | The old Magic MCP is compatibility-only; do not build new workflows around retired Magic names |
| React / Next implementation quality | Vercel React best-practices skill | Engineering/performance guidance, not aesthetic direction |
| React Native / Expo | Vercel React Native guidelines | Native/mobile implementation and performance |
| Local component-state motion | Motion / Framer Motion | Prefer for ordinary transitions and micro-interactions |
| Timeline/scroll choreography | GSAP | Only when choreography is central, not for routine controls |
| 3D / shader / WebGL | ThreeUI Community | Specialist for immersive/visual surfaces; never a default dashboard dependency |
| Convex component architecture | Convex create-component skill | Only when the project actually uses Convex |
| Design-file truth | Figma MCP | Exact frame/node/variables/components only |
| Browser behavior | Playwright MCP | Navigation/focus/forms/state only; avoid giant automatic snapshots |

Canonical upstreams worth recognizing:

- `https://github.com/anthropics/skills/tree/main/skills/frontend-design`
- `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`
- `https://github.com/Leonxlnx/taste-skill`
- `https://github.com/vercel-labs/agent-skills`
- `https://github.com/MengTo/threeui`

Do not vendor all of those into the task context.

## ThreeUI rule

ThreeUI earns its dependency only when 3D/WebGL/shader behavior is part of the intended experience: immersive hero, visualized data/world, product showcase, or a deliberate rare visual moment.

Prefer the public Community package/repository for normal use:

```bash
npm install @designcodeio/threeui
```

Use a narrow component/subpath import when supported. Hosted MCP/Pro access is optional, not a core dependency.

Before shipping a ThreeUI effect, verify:

- mobile and low-end-device cost;
- reduced-motion behavior;
- lazy loading/code splitting;
- fallback when WebGL/effect assets fail;
- the primary user task remains obvious without the effect.

If those checks fail, the 3D is decoration you cannot afford.

## Product-specific workflow

1. Identify primary user, repeated task, target devices/input methods and real domain constraints.
2. Audit existing components/tokens and production behavior before choosing references.
3. State one visual direction and one density/motion budget.
4. Fix information hierarchy before decoration.
5. Prefer existing semantic primitives; introduce one external component source only for missing capability.
6. Exercise relevant states: loading, empty, error, long content, narrow width, keyboard/touch, permission/offline where applicable.
7. Verify rendered layout/accessibility/performance, then use interactive browser evidence only for behavior that still needs proof.
8. Return reusable system fixes, not a pile of isolated pixel patches.

## Slop tells to remove deliberately

- card-per-thought layouts and nested cards without hierarchy;
- giant generic hero heading + weak tiny copy;
- default purple/blue gradients, glowing blobs, glass everywhere;
- excessive pills, icon tiles, huge radii, decorative grids;
- fake KPI/stat cards that exist only to fill a layout slot;
- mixing icon families or component systems;
- motion on frequent expert actions;
- loading only the happy-path screenshot and ignoring empty/error/mobile states.

## Exit criteria

- primary task/hierarchy is obvious;
- design direction is product-specific rather than library-demo-specific;
- external sources each have a named, non-overlapping job;
- responsive/accessibility/runtime costs are checked where relevant;
- important residual unknowns are explicit;
- no external skill/MCP remains in the workflow merely because it was available.
