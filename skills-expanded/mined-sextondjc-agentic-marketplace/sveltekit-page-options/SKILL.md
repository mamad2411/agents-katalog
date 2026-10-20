---
name: sveltekit-page-options
description: Use when configuring SvelteKit rendering behaviour through page options including ssr, csr, prerender, trailingSlash, and the entries function for static prerendering.
---

# SvelteKit Page Options

## Specialization

Expert guidance for SvelteKit page and layout rendering options. Covers the `ssr`, `csr`, `prerender`, and `trailingSlash` exports, the `entries()` function for static route enumeration, inheritance through layout hierarchies, and the trade-offs of each rendering mode.

## Trigger Conditions

- Choosing a rendering strategy for a page or group of pages.
- Enabling or disabling SSR or client-side rendering selectively.
- Prerendering static pages or a full static site export.
- Controlling trailing slash behaviour for SEO or CDN compatibility.
- Diagnosing rendering errors caused by incompatible option combinations.

## Scope Boundaries

In scope:

- `export const ssr = true | false` — server-side rendering toggle.
- `export const csr = true | false` — client-side hydration toggle.
- `export const prerender = true | false | 'auto'` — static prerendering.
- `export const trailingSlash = 'never' | 'always' | 'ignore'`.
- `export const entries = () => RouteDefinition[]` — static route enumeration for dynamic prerendered routes.
- Option inheritance from layout to page and override semantics.
- Interaction between `prerender = true` and load functions (no request-time data).
- Combining `ssr = false` with SPA mode via `adapter-static`.

Out of scope:

- Adapter selection and deployment (covered by `sveltekit-adapters`).
- Load function implementation (covered by `sveltekit-load`).
- Route file structure (covered by `sveltekit-routing`).

## Inputs

- Page types and their data sources (static content, user-specific data, real-time data).
- Deployment target and adapter constraints.
- SEO requirements.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Rendering mode decision | Documented choice per page or layout with rationale |
| Page options exports | Correct `export const` statements in the relevant `+page.ts` or `+layout.ts` |
| `entries()` implementation | Static route list for dynamic prerendered routes |
| Inheritance map | Which options are set at layout level and which override at page level |
| Page options checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Understand what each option does | One option changed and effect verified in dev |
| L2 Practical Delivery | Configure rendering for a multi-page app with mixed strategies | SSR, prerender, and SPA sections each work correctly |
| L3 Specialist Hardening | Optimise rendering for SEO, CDN edge, and performance | Core Web Vitals measured; cache headers aligned; `trailingSlash` matches CDN config |
| L4 Expert Standardisation | Define rendering policy for a project | Per-section rendering policy documented with adapter compatibility matrix |

## Rendering Mode Decision Guide

| Scenario | Recommended Options |
|---|---|
| Marketing page with static content | `prerender = true`, `ssr = true` |
| User dashboard with session data | `ssr = true`, `csr = true`, `prerender = false` |
| Admin SPA with no public indexing need | `ssr = false`, `csr = true`, `prerender = false` |
| Docs site, full static | `prerender = true` in root layout |
| Dynamic routes with finite known paths | `prerender = true` + `entries()` |
| Real-time data page | `ssr = true`, `csr = true`, `prerender = false` |

## Workflow

1. Categorise each page or section by data source: static, session-bound, or real-time.
2. Map each category to a rendering mode using the decision guide above.
3. Set options at the layout level for shared behaviour; override at the page level only where the section differs.
4. For prerendered dynamic routes, implement `entries()` to enumerate all paths at build time.
5. Verify that `prerender = true` pages do not depend on request-time data in load functions.
6. Align `trailingSlash` with CDN and adapter redirect behaviour.
7. Test each rendering mode in development and confirm correct HTML output for SSR pages.
8. For `ssr = false` SPA sections, confirm `adapter-static` or a compatible adapter is in use.
9. Run the page options checklist.

## Page Options Checklist

- [ ] Every page has an explicit or inherited rendering mode decision.
- [ ] `prerender = true` pages do not access `request`, `cookies`, or `locals` in load functions.
- [ ] `entries()` is implemented for every dynamic route with `prerender = true`.
- [ ] `trailingSlash` matches the canonical URL policy enforced by the CDN or hosting platform.
- [ ] `ssr = false` is not applied to pages that require server-rendered HTML for SEO.
- [ ] `csr = false` is only used for fully static pages with no client interactivity.
- [ ] Layout-level options are not overridden at the page level without documented justification.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Rendering mode selection | Rendering Mode Decision Guide |
| Option syntax | Scope Boundaries + Workflow steps 2–3 |
| Dynamic prerendering | Workflow step 4 |
| trailingSlash alignment | Workflow step 6 |
| Constraint validation | Page Options Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
