---
name: backstage-plugin-development
description: >
  Guides authoring a custom Backstage plugin — scaffolding a frontend or
  backend plugin package with `yarn new`, wiring a frontend API client via
  `createApiRef`, building a backend plugin on the new backend system
  (`createBackendPlugin`), and registering either into the app's routes or
  an entity page tab. Use when a user asks to "write a custom Backstage
  plugin," "add a backend plugin to Backstage," "build a Backstage frontend
  component that talks to a new API," or "create a Backstage plugin that
  surfaces X" — this goes beyond catalog/TechDocs/template configuration.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Backstage Plugin Development

## Purpose

Backstage's catalog, TechDocs, and Software Templates cover the platform's
baseline needs, but the moment a platform team wants to surface something
that doesn't already have a plugin — an internal cost-allocation report, a
custom deployment-approval workflow, a proprietary incident tool's live
status — the answer is a custom plugin, not a catalog annotation. Writing
one badly (a frontend page that calls an external API directly with a
hardcoded token, or a backend route bolted onto `packages/backend` instead
of being its own package) creates something that breaks on every Backstage
upgrade and that only the original author can maintain. Writing one well
means treating it as its own versioned package with a defined frontend/
backend contract, so it upgrades alongside Backstage core, other engineers
can extend it, and it fails predictably instead of silently. This skill
covers scaffolding, structuring, wiring, and locally testing a custom
Backstage plugin — it assumes the baseline catalog/TechDocs/Software
Template setup from
[backstage-developer-portal](../../../observability-and-platform-extras/skills/backstage-developer-portal/SKILL.md)
is already in place and does not repeat it.

## When to use

- A team wants a new tab on a `Component`'s catalog page (e.g. "Cost,"
  "Security Findings," "Deploy Approvals") backed by data no existing
  plugin exposes.
- An internal API or service needs a first-class UI inside the developer
  portal instead of a link out to a separate tool.
- A self-service workflow (see
  [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md))
  needs both a backend to call and a frontend surface for developers to
  trigger and monitor it from within Backstage.
- An existing community plugin is close but not quite right, and the team
  needs to understand plugin structure well enough to fork/extend it
  rather than patch it blindly.
- Debugging why a plugin page renders blank, an API client throws
  "no implementation available for apiRef," or a backend plugin never
  starts.

## Prerequisites & environment

- A working Backstage app created via `@backstage/create-app` (or an
  existing monorepo with `packages/app`, `packages/backend`, and a
  `plugins/` directory) — plugin development happens inside that monorepo,
  not as a standalone project.
- Node.js and Yarn versions matching the app's `package.json` `engines`
  field — Backstage pins these tightly, and a mismatched Node version is a
  common source of `yarn new`/`yarn start` failures.
- Backstage CLI tooling available via the monorepo's dev dependencies
  (`@backstage/cli`) — `yarn new` and `yarn start` are invoked through
  Yarn workspace scripts, not a globally installed CLI.
- Familiarity with the **new backend system** (`createBackendPlugin`,
  `coreServices`) — as of Backstage's modern backend (the default for apps
  scaffolded since `@backstage/create-app` moved off the legacy backend in
  its 2023+ releases), the legacy `createRouter`-based backend plugin
  style is deprecated for new plugins; check `packages/backend/src/index.ts`
  to confirm which system the app is on before writing new backend code.
- TypeScript familiarity — Backstage plugins are TypeScript-first, and the
  scaffolded plugin templates assume it.
- Write access to the monorepo (internal plugins are almost always
  committed there, not published to npm).

## Step-by-step guidance

1. **Scaffold a new frontend plugin** with the Backstage CLI's interactive
   generator, run from the monorepo root:
   ```bash
   yarn new
   # ? What do you want to create? Plugin
   # ? Enter an ID for the plugin [component-name] cost-insights-lite
   ```
   This creates `plugins/cost-insights-lite/` with its own `package.json`
   (name `@internal/plugin-cost-insights-lite`), `src/plugin.ts`,
   `src/routes.ts`, and a default page component — a real Yarn workspace
   package, versioned and built independently of `packages/app`.

