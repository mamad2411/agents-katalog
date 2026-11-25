---
name: domo-app-initial-build-playbook
description: Starting sequence for new Domo custom app builds, including which rules and skills to apply first.
---

# Domo App Initial Build Playbook

## When to use
- Use at project kickoff for a brand-new Domo custom app.
- Use when taking over an existing app and normalizing it to platform best practices.

## Apply these rules first (always-on)
- `rules/core-platform-rule.md`
- `rules/domo-gotchas.md`

## Recommended skill order for initial build
1. `domo-manifest` - define mappings/contracts first.
2. `domo-js` - baseline app shell, navigation, events, environment usage.
3. `domo-dataset-query` (and `domo-data-api`) - data access with query-first patterns.
4. `domo-appdb` - persistent app state/documents.
5. `domo-toolkit-wrapper` - move to typed toolkit clients where useful.
6. `domo-ai-service-layer` / `domo-code-engine` / `domo-workflow` as needed by features.
7. `domo-performance-optimizations` before finalizing queries.
8. `domo-app-publish` for release flow and first-publish ID handling.

## Build-time guardrails
- Client-side only: no SSR/server routes/server components.
- Use Vite `base: './'`.
- Prefer `HashRouter` unless rewrites are intentionally handled.
- Treat `domo.env.*` as convenience only; use verified identity for trust decisions.

## Explicitly separate from connector work
- Do **not** use this playbook for Domo Custom Connector IDE projects.
- Connector projects should use `domo-custom-connector-ide` instead.
