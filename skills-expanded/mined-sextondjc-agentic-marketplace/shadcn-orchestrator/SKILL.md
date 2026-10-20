---
name: shadcn-orchestrator
description: Use when a shadcn/ui request spans multiple capability areas — setup, theming, component design, forms, data display, testing, accessibility, migration, animation, registry, CI integration, design system, or quality — and needs one deterministic intake, explicit phase ownership, and a unified execution contract.
---

# shadcn Orchestrator

## Specialization

Use this skill to coordinate cross-cutting shadcn/ui requests from one intake when work spans source curation, project setup, theming, component design, form patterns, and quality gating.

This skill is specialized for intake, phase ownership, and unified synthesis. It does not replace deep execution guidance — it routes to the appropriate specialist shadcn skill for each phase.

**Design language model**: shadcn/ui is the primary design language; TailwindCSS is the utility layer. Both are leveraged for their strengths. shadcn CSS variable tokens govern component color, spacing, and border-radius. Tailwind utilities govern layout, responsive breakpoints, prose styling, animation, and non-component surfaces. When both could apply, prefer the shadcn semantic token; use a Tailwind utility only when it provides a capability shadcn does not cover. Conflicts on component tokens are resolved in favor of shadcn. Use `tailwind-orchestrator` for Tailwind-specific build, pipeline, and CI concerns and coordinate with the shadcn skill family when the two surfaces intersect.

## Objective

Produce one deterministic shadcn/ui execution contract from a single intake — with explicit phase ownership, evidence expectations, and closure checks — for any request that spans more than one shadcn capability area.

## Trigger Conditions

- A shadcn/ui request spans more than one capability area (e.g., new project setup + brand theming + form implementation).
- A project is adopting shadcn/ui for the first time and needs end-to-end guidance.
- A cross-project shared component library backed by shadcn/ui must be established.
- An existing shadcn implementation needs a full-cycle review: sources → setup → theming → components → forms → gate.
- A team needs one intake instead of disconnected setup, design, and review workflows.
- A major shadcn/ui or Radix primitives update requires an impact assessment across all capability areas.

## When Not to Use

- The request is clearly scoped to one capability area — use the specialist skill directly.
- Source-only freshness verification with no implementation (use `shadcn-source-curation` directly).
- A single component needs review without a broader gate (use `shadcn-quality-gate` directly).

## Scope Boundaries

In scope:

- Deterministic shadcn intake and phased execution planning.
- Phase-output ownership with exactly one owner per required output.
- Unified execution recommendation for mixed shadcn requests.
- Cross-phase dependency mapping (source freshness → setup → theming → components → forms → gate).

Out of scope:

- Deep implementation within any one phase.
- Non-shadcn UI tooling unless it directly gates a shadcn phase.
- Generic frontend project governance unrelated to shadcn/ui.

## Inputs

- User objective and target shadcn surface (new project, component library, theming, form audit, quality gate).
- Framework and shadcn/ui version in use or target version.
- Scope boundaries, environments, and risk level.
- Required outputs, known constraints, and delivery timeline.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness.

## Required Outputs

- Intake contract with objective, boundaries, and required outputs.
- Phase-output ownership matrix.
- Unified shadcn/ui execution recommendation.
- Rejected-phase table with deterministic reason codes (phases excluded from scope).
- Closure check stating whether all required outputs are owned.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Route one mixed shadcn request | One intake and one phase contract exist |
| L2 Delivery | Coordinate a cross-phase shadcn effort | Every required output has one owning phase |
| L3 Hardening | Support production-grade shadcn delivery | Risks, evidence expectations, and blockers are explicit |
| L4 Expert Standardization | Establish reusable shadcn operating model | Reusable intake, token conventions, component library baseline, and CI quality policy documented |

## shadcn Capability Catalog

