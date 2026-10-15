---
name: use-stayhydated-github-pages
description: "Adopt, migrate, review, or update a Rust/Dioxus GitHub Pages site that consumes stayhydated/shared. Use for synchronized shared SHA pins, consumer-owned Project or ProjectSite configuration, single-page or multi-route shells, route manifests, mdBook or LLM outputs, Trunk browser demos, static preview, reusable Pages workflows, revision automation, or audit_consumer.py."
---

# Use stayhydated GitHub Pages

## Establish the source of truth

1. Read the consumer repository's guidance and inspect `Cargo.toml`,
   `Cargo.lock`, `justfile`, `web/`, `xtask/`, and `.github/workflows/`.
2. Read `stayhydated/shared` guidance and source at the consumer's pinned full
   SHA. Do not infer signatures from a newer checkout.
3. Record the project slug, canonical URL, Dioxus base path, routes, generated
   directories, books, LLM outputs, browser demos, and default branch.
4. Preserve unrelated worktree changes and treat generated artifacts as build
   outputs.

## Preserve ownership

Shared owns generic Dioxus shells and styles, base-path and route types, static
assembly helpers, and reusable workflows. The consumer owns project identity,
canonical URLs, destinations, routes, optional CSS, demo inputs, and its xtask
sequence.

Keep application routes root-relative. Let Dioxus configuration and shared
routing helpers apply the GitHub Pages project prefix.

## Select the workflow

- For a revision-only update, inspect the pinned API, update all three shared
  dependencies to one full SHA, refresh only those lockfile packages, and run
  the consumer audit.
- For a single-route portal, use `ProjectSite` with
  `StayhydatedSinglePageProjectApp`.
- For a portal that embeds one static demo, use
  `StayhydatedEmbeddedDemoProjectApp` and its manifest preset.
- For a multi-route site, derive application paths from the consumer's
  `Routable` enum and use `StayhydatedProjectApp`.
- For build, asset, demo, preview, deployment, or revision-automation work, load
  the matching section of
  [references/adoption-patterns.md](references/adoption-patterns.md) before
  editing.

Read the full reference for a new adoption or site-wide review. For a narrow
change, load only the relevant section and verify every signature against the
pinned source.

## Apply the shared contract

1. Pin `stayhydated-dioxus`, `stayhydated-site`, and `stayhydated-xtask` to one
   full shared SHA in workspace dependencies.
2. Define consumer-owned `Project` and `ProjectSite` values. Configure the
   Skills command and demo path only when those destinations exist.
3. Keep the web package featureless, enable Dioxus Web directly, and launch with
   `stayhydated_site::launch(web::App)`.
4. Export one `SiteRouteManifest`; use it for both fallback generation and the
   sitemap.
5. Assemble the site with `WebBuildConfig::github_pages`, adding explicit asset
   and demo inputs only when the consumer owns them.
6. Keep `web-build`, `web`, and `web-preview` as distinct repository tasks, with
   the build task producing every prerequisite before final assembly.
7. Use the shared reusable deployment and revision-update workflows. Install
   Trunk or nightly only for demos that require them.

## Ownership rules

- Keep generic visual behavior and CSS in shared. Keep only project-specific
  layout/content CSS in the consumer. The shared Dioxus component theme is a
  bundled asset; do not copy it into `web/public` or `web/dist`.
- Use shared components directly. Do not retain downstream wrappers or copied
  helpers once shared exposes the required API.
- Treat `web/dist`, generated books, llms.txt trees, and built wasm demos as
  generated outputs. Rebuild them through the owning task.
- Keep root-relative application routes separate from the GitHub Pages project
  prefix. Let Dioxus CLI config and shared routing types apply the base path.

## Reference selection

Read [references/adoption-patterns.md](references/adoption-patterns.md) for a
new adoption, a full-site review, or work that changes Cargo, Dioxus, routing,
xtask, preview, or workflow shapes. For a narrow shared-revision update, inspect
the pinned source and affected consumer surfaces first, then load the reference
only when a signature or site contract needs comparison.

## Validate the assembled contract

Follow the reference's validation checklist, then run the bundled
[consumer audit](scripts/audit_consumer.py). Pass the intended commit with
`--expected-shared-revision` and use `--dist` after building the site.

Inspect `web/dist` under the configured base path. The audit checks shared
structure and declared generated routes; retain consumer tests for every static
destination the project promises. When shared itself changes, validate the
focused shared crates and dummy site before validating consumers.
