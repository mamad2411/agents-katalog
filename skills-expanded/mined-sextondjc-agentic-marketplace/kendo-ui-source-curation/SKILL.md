---
name: kendo-ui-source-curation
description: Use when Kendo UI guidance requires Telerik-first evidence across jQuery, Angular, React, and Vue variants with release-history, licensing, and component-contract drift controls.
---

# Kendo UI Source Curation

## Specialization

Build a Telerik-first evidence set centered on commercial release cadence, framework-variant divergence, licensing implications, and component contract drift across the Kendo product line.

This specialization follows `What's New`, `kendo-ui-core`, and variant docs to expose platform-specific breakpoints for Grid/DataSource behavior, theme changes, and upgrade risk.

This skill governs source selection and skill grounding only. It does not implement Kendo UI components or configure projects.

## Objective

Produce a Kendo UI source dossier that separates stable vendor guidance from variant-specific caveats for components, DataSource, theming, accessibility, migration, and security.

## Trigger Conditions

- A new Kendo UI skill or policy needs source grounding.
- Existing Kendo UI skill references may be stale after a Kendo UI version release.
- A quality gate or implementation workflow needs refreshed source evidence before proceeding.
- Any downstream Kendo UI skill requires a source-freshness check.
- A project is adopting a new Kendo UI major version or migrating between framework variants (jQuery → Angular → React).
- A security advisory or CVE has been published for a Kendo UI or Progress dependency.

## Scope Boundaries

In scope:

- Source selection, authority classification, and freshness checks for Kendo UI and its immediate ecosystem.
- Mapping source content into actionable guidance deltas for downstream Kendo UI skills.
- Rejected-source recording with explicit reason codes.
- Version-aware curation for Kendo UI core changes, deprecated API removals, component interface shifts, and licensing changes.
- Framework variant tracking: Kendo UI for jQuery, Kendo UI for Angular, KendoReact, Kendo UI for Vue.

Out of scope:

- Direct implementation of Kendo UI components or configuration files.
- Framework-specific integration patterns beyond what official docs cover.
- Non-Kendo UI frontend tooling unless it directly gates a Kendo UI capability phase.

## Inputs

- Target Kendo UI topics and expected output artifacts.
- Evaluation date in ISO format (`YYYY-MM-DD`).
- Freshness threshold in days (default: 30).
- Current Kendo UI version and framework variant in the project (if applicable).
- Existing source inventory if available (`./references/source-catalog.md`).

## Required Outputs

- Updated source catalog (`./references/source-catalog.md`) with authority, freshness, relevance, and actionability fields.
- Topic-to-source coverage matrix across: components, DataSource, theming, accessibility, forms, security, performance, migration, and testing.
- Rejected-source table with deterministic reason codes.
- Prioritized guidance deltas grouped by: API changes, deprecated removals, theming contract changes, accessibility advisories, and security notices.
- Version-impact note describing any Kendo UI behavior changes relevant to existing skills.

## Authoritative Source Registry

| Source | Authority | Domain | URL |
|---|---|---|---|
| Kendo UI for jQuery Docs | Primary | Full component API — Grid, Chart, Scheduler, Editor, DataSource, MVVM | https://docs.telerik.com/kendo-ui/introduction |
| Kendo UI API Reference | Primary | Detailed method, event, and option contracts per component | https://docs.telerik.com/kendo-ui/api/javascript/ |
| Kendo UI Live Demos | Primary | Runnable component examples with source code | https://demos.telerik.com/kendo-ui/ |
| Kendo UI GitHub (kendo-ui-core) | Primary | OSS subset — changelogs, issues, source code | https://github.com/telerik/kendo-ui-core |
| What's New / Release History | Primary | Version changelog, breaking changes, deprecation notices | https://www.telerik.com/support/whats-new/kendo-ui |
| KendoReact Docs | Primary | React component suite, design system, hooks API | https://www.telerik.com/kendo-react-ui/components |
| Kendo UI for Angular Docs | Primary | Angular component suite, module system, CDK integration | https://www.telerik.com/kendo-angular-ui/components |
| Kendo UI for Vue Docs | Primary | Vue component suite, composition API patterns | https://www.telerik.com/kendo-vue-ui/components |
| Progress Virtual Classroom | Primary | Structured courses on Kendo UI implementation | https://learn.telerik.com |
| Telerik Blog (Kendo UI) | First-party | Release articles, how-to guides, upgrade announcements | https://www.telerik.com/blogs/kendo-ui |
| Progress Community Forums | First-party | Peer Q&A, official team responses, known issue threads | https://www.telerik.com/forums/kendo-ui |
| OWASP XSS Prevention Cheat Sheet | Standard | Security baseline for template-injected content in Kendo UI widgets | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html |
| OWASP CSRF Prevention Cheat Sheet | Standard | CSRF token handling in DataSource transport requests | https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html |
| WAI-ARIA Authoring Practices Guide | Standard | ARIA pattern baseline for Kendo UI accessibility compliance | https://www.w3.org/WAI/ARIA/apg/ |
| MDN Web Docs | Supporting | DOM, CSS, and browser API context for native-vs-Kendo decisions | https://developer.mozilla.org |

## Source Decision Rules

- `accept`: authoritative source, freshness within threshold, directly actionable.
- `accept-with-watch`: authoritative and relevant but partial, stale, or pending update.
- `reject`: not authoritative, too stale, redundant, or non-actionable.

## Rejected Source Reasons

| Code | Meaning |
|---|---|
| `NOT-AUTHORITATIVE` | Source is community-written with no official affiliation |
| `STALE` | Source exceeds freshness threshold and no update is pending |
| `REDUNDANT` | Content already covered by an accepted source with higher authority |
| `FRAMEWORK-MISMATCH` | Source covers a different Kendo UI framework variant than the target |
| `NON-ACTIONABLE` | Content is conceptual only with no implementable guidance |

## Coverage Matrix Template

| Topic | Primary Source | Supporting Source | Freshness Status |
|---|---|---|---|
| Grid component | Kendo UI API Reference | Live Demos | Verify on each run |
| DataSource patterns | Kendo UI for jQuery Docs | Telerik Blog | Verify on each run |
| SASS theming | Kendo UI for jQuery Docs | What's New | Verify on each run |
| Accessibility | Kendo UI Docs + WAI-ARIA APG | OWASP | Verify on each run |
| Form validation | Kendo UI API Reference | Live Demos | Verify on each run |
| Security | OWASP XSS + CSRF | kendo-ui-core GitHub | Verify on each run |
| Performance | Kendo UI Docs | Telerik Blog | Verify on each run |
| Migration | What's New + GitHub changelog | Telerik Blog | Verify on each run |
| Testing | Kendo UI Docs | Progress Community | Verify on each run |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Verify one source for one Kendo UI topic | One source accepted or rejected with reason code |
| L2 Baseline | Full coverage matrix for a target framework variant | All nine topic areas have at least one accepted source |
| L3 Hardening | Version-locked source catalog with drift detection | Catalog includes version-impact note and rejected-source table |
| L4 Expert Standardization | Reusable source catalog powering all Kendo UI skills | Catalog is cited by every downstream skill without re-fetch |