| Phase | Specialist Skill | When Active |
|---|---|---|
| Source Curation | `shadcn-source-curation` | First adoption, major CLI or Radix update, or source freshness check required |
| Setup and Configuration | `shadcn-setup` | New project, monorepo layout, framework integration, or `components.json` audit |
| Theming | `shadcn-theming` | Brand palette mapping, dark mode implementation, or multi-theme / white-label work |
| Component Design | `shadcn-component-design` | New component, CVA variants, Radix primitive integration, or cross-project component conventions |
| Data Display | `shadcn-data-display` | DataTable with TanStack Table, Charts with Recharts, Command palette, Combobox, or virtualized list/grid |
| Forms | `shadcn-forms` | Any form with `react-hook-form` + `zod`, multi-step forms, or form accessibility audit |
| CI Integration | `shadcn-ci-integration` | Registry drift detection, bundle gating, import lint, token conformance, or RSC boundary checks in CI |
| Design System | `shadcn-design-system` | Shared component package across multiple apps or monorepo — versioning, token contract, breaking-change governance |
| Testing | `shadcn-testing` | Writing or reviewing component tests — Radix portal queries, keyboard interaction, async assertions, `forceMount` patterns, Storybook `play` functions |
| Accessibility | `shadcn-accessibility` | Per-component ARIA contracts, WCAG 2.2 mapping, focus management, `aria-live` announcements, and screen reader test sequences |
| Migration | `shadcn-migration` | Transitioning from MUI, Chakra UI, Mantine, or Ant Design — equivalence maps, token migration, coexistence configuration, and phase sequencing |
| Animation | `shadcn-animation` | Enter/exit animations with Framer Motion or `tailwindcss-animate`, `forceMount` + `AnimatePresence` for Radix overlays, route transitions, and reduced-motion compliance |
| Registry | `shadcn-registry` | Authoring a custom component registry — `registry.json` schema, item types, hosting, CLI consumption, co-existence with upstream, and versioning strategy |
| Quality Gate | `shadcn-quality-gate` | Pre-merge review, pre-promotion gate, design system audit, or post-update conformance check |

## Deterministic Workflow

1. Lock objective, risk boundary, target framework, and required outputs.
2. Classify the request into one or more capability phases from the catalog above.
3. Assign exactly one owner per required output using the phase assignment table below.
4. Map cross-phase dependencies: source freshness must precede setup; setup must precede theming and components; theming and components must precede gate.
5. Identify phases not active and record them in the rejected-phase table with reason codes.
6. Confirm closure: every required output has an owner.
7. Emit the execution contract.

## Phase Assignment Table

| Required Output Type | Owning Phase |
|---|---|
| Source freshness baseline | Source Curation |
| `components.json`, path aliases, framework wiring | Setup and Configuration |
| CSS variable declarations, dark mode, brand token mapping | Theming |
| TSX components, CVA schemas, Radix wiring, RSC boundaries | Component Design |
| DataTable, Chart, Command, Combobox, virtualized list | Data Display |
| Zod schemas, `useForm` setup, `FormField` compositions, submission handlers | Forms |
| CI checks: drift, bundle, import lint, token scan, RSC lint | CI Integration |
| Shared package architecture, token contract, breaking-change policy | Design System |
| Accessibility verdict, token conformance, bundle health, gate recommendation | Quality Gate |
| Test files, portal query strategy, keyboard maps, Storybook stories | Testing |
| ARIA contracts, WCAG mappings, focus management spec, screen reader sequences | Accessibility |
| Component equivalence map, token migration map, coexistence configuration, phase plan | Migration |
| Animation implementation, variant library, `forceMount` pattern, reduced-motion compliance | Animation |
| `registry.json`, component item files, hosting config, consumer onboarding guide | Registry |

## Cross-Phase Dependency Map

```
Source Curation
    └── Setup and Configuration
            ├── Theming
            │       └── Quality Gate
            ├── Component Design
            │       └── Quality Gate
            ├── Data Display
            │       └── Quality Gate
            ├── Forms
            │       └── Quality Gate
            ├── Design System
            │       ├── CI Integration
            │       └── Quality Gate
            ├── Testing
            │       └── Quality Gate
            ├── Accessibility
            │       └── Quality Gate
            ├── Animation
            │       └── Quality Gate
            ├── Registry
            │       └── Quality Gate
            └── Migration
                    └── Quality Gate
```

- Source Curation is optional when sources are within freshness threshold.
- Theming, Component Design, Data Display, and Forms are independently executable once Setup is complete.
- Design System requires Setup and is typically active in monorepo or multi-app contexts.
- CI Integration requires Setup and may run alongside or after Design System.
- Quality Gate is always the final phase when a merge or promotion decision is required.

## Rejected Phase Reason Codes

| Code | Meaning |
|---|---|
| `P1` | Phase not needed — request is scoped to other phases only |
| `P2` | Phase already complete — evidence exists from a prior session |
| `P3` | Phase deferred — out of current delivery scope; owner identified for future work |
| `P4` | Phase not applicable — framework or project type does not require it |

## Pragmatic Stop Rule

Stop when the intake contract is locked, every required output has exactly one owning phase, rejected phases are recorded, and the closure check passes. A bounded exception record is required for any output with no clear phase owner.


