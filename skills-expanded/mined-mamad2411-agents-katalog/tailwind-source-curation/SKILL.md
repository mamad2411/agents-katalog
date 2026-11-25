---
name: tailwind-source-curation
description: Use when TailwindCSS guidance must be grounded in authoritative, current sources and converted into reusable, agent-usable Tailwind skill inputs with freshness and drift controls.
---

# TailwindCSS Source Curation

## Specialization

Curate authoritative TailwindCSS guidance into deterministic, reusable skill inputs while enforcing official-source-first policy and explicit freshness controls.

This skill governs Tailwind source selection and skill grounding only. It does not implement components or author configuration files.

## Objective

Produce a TailwindCSS evidence baseline with explicit decisions for configuration, v4 migration, component patterns, accessibility, performance, and build-pipeline integration that downstream Tailwind skills can cite without re-fetching.

## Trigger Conditions

- A new Tailwind skill or policy needs source grounding.
- Existing Tailwind skill references may be stale after a v4 release or major tooling update.
- A quality gate or setup workflow needs refreshed source evidence before proceeding.
- The `tailwind-setup`, `tailwind-component-design`, or `tailwind-quality-gate` skills require a source-freshness check.

## Scope Boundaries

In scope:

- Source selection, authority classification, and freshness checks.
- Mapping source content into actionable guidance deltas for downstream Tailwind skills.
- Rejected-source recording with explicit reason codes.
- Version-aware curation for TailwindCSS v3 → v4 API and config changes.

Out of scope:

- Direct implementation of components or configuration files.
- Framework-specific curation beyond what Tailwind official docs and guides cover.
- Non-Tailwind CSS tooling unless it directly gates a Tailwind build step.

## Inputs

- Target Tailwind topics and expected output artifacts.
- Evaluation date in ISO format (`YYYY-MM-DD`).
- Freshness threshold in days (default: 30).
- Existing source inventory if available.

## Required Outputs

- Updated source catalog (`./references/source-catalog.md`) with authority, freshness, relevance, and actionability fields.
- Tailwind topic-to-source coverage matrix.
- Rejected-source table with deterministic reason codes.
- Prioritized guidance deltas grouped by: setup and config, v4 migration, component design, accessibility, performance, and build pipeline.
- Version-impact note describing any TailwindCSS behavior changes relevant to existing Tailwind skills.

## Authoritative Source Registry

| Source | Authority | Domain | URL |
|---|---|---|---|
| TailwindCSS Official Docs | Primary | All utilities, config, plugins, dark mode, responsive | https://tailwindcss.com/docs |
| TailwindCSS v4 Upgrade Guide | Primary | Breaking changes, new config model, CSS-first config | https://tailwindcss.com/docs/upgrade-guide |
| TailwindCSS GitHub Releases | Primary | Changelogs, API changes, deprecation notices | https://github.com/tailwindlabs/tailwindcss/releases |
| TailwindCSS Blog | First-party | Major feature rationale and release announcements | https://tailwindcss.com/blog |
| Headless UI Docs | First-party | Accessible component interaction patterns with Tailwind | https://headlessui.com |
| Prettier Plugin for Tailwind | First-party | Class-ordering rules and consistency enforcement | https://github.com/tailwindlabs/prettier-plugin-tailwindcss |
| TailwindCSS + Vite Setup | First-party | Canonical Vite integration and PostCSS chain | https://tailwindcss.com/docs/installation/using-vite |
| TailwindCSS Framework Guides | First-party | SvelteKit, Next.js, Vue, Nuxt, Astro integration steps | https://tailwindcss.com/docs/installation/framework-guides |
| web.dev Core Web Vitals | Vendor | Performance thresholds for CSS delivery quality gates | https://web.dev/vitals |
| WCAG 2.2 | Standard | Contrast, focus-visible, and keyboard requirements | https://www.w3.org/TR/WCAG22/ |
| MDN CSS Reference | Standard | Fallback canonical source for utility semantics and browser behavior | https://developer.mozilla.org/docs/Web/CSS |
| Awesome Tailwind CSS | Community | Plugin and tooling discovery (accepted for discovery only) | https://github.com/aniftyco/awesome-tailwindcss |

## Source Decision Rules

- `accept`: authoritative source, freshness within threshold, directly actionable.
- `accept-with-watch`: authoritative and relevant but partial, stale, or pending update.
- `reject`: not authoritative, too stale, redundant, or non-actionable.

## Rejected Source Reasons

- `R1`: Not authoritative for TailwindCSS behavior.
- `R2`: Older than freshness threshold without durable applicability.
- `R3`: Redundant with no new actionable guidance.
- `R4`: Opinion-heavy with low implementation specificity.
- `R5`: Outside TailwindCSS or directly-coupled build-pipeline scope.

## Topic-to-Source Coverage Map

| Topic | Primary Source | Secondary Source |
|---|---|---|
| CSS-first config (v4 `@theme`, `@import`) | TailwindCSS Official Docs | TailwindCSS v4 Upgrade Guide |
| v3 → v4 migration and breaking changes | TailwindCSS v4 Upgrade Guide | TailwindCSS GitHub Releases |
| Responsive breakpoints and container queries | TailwindCSS Official Docs | MDN CSS Reference |
| Dark mode strategy (class vs. media) | TailwindCSS Official Docs | TailwindCSS Blog |
| Arbitrary values and custom utilities | TailwindCSS Official Docs | TailwindCSS GitHub Releases |
| Plugin authoring and extension | TailwindCSS Official Docs | TailwindCSS GitHub Releases |
| Headless UI component interaction patterns | Headless UI Docs | WCAG 2.2 |
| Class ordering and code consistency | Prettier Plugin for Tailwind | TailwindCSS Official Docs |
| Vite and PostCSS build pipeline | TailwindCSS + Vite Setup | TailwindCSS Official Docs |
| Framework-specific setup (SvelteKit, Next.js) | TailwindCSS Framework Guides | TailwindCSS + Vite Setup |
| CSS bundle size and content scanning | TailwindCSS Official Docs | web.dev Core Web Vitals |
| Color contrast and accessibility compliance | WCAG 2.2 | TailwindCSS Official Docs |
| Core Web Vitals impact from CSS delivery | web.dev Core Web Vitals | MDN CSS Reference |
| Plugin and community tooling discovery | Awesome Tailwind CSS | TailwindCSS Official Docs |

## Deterministic Workflow

1. Enumerate target Tailwind topics that must be covered for the requesting skill or task.
2. Classify each candidate source by domain coverage using the authority registry.
3. Evaluate freshness: check publication or last-reviewed date against threshold.
4. Accept, accept-with-watch, or reject each source using the decision rules.
5. Extract testable, actionable guidance deltas from accepted sources.
6. Produce a version-impact note for any TailwindCSS v4 behavior changes that affect existing skills.
7. Write updated source catalog at `./references/source-catalog.md`.
8. Return topic coverage matrix and prioritized deltas to the requesting skill or operator.

## Done Criteria

- [ ] Source catalog is complete with all active sources evaluated and dated.
- [ ] All in-use sources are official-first and freshness-checked.
- [ ] Topic coverage matrix covers all topics requested by the downstream skill.
- [ ] Rejected sources are recorded with explicit reason codes.
- [ ] Version-impact note is present for any v4 API or config changes.
- [ ] Guidance deltas are grouped and prioritized for downstream consumption.