2. **Scaffold the matching backend plugin** the same way, choosing the
   backend plugin option:
   ```bash
   yarn new
   # ? What do you want to create? Backend plugin
   # ? Enter an ID for the plugin [component-name] cost-insights-lite
   ```
   This creates `plugins/cost-insights-lite-backend/` (package name
   `@internal/plugin-cost-insights-lite-backend`) with a
   `createBackendPlugin` skeleton already wired up — separate package,
   separate lifecycle, so the frontend can be developed and released
   without forcing a backend redeploy and vice versa.

3. **Define the frontend plugin and its route** in `src/plugin.ts` and
   `src/routes.ts`:
   ```typescript
   // plugins/cost-insights-lite/src/routes.ts
   import { createRouteRef } from '@backstage/core-plugin-api';

   export const rootRouteRef = createRouteRef({
     id: 'cost-insights-lite',
   });
   ```
   ```typescript
   // plugins/cost-insights-lite/src/plugin.ts
   import {
     createPlugin,
     createRoutableExtension,
     createApiFactory,
     discoveryApiRef,
     fetchApiRef,
   } from '@backstage/core-plugin-api';
   import { rootRouteRef } from './routes';
   import { costInsightsApiRef, CostInsightsClient } from './api';

   export const costInsightsLitePlugin = createPlugin({
     id: 'cost-insights-lite',
     routes: { root: rootRouteRef },
     apis: [
       createApiFactory({
         api: costInsightsApiRef,
         deps: { discoveryApi: discoveryApiRef, fetchApi: fetchApiRef },
         factory: ({ discoveryApi, fetchApi }) =>
           new CostInsightsClient({ discoveryApi, fetchApi }),
       }),
     ],
   });

   export const CostInsightsLitePage = costInsightsLitePlugin.provide(
     createRoutableExtension({
       name: 'CostInsightsLitePage',
       component: () =>
         import('./components/Router').then(m => m.Router),
       mountPoint: rootRouteRef,
     }),
   );
   ```

4. **Define the API client contract** via `createApiRef` so the page
   component never talks to `fetch()` directly — it depends on an
   interface the app wires an implementation into:
   ```typescript
   // plugins/cost-insights-lite/src/api.ts
   import { createApiRef, DiscoveryApi, FetchApi } from '@backstage/core-plugin-api';

   export interface CostInsightsApi {
     getMonthlyCost(componentName: string): Promise<{ amountUsd: number }>;
   }

   export const costInsightsApiRef = createApiRef<CostInsightsApi>({
     id: 'plugin.cost-insights-lite.service',
   });

   export class CostInsightsClient implements CostInsightsApi {
     constructor(
       private readonly deps: { discoveryApi: DiscoveryApi; fetchApi: FetchApi },
     ) {}

     async getMonthlyCost(componentName: string) {
       const baseUrl = await this.deps.discoveryApi.getBaseUrl('cost-insights-lite');
       const res = await this.deps.fetchApi.fetch(
         `${baseUrl}/components/${componentName}/monthly-cost`,
       );
       if (!res.ok) throw new Error(`Cost lookup failed: ${res.status}`);
       return res.json();
     }
   }
   ```
   The component consumes it with `useApi(costInsightsApiRef)` —
   never `new CostInsightsClient()` directly inside a component, since
   that bypasses the app's `ApiFactory` registration and makes the client
   impossible to mock in tests or swap in dev.

5. **Write the backend plugin on the new backend system**, declaring only
   the `coreServices` it actually needs:
   ```typescript
   // plugins/cost-insights-lite-backend/src/plugin.ts
   import { createBackendPlugin, coreServices } from '@backstage/backend-plugin-api';
   import { createRouter } from './router';

   export const costInsightsLitePlugin = createBackendPlugin({
     pluginId: 'cost-insights-lite',
     register(env) {
       env.registerInit({
         deps: {
           logger: coreServices.logger,
           httpRouter: coreServices.httpRouter,
           database: coreServices.database,
         },
         async init({ logger, httpRouter, database }) {
           const router = await createRouter({ logger, database });
           httpRouter.use(router);
           logger.info('cost-insights-lite backend plugin initialized');
         },
       });
     },
   });
   ```
   Register it in the app's backend entrypoint, `packages/backend/src/index.ts`:
   ```typescript
   backend.add(import('@internal/plugin-cost-insights-lite-backend'));
   ```
   This one line is the only change `packages/backend` needs — the plugin
   package owns its own routes, dependencies, and lifecycle.

