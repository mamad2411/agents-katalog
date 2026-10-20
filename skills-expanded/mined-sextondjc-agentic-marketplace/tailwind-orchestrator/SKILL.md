---
name: tailwind-orchestrator
description: Use when a TailwindCSS request spans multiple capability areas — setup, component design, quality, or migration — and needs one deterministic intake, explicit phase ownership, and a unified execution contract.
---

# TailwindCSS Orchestrator

## Specialization

Use this skill to coordinate cross-cutting TailwindCSS requests from one intake when work spans source curation, setup and migration, component design, and quality gating.

This skill is specialized for intake, phase ownership, and unified synthesis. It does not replace deep execution guidance; it routes to the appropriate specialist Tailwind skill for each phase.

**Design language model**: When shadcn/ui is present in the project, shadcn is the primary design language for component tokens and brand color. Tailwind is fully active for layout, responsive design, prose, animation, and utility composition on non-component surfaces. Route component token and color system decisions to the `shadcn-*` skill family. Use this skill for Tailwind-specific concerns (build pipeline, content scanning, class ordering, CSS purge, CI integration, design system tokens on non-shadcn surfaces). The two skill families are complementary — coordinate rather than replace.

## Objective

Produce one deterministic TailwindCSS execution contract from a single intake — with explicit phase ownership, evidence expectations, and closure checks — for any request that spans more than one Tailwind capability area.

## Trigger Conditions

- A TailwindCSS request spans more than one capability area (e.g., migration + component redesign + quality gate).
- A project is adopting Tailwind for the first time and needs end-to-end guidance.
- A cross-project Tailwind standard must be established (design tokens, accessibility baseline, class-ordering policy).
- An existing Tailwind implementation needs a full-cycle review: sources → setup → components → gate.
- A team needs one intake instead of disconnected setup, design, and review workflows.

## When Not to Use

- The request is clearly scoped to one phase (use the specialist skill directly).
- Source-only freshness verification with no implementation (use `tailwind-source-curation` directly).
- A single component needs review without a broader gate (use `tailwind-quality-gate` directly).

## Scope Boundaries

In scope:

- Deterministic Tailwind intake and phased execution planning.
- Phase-output ownership with exactly one owner per required output.
- Unified execution recommendation for mixed Tailwind requests.
- Cross-phase dependency mapping (source freshness → setup → design → gate).

Out of scope:

- Deep implementation within any one phase.
- Non-Tailwind CSS tooling unless it directly gates a Tailwind phase.
- Generic frontend project governance unrelated to Tailwind.

## Inputs

- User objective and target Tailwind surface (new project, migration, component library, audit).
- Framework and TailwindCSS version in use or target version.
- Scope boundaries, environments, and risk level.
- Required outputs, known constraints, and delivery timeline.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness.

## Required Outputs

- Intake contract with objective, boundaries, and required outputs.
- Phase-output ownership matrix.
- Unified TailwindCSS execution recommendation.
- Rejected-phase table with deterministic reason codes (phases excluded from scope).
- Closure check stating whether all required outputs are owned.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Route one mixed Tailwind request | One intake and one phase contract exist |
| L2 Delivery | Coordinate a cross-phase Tailwind effort | Every required output has one owning phase |
| L3 Hardening | Support production-grade Tailwind delivery | Risks, evidence expectations, and blockers are explicit |
| L4 Expert Standardization | Establish reusable Tailwind operating model | Reusable intake, token conventions, accessibility baseline, and CI quality policy documented |

## Tailwind Capability Catalog

| Phase | Specialist Skill | When Active |
|---|---|---|
| Source Curation | `tailwind-source-curation` | First adoption, major version update, or source freshness check required |
| Setup and Migration | `tailwind-setup` | New project, v3 → v4 migration, or build-pipeline audit |
| Component Design | `tailwind-component-design` | New component work, design token strategy, dark mode, or accessibility pass |
| CI Integration | `tailwind-ci-integration` | Automated bundle, ordering, content-scan, or Lighthouse CI thresholds need to be established or audited |
| Design System | `tailwind-design-system` | Shared token package serves two or more apps; token versioning, deprecation, or cross-app consistency governance needed |
| Quality Gate | `tailwind-quality-gate` | Pre-merge, pre-staging, or pre-production promotion review |

