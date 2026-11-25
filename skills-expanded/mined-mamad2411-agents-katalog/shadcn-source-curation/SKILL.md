---
name: shadcn-source-curation
description: Use when shadcn/ui guidance needs CLI-registry, Radix primitive, and token-system evidence with explicit tracking for component API drift and accessibility contract changes.
---

# shadcn/ui Source Curation

## Specialization

Curate shadcn/ui evidence around CLI registry behavior, copy-paste component composition, token semantics, and Radix interaction contracts used in app-level design systems.

This specialization emphasizes `ui.shadcn.com`, Radix primitives, and form-stack dependencies to keep generated guidance aligned with registry drift, dependency updates, and accessibility contracts.

This skill governs source selection and skill grounding only. It does not implement components or configure projects.

## Objective

Produce a shadcn/ui reference pack that clarifies install-time choices, component-copy patterns, token behavior, Radix dependencies, and accessibility-sensitive API changes for downstream shadcn skills.

## Trigger Conditions

- A new shadcn skill or policy needs source grounding.
- Existing shadcn skill references may be stale after a CLI or component catalog update.
- A quality gate or setup workflow needs refreshed source evidence before proceeding.
- The `shadcn-setup`, `shadcn-component-design`, `shadcn-theming`, `shadcn-forms`, or `shadcn-quality-gate` skills require a source-freshness check.
- A new framework integration target is being added (e.g., SvelteKit, Astro, TanStack Start).

## Scope Boundaries

In scope:

- Source selection, authority classification, and freshness checks for shadcn/ui and its dependency surface.
- Mapping source content into actionable guidance deltas for downstream shadcn skills.
- Rejected-source recording with explicit reason codes.
- Version-aware curation for CLI changes, component API changes, and Radix Primitives updates.

Out of scope:

- Direct implementation of components or configuration files.
- Framework-specific setup steps beyond what official docs cover.
- Non-shadcn UI tooling unless it directly gates a shadcn capability phase.

## Inputs

- Target shadcn/ui topics and expected output artifacts.
- Evaluation date in ISO format (`YYYY-MM-DD`).
- Freshness threshold in days (default: 30).
- Existing source inventory if available.

## Required Outputs

- Updated source catalog (`./references/source-catalog.md`) with authority, freshness, relevance, and actionability fields.
- Topic-to-source coverage matrix across: setup, components, theming, forms, accessibility, and quality.
- Rejected-source table with deterministic reason codes.
- Prioritized guidance deltas grouped by: CLI and installation, component API, theming model, Radix integration, form patterns, and accessibility.
- Version-impact note describing any shadcn/ui or Radix behavior changes relevant to existing skills.

## Authoritative Source Registry

| Source | Authority | Domain | URL |
|---|---|---|---|
| shadcn/ui Official Docs | Primary | CLI, components, theming, installation | https://ui.shadcn.com/docs |
| shadcn/ui GitHub | Primary | Source, changelogs, issue tracker, component internals | https://github.com/shadcn-ui/ui |
| shadcn/ui Blocks | Primary | Prebuilt layout compositions and page patterns | https://ui.shadcn.com/blocks |
| shadcn/ui Themes | Primary | CSS variable token model, color system | https://ui.shadcn.com/themes |
| shadcn/ui Charts | Primary | Recharts integration with shadcn theming | https://ui.shadcn.com/charts |
| Radix UI Primitives Docs | Primary | Accessibility semantics, state machine behavior, WAI-ARIA patterns | https://www.radix-ui.com/primitives |
| Radix UI Primitives GitHub | Primary | Primitive changelogs and breaking changes | https://github.com/radix-ui/primitives |
| class-variance-authority (CVA) | First-party | Variant definition API, `cva()` patterns | https://cva.style/docs |
| react-hook-form Docs | First-party | Form state management, Controller, FormProvider | https://react-hook-form.com/docs |
| Zod Docs | First-party | Schema validation, `z.infer`, form schema patterns | https://zod.dev |
| cmdk Docs | First-party | Command palette component underlying Command | https://cmdk.dev |
| Lucide React | First-party | Icon library used by default in shadcn components | https://lucide.dev/guide/packages/lucide-react |
| TailwindCSS Docs | Supporting | Utility classes and design token model underlying shadcn styling | https://tailwindcss.com/docs |
| WCAG 2.2 | Standard | Accessibility requirements inherited from Radix primitives | https://www.w3.org/TR/WCAG22/ |
| WAI-ARIA Authoring Practices | Standard | Keyboard and interaction patterns for interactive components | https://www.w3.org/WAI/ARIA/apg/ |
| Awesome shadcn/ui | Community | Plugin and extension discovery (accepted for discovery only) | https://github.com/birobirobiro/awesome-shadcn-ui |

## Source Decision Rules

- `accept`: authoritative source, freshness within threshold, directly actionable.
- `accept-with-watch`: authoritative and relevant but partial, stale, or pending update.
- `reject`: not authoritative, too stale, redundant, or non-actionable.

## Rejected Source Reasons

- `R1`: Not authoritative for shadcn/ui behavior.
- `R2`: Stale beyond freshness threshold with no mitigation.
- `R3`: Redundant — a higher-authority source already covers the same content.
- `R4`: Community content with unverified accuracy for production guidance.

## Workflow

1. Record evaluation date and freshness threshold.
2. Load existing source catalog from `./references/source-catalog.md` if present.
3. Fetch each authoritative source and classify: accept, accept-with-watch, or reject with a reason code.
4. Map each accepted source to the downstream skill phase it informs.
5. Identify guidance deltas since last evaluation: component API changes, CLI changes, Radix version updates.
6. Record rejected sources with reason codes.
7. Produce coverage matrix and confirm every downstream skill topic has at least one accepted source.
8. Emit the version-impact note for any behavior change that affects existing skill recommendations.
9. Write updated `./references/source-catalog.md`.

## Pragmatic Stop Rule

Stop when every downstream skill topic in the coverage matrix maps to at least one `accept` or `accept-with-watch` source, and all guidance deltas are recorded. A bounded exception record is required for any topic with only `accept-with-watch` sources.