6. **Surface the frontend page** in `packages/app/src/App.tsx`, either as
   a standalone top-level route:
   ```tsx
   import { CostInsightsLitePage } from '@internal/plugin-cost-insights-lite';

   <FlatRoutes>
     <Route path="/cost-insights-lite" element={<CostInsightsLitePage />} />
   </FlatRoutes>
   ```
   or, more commonly for a plugin scoped to a single service, as a tab on
   the `Component` entity page in `packages/app/src/components/catalog/EntityPage.tsx`:
   ```tsx
   const serviceEntityPage = (
     <EntityLayout>
       {/* existing tabs: Overview, CI/CD, API, ... */}
       <EntityLayout.Route path="/cost" title="Cost">
         <CostInsightsLitePage />
       </EntityLayout.Route>
     </EntityLayout>
   );
   ```

7. **Run the plugin in isolation during development** before testing it
   inside the full app, using the scaffolded dev entrypoint:
   ```bash
   yarn workspace @internal/plugin-cost-insights-lite start
   ```
   This boots a minimal standalone dev app (`plugins/cost-insights-lite/dev/index.tsx`,
   generated by `yarn new`) around just this plugin — much faster iteration
   than rebuilding the whole app on every change. Once the component and
   API client behave correctly in isolation, run `yarn start` at the repo
   root to verify it inside the full app (catalog context, real
   `discoveryApi` resolving the real backend, entity-page routing).

8. **Version and ship as part of the monorepo release**, not an
   independent npm publish: internal plugins are pinned to the app's
   Backstage core version by living in the same Yarn workspace, so a
   `yarn backstage-cli versions:bump` that upgrades core packages
   upgrades the plugin's dependency versions in the same commit — see the
   version-pinning guidance already covered in
   [backstage-developer-portal](../../../observability-and-platform-extras/skills/backstage-developer-portal/SKILL.md),
   which applies unchanged here.

## Best practices

- **Never call `fetch()` directly from a component** — always go through
  a `createApiRef`-defined client injected via `useApi()`, so the
  implementation can be swapped (mocked in tests, pointed at a different
  backend in dev) without touching component code.
- **Keep the backend plugin's registered `coreServices` minimal** —
  declaring `coreServices.database` when the plugin doesn't persist
  anything, or `coreServices.httpAuth` when it doesn't need caller
  identity, makes the plugin's actual capability surface unclear to
  reviewers and to Backstage's own dependency-injection validation.
- **Namespace backend routes under the plugin's own `pluginId`** (handled
  automatically by `httpRouter` under `/api/<pluginId>/...`) rather than
  inventing a separate path scheme — this is also what `discoveryApi.getBaseUrl(pluginId)`
  on the frontend resolves against, so the two must agree.
- **Use `yarn workspace <plugin> start` for the frontend dev loop**, not
  the full `yarn start`, until the component and API client work in
  isolation — cuts iteration time from a full-app rebuild to a single
  plugin's build.
- **Treat a plugin as a product for internal customers**, not an
  internal-only afterthought — write a short README in the plugin package
  describing what it surfaces and who owns it, matching the "platform as
  product" framing in
  [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md).
- **Prefer extending an existing community plugin (fork or contribute
  upstream) over building a near-duplicate from scratch** — check the
  Backstage plugin marketplace before scaffolding a new plugin for
  something like Kubernetes status, cost insight, or CI status, which
  already have maintained community implementations.
- **Don't put business logic that belongs to an existing internal service
  inside the Backstage backend plugin** — the backend plugin should be a
  thin proxy/aggregator calling that service's real API, not a place
  where provisioning or approval logic gets duplicated.

## Common pitfalls

- **Symptom:** A component throws `Error: No implementation available for
  apiRef 'plugin.cost-insights-lite.service'` at runtime.
  **Fix:** The `createApiRef` was defined but never registered into the
  plugin's `apis` array in `createPlugin(...)` (or the `ApiFactory` isn't
  exported/imported into the app), so nothing implements the interface the
  component asked for via `useApi()`. Add the `createApiFactory` entry to
  the plugin definition (step 3) and confirm the plugin package is
  actually imported somewhere the app's dependency graph reaches.

- **Symptom:** The backend plugin's routes 404 at
  `/api/cost-insights-lite/...` even though the plugin package builds
  cleanly.
  **Fix:** The plugin was scaffolded and coded but never added to
  `packages/backend/src/index.ts` via `backend.add(import(...))` — a
  backend plugin package existing in `plugins/` does nothing until the
  backend's entrypoint registers it.