## Deterministic Workflow

1. Lock objective, risk boundary, target framework/version, and required outputs.
2. Classify the request into one or more capability phases from the catalog above.
3. Determine whether source freshness must be confirmed before other phases begin.
4. Assign exactly one owner per required output.
5. Reject any phase plan with unowned or multiply owned outputs.
6. Define inter-phase dependencies: source curation must complete before setup if version caveats exist; setup must complete before component design if config is changing; CI integration and design system phases may run in parallel with component design once setup is complete; quality gate runs last.
7. Produce one unified execution recommendation: `narrow-execution` (single phase), `phased-execution` (two or more sequential phases), or `stop-pending-blockers`.
8. Publish closure status with residual risks and unresolved blockers.

## Phase-Output Ownership Matrix Template

| Required Output | Owning Phase | Specialist Skill | Evidence Expectation |
|---|---|---|---|
| Source freshness and version-impact decision | Source Curation | `tailwind-source-curation` | Source catalog dated within threshold; v4 breaking-change notes present |
| Installation and config correctness | Setup and Migration | `tailwind-setup` | Build output purged; config model matches target version; CSP note present |
| v3 → v4 migration completion | Setup and Migration | `tailwind-setup` | Visual regression clean; automated upgrade tool run; no JS config remnants |
| Design token map and component patterns | Component Design | `tailwind-component-design` | `@theme` block covers all semantic roles; dark mode contract complete |
| Accessibility annotation for components | Component Design | `tailwind-component-design` | Contrast, focus-visible, and reduced-motion checks documented per component |
| Automated CI enforcement (bundle, ordering, Lighthouse CI) | CI Integration | `tailwind-ci-integration` | All gate checks run on every PR; artifact storage contract defined; noise-reduction controls applied |
| Shared token package architecture and versioning policy | Design System | `tailwind-design-system` | Three-layer taxonomy documented; semver policy and breaking-change matrix in place; cross-app consistency audit complete |
| Quality gate verdict and findings | Quality Gate | `tailwind-quality-gate` | All five gate dimensions with findings table and GO/NO-GO recommendation |

## Unified Decision Rules

- If the request is a new project on v4: run Source Curation → Setup → Component Design → Quality Gate in sequence.
- If the request is a v3 → v4 migration of an existing project: start at Setup (migration workflow); run Quality Gate after.
- If the request is a component library design or update with no config changes: start at Component Design; run Quality Gate after.
- If the request is a quality audit only: run Quality Gate; invoke Source Curation only if version staleness is suspected.
- If source curation reveals a breaking change that affects the target version: block downstream phases until curation is complete.
- If the project serves multiple apps from a shared token package: activate Design System phase before Component Design; Component Design consumes the token package output.
- If CI enforcement is not yet in place for the project: activate CI Integration phase alongside or immediately after Setup; do not defer to Quality Gate only.

## Rejected-Phase Reason Codes

| Code | Meaning |
|---|---|
| `P1` | Phase not relevant to declared objective |
| `P2` | Phase already completed in a prior session with current evidence |
| `P3` | Phase scope falls outside declared boundary |
| `P4` | Phase blocked by unresolved prior-phase dependency |

## Done Criteria

- [ ] Intake contract records objective, boundaries, and required outputs.
- [ ] Phase-output ownership matrix is complete; every output has exactly one owning phase.
- [ ] Rejected phases are recorded with reason codes.
- [ ] Unified execution recommendation is explicit (`narrow-execution`, `phased-execution`, or `stop-pending-blockers`).
- [ ] Closure check confirms all required outputs are owned or explicitly deferred.

## References

- [Source Catalog](./references/source-catalog.md)
- [tailwind-source-curation](../tailwind-source-curation/SKILL.md)
- [tailwind-setup](../tailwind-setup/SKILL.md)
- [tailwind-component-design](../tailwind-component-design/SKILL.md)
- [tailwind-ci-integration](../tailwind-ci-integration/SKILL.md)
- [tailwind-design-system](../tailwind-design-system/SKILL.md)
- [tailwind-quality-gate](../tailwind-quality-gate/SKILL.md)


