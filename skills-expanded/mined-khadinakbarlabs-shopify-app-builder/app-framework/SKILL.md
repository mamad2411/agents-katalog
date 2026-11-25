---
name: app-framework
description: "Build a maintainable Shopify app foundation: framework choice, routes, shop-isolated data, migrations, jobs, tests, configuration and hosting boundaries. Use after setup or when extending an existing app."
---

# Build a foundation you can maintain

A framework supplies routing, rendering and Shopify integration. A database stores app-owned data; a background job processes work outside a page request.

## Start here

For a new embedded app, follow the current official Shopify CLI scaffold and React Router integration, including current App Home/Polaris web component setup. Do not make a beginner choose a custom stack unless a concrete requirement needs it.
For an existing app, inspect package versions, route layout, session storage, tests and hosting. Preserve a supported existing framework rather than forcing a migration.

## Guided workflow

1. Define one merchant task, inputs, output and failure states. Propose the smallest architecture with cost/maintenance tradeoffs.
2. Use [shopify-cli](../shopify-cli/SKILL.md), [app-auth](../app-auth/SKILL.md), [app-bridge](../app-bridge/SKILL.md) and [polaris-ui](../polaris-ui/SKILL.md) for the first authenticated embedded page.
3. Model data ownership by shop, input validation, database constraints and query authorization. Every read/write must use the authenticated shop, not a client-supplied shop ID alone. Use parameterized access and avoid mass assignment.
4. Add migrations and test fixtures; rehearse migrations with backup/recovery. Keep app configuration/secret injection separate from browser code and public source. Do not inspect local credentials to configure an app.
5. Put slow syncs in durable jobs with deduplication, bounded retries, observable status and cleanup on uninstall. Authenticate callbacks; fail safely when dependencies are unavailable.
6. Test before expanding features: unit rules, auth and shop-isolation integration tests, error handling and the primary end-to-end dev-store journey.
7. Choose hosting only when needed; explain Shopify deploy manages configuration/extensions, while the app server/database need their own host. Obtain approval before provisioning or changing production.

## Check it worked

A new merchant can install, reach first value, recover from an error and reopen saved state. A second shop cannot read the first shop's data. Tests cover denied/invalid requests, duplicate jobs and migration boundaries. Build/type checks and live dev-store QA are separate evidence.

## If you get stuck

Work locally with mocks/synthetic fixtures when accounts are unavailable, and label those results. Do not create a paid database or change an existing deployment to unblock a local prototype without authorization.

Use [app-release-readiness](../app-release-readiness/SKILL.md) before calling this production-ready.
Sources: [official scaffold](https://shopify.dev/docs/apps/build/scaffold-app), [React Router app guide](https://shopify.dev/docs/apps/build/build), [App Home](https://shopify.dev/docs/api/app-home).