- **Symptom:** A new catalog entity-page tab never appears on any
  `Component`, despite the plugin's page rendering fine when accessed
  directly by URL.
  **Fix:** The `EntityLayout.Route` was added to the wrong entity-page
  variant in `EntityPage.tsx` (Backstage typically defines separate page
  layouts per `spec.type`, e.g. `service` vs. `website` vs. `library`) —
  add the route to every entity-page variant that should show it, or to a
  shared layout all variants compose.

- **Symptom:** `yarn new` fails, or the generated plugin doesn't build,
  immediately after a Backstage core upgrade.
  **Fix:** The CLI's plugin template version is tied to the installed
  `@backstage/cli` version; a partially completed upgrade (some
  `@backstage/*` packages bumped, others not) leaves the generator
  producing code against APIs the rest of the app doesn't have yet. Run
  `yarn backstage-cli versions:bump` to align all `@backstage/*`
  dependencies to a single release line before scaffolding new plugins.

- **Symptom:** A plugin works correctly under `yarn workspace <plugin>
  start` in isolation, but breaks once mounted in the full app.
  **Fix:** The isolated dev harness provides its own mock
  `discoveryApi`/`fetchApi` and catalog context that can mask a real
  dependency the plugin needs from the full app (e.g. auth headers the
  full app's `fetchApi` attaches automatically but the dev harness
  doesn't). Always do a final verification with `yarn start` against the
  full app before considering the plugin done.

## Worked example

**Scenario:** The platform team at Acme wants a "Deploy Approvals" tab on
every `Component` catalog page, showing pending/approved/rejected
deployment-approval requests from an internal approvals service, and
letting a developer approve a request without leaving Backstage.

1. `yarn new` → Backend plugin → id `deploy-approvals`, creating
   `plugins/deploy-approvals-backend/` with a `createBackendPlugin`
   skeleton.
2. Implement the backend's router to proxy the internal approvals
   service, declaring `coreServices.logger`, `coreServices.httpRouter`,
   and `coreServices.httpAuth` (to forward the calling user's identity to
   the approvals service so "who approved this" is accurate):
   ```typescript
   env.registerInit({
     deps: {
       logger: coreServices.logger,
       httpRouter: coreServices.httpRouter,
       httpAuth: coreServices.httpAuth,
     },
     async init({ logger, httpRouter, httpAuth }) {
       httpRouter.use(await createRouter({ logger, httpAuth }));
     },
   });
   ```
3. Register it: `backend.add(import('@internal/plugin-deploy-approvals-backend'));`
   in `packages/backend/src/index.ts`.
4. `yarn new` → Plugin → id `deploy-approvals`, creating
   `plugins/deploy-approvals/` for the frontend.
5. Define `deployApprovalsApiRef` with `listForComponent(componentName)`
   and `approve(requestId)` methods, implemented by a `DeployApprovalsClient`
   calling the backend via `discoveryApi.getBaseUrl('deploy-approvals')`.
6. Build a `Router.tsx` listing pending requests with an "Approve" button
   calling `deployApprovalsApi.approve(requestId)`, and register the page
   via `createRoutableExtension` in `plugin.ts`.
7. Add `<EntityLayout.Route path="/deploy-approvals" title="Deploy
   Approvals"><DeployApprovalsPage /></EntityLayout.Route>` to the
   service entity-page layout in `EntityPage.tsx`.
8. Verify with `yarn workspace @internal/plugin-deploy-approvals start`
   against a mocked API response, then `yarn start` against the full app
   and a real approvals-service sandbox before merging.

The result: any `Component` in the catalog now has a "Deploy Approvals"
tab backed by a real internal service, built as two independently
versioned packages that upgrade alongside Backstage core rather than as
code bolted onto `packages/app`/`packages/backend` directly.

## Cross-references

- [backstage-developer-portal](../../../observability-and-platform-extras/skills/backstage-developer-portal/SKILL.md) — the baseline catalog/TechDocs/Software Template setup this plugin work is built on top of; read that first, it's not repeated here.
- [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md) — a common reason to write a custom plugin is to give a self-service provisioning workflow's API a first-class UI and Scaffolder action inside Backstage.
- [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md) — who on the platform team owns building/maintaining plugins, and why plugin development should be run like product work for internal customers rather than a side project.
