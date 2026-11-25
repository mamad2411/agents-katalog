# Documentation Publishing

## Purpose
Build, version, and publish unified documentation sites from canonical Markdown sources with Astro Starlight or Docusaurus: single-source builds, public/internal view separation, link and anchor validation, versioned releases, and sitemap plus redirect management.

## Use when
- Generating a static documentation site from a Markdown corpus (docs/, specs, ADRs, API references).
- Splitting public and internal views of the same canonical sources without duplicating truth.
- Cutting a versioned docs release (v0.4, v0.5) with changelogs and redirects for moved pages.
- Auditing a docs build for broken links, missing sitemap entries, or stale search indexes.

## Do not use when
- Restructuring Markdown for LLM consumption without publishing a site (use `documentation-for-llms`).
- Writing marketing landing pages or blog content calendars.
- Editing application code that happens to live next to docs.

## Required context
- Canonical Markdown sources root and the site generator in use (Astro Starlight 4.x or Docusaurus 3.x, pinned version).
- Public vs internal classification: which sections ship to the public site.
- Hosting target and base URL, e.g. https://docs.prumo.dev with Cloudflare Pages.
- Versioning policy: current stable version, maintenance window for old versions.

## Procedure
1. **Pin the toolchain**: lock the generator version in package.json (e.g. `@astrojs/starlight` 4.14.2), run `npm ci`, and confirm `npm run build` succeeds on a clean checkout before any content change.
2. **Map sources to routes**: define the sidebar/nav config so every canonical Markdown file maps to exactly one route; flag orphan pages reachable only by URL.
3. **Separate views without forking**: implement public/internal separation with build-time env flags or collection filters reading frontmatter `visibility: public|internal`, never by maintaining two copies of a page.
4. **Validate links and anchors**: run the generator's build (which fails on bad relative links) plus lychee over the built output; zero broken links is the merge gate.
5. **Manage versions and redirects**: on release, snapshot the versioned sidebar, add redirect entries for every moved or renamed route, and regenerate sitemap.xml; verify the sitemap lists all public routes and no internal ones.
6. **Publish and smoke-test**: deploy the preview build, check the 10 highest-traffic routes return HTTP 200 with correct canonical tags, then promote to production and run `scripts/verify.sh`.

## Decision rules
- **Build from canonical sources only**: the site generator reads the same Markdown files developers edit; generated copies checked into the repo are prohibited.
- **Never fork public/internal copies**: one page, one file, visibility decided by frontmatter plus build flags.
- **Redirects mandatory on moves**: every renamed or moved public route ships a 301 redirect in the same release.
- **Broken link intolerance**: a build with any broken internal link or anchor is not publishable.
- **Sitemap parity**: sitemap.xml must contain every public route and zero internal routes after each release.

## Evidence required
- Clean production build log (`npm run build`) from a pinned toolchain.
- Link-check report with zero broken links or anchors over the built output.
- Sitemap diff showing route additions, removals, and redirect coverage.
- Passing execution log from `scripts/verify.sh`.
- Post-deploy smoke test: HTTP 200 on the top 10 routes with correct canonical tags.

## Output contract
- Published or preview-deployable documentation site built from canonical sources.
- Version snapshot plus redirect table for the release.
- Build, link-check, sitemap, and smoke-test evidence.

## Stop conditions
- Site builds cleanly, links resolve, sitemap matches public routes, and smoke tests pass.
- Version snapshot and redirects recorded for the release.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the docs owner if a publish requires deleting a public URL with external inbound links.
- Escalate to platform engineering if the hosting provider or CDN blocks the deploy pipeline.
