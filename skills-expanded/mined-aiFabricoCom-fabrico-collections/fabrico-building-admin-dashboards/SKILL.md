---
name: fabrico-building-admin-dashboards
description: "Builds and reviews admin dashboards with the mandatory Laravel, MySQL 8, Redis, Docker, Vue 3, Inertia, TypeScript, Tailwind, and shadcn-vue stack. Use for every greenfield admin panel, back-office, operations console, internal dashboard, CRUD console, or material admin UI extension; flags existing-stack conflicts before implementation."
---

# Building Admin Dashboards

Build admin dashboards on one consistent full-stack foundation. Treat the stack and the shadcn-vue registry as implementation constraints, not optional suggestions.

<required-foundation>

| Layer | Required choice |
|---|---|
| Backend | Current project-compatible Laravel release and supported PHP |
| Database | MySQL 8 with an explicit image/version constraint; never `latest` |
| Cache, queues, sessions | Redis |
| Runtime | Docker Compose for local development and test parity |
| Web UI | Vue 3, TypeScript, Inertia, Tailwind, and shadcn-vue |
| Package manager | Yarn for frontend and shadcn-vue CLI commands |

For a greenfield admin dashboard, do not substitute React, Blade-only UI, Livewire, Filament, Nova, Bootstrap, PostgreSQL, or a Node backend unless the user explicitly overrides this foundation. In an existing application with a conflicting stack, surface the conflict before implementation; do not silently introduce a parallel framework or begin a migration.

</required-foundation>

## Admin Dashboard Process

Track this checklist:

```text
Progress:
- [ ] Define the cost and quality profile
- [ ] Inspect the target application and freeze the stack
- [ ] Bootstrap Laravel, MySQL 8, Redis, and Docker
- [ ] Configure shadcn-vue and its Claude MCP server
- [ ] Define reusable forms, tables, filters, and CRUD resources
- [ ] Compose the admin UI from registry blocks and components
- [ ] Implement authorization, auditability, and data operations
- [ ] Apply AI-ready and SaaS-ready foundations
- [ ] Run the complete verification gate
```

### 1. Inspect and freeze the stack

- Apply `fabrico-building-lean-applications` and record the lowest safe architecture tier, infrastructure ceiling, recovery target, approved paid services, and measurable escalation triggers.
- Read `composer.json`, `package.json`, `yarn.lock`, `components.json`, Docker files, routes, authentication, authorization, and tenant conventions before editing.
- Distinguish a greenfield dashboard from an extension of an existing system.
- Record the required foundation in the implementation plan. Record any explicit user override and its consequences.
- Reuse existing compatible Laravel and Vue patterns. Do not create duplicate infrastructure or component systems.

### 2. Bootstrap the application foundation

- Start greenfield work from Laravel's official Vue starter kit so Vue, TypeScript, Inertia, Tailwind, authentication, and shadcn-vue share one supported baseline.
- Keep Laravel, Inertia pages, workers, and scheduler in one modular-monolith repository and build one application image. Use separate process roles from that image instead of separate services or codebases.
- Define Docker Compose services for the application, HTTP server, queue worker, scheduler, MySQL 8, and Redis. Add health checks, persistent development volumes, and an `.env.example` without secrets.
- Keep debugging, mail-capture, browser, and observability containers behind optional Compose profiles. Do not run idle development tooling in every environment.
- Configure Laravel to use MySQL for persistence and Redis for cache and queues. Use Redis for sessions when the deployment topology requires shared sessions.
- Make queue jobs idempotent and keep scheduler and worker processes separate from the web process.
- Pin compatible major/minor image constraints and verify the lockfiles; never rely on floating production dependencies.

### 3. Configure shadcn-vue discovery

Run this command from the target application's root when the Claude MCP configuration is absent:

```bash
yarn dlx shadcn-vue@latest mcp init --client claude
```

Preserve and merge any existing MCP configuration. If `components.json` is absent, initialize shadcn-vue with:

```bash
yarn dlx shadcn-vue@latest init
```

- Verify the MCP connection before relying on it. If the current client cannot reload MCP during the task, use the shadcn-vue CLI as the bounded fallback and report that limitation.
- Search the MCP registry and [shadcn-vue blocks](https://www.shadcn-vue.com/blocks) before writing UI code.
- Select the closest complete block first, then adapt it to the product. Prefer dashboard, sidebar, login, signup, and related blocks over recreating their structure.
- Install registry items through MCP or `yarn dlx shadcn-vue@latest add <item>`.
- Review third-party registry code before installation. Promote only stable, product-independent compositions into the private registry.

### 4. Compose the admin UI

- Apply `fabrico-building-admin-resources` to every CRUD form, data table, filter set, and resource page. Keep ordinary resource definitions in Git and use versioned database JSON only when authorized users must change form structure without a deployment.
- Source inputs, textareas, selects, checkboxes, radios, switches, date controls, buttons, dialogs, drawers, menus, tabs, cards, tables, pagination, breadcrumbs, sidebars, alerts, toasts, skeletons, and reusable layout blocks from shadcn-vue.
- Do not hand-roll an interactive primitive when a suitable registry item exists. Domain components may compose shadcn-vue primitives; generated `components/ui` code remains the low-level component boundary.
- When no suitable registry item exists, document the search, build the smallest accessible wrapper consistent with shadcn-vue APIs and tokens, and add automated interaction tests.
- Keep design tokens semantic. Preserve keyboard operation, focus visibility, labels, descriptions, error associations, loading states, empty states, and destructive-action confirmation.
- Implement server-side filtering, sorting, pagination, and authorization for data-heavy admin tables. Do not load unbounded datasets into the browser.

### 5. Implement secure administration

- Keep controllers thin; put validation in Form Requests, authorization in policies or gates, and business operations in application services.
- Enforce least-privilege roles and permissions on the server for every read and mutation. Hiding a UI action is not authorization.
- Protect state changes with CSRF controls, rate limits where relevant, transactions, idempotency for retried operations, and explicit confirmation for destructive actions.
- Record security-sensitive and business-critical mutations in an audit trail containing actor, tenant, action, subject, timestamp, and safe change metadata.
- Avoid N+1 queries, add indexes for admin filters and ordering, and return only fields required by the page.

### 6. Apply product-readiness foundations

- Apply `fabrico-preparing-applications-for-ai` to callable business operations, asynchronous work, data governance, observability, and future provider boundaries.
- Apply `fabrico-preparing-applications-for-saas` to tenant context, isolation, roles, entitlements, limits, audit trails, and lifecycle operations.
- Do not add unused providers, paid services, billing flows, or speculative AI features merely to satisfy readiness. Establish the required seams in code already needed by the product.
- Keep MySQL search, Redis queues, framework authorization, configuration flags, and the single-region deployment until measured requirements justify a more expensive tier.

### 7. Verify the result

```text
Validation:
- [ ] Docker Compose configuration resolves and required containers become healthy
- [ ] Application migrations and tests run against MySQL 8
- [ ] Laravel connects to Redis and a queued test job completes
- [ ] Authentication, authorization, tenant isolation, and audit events have automated tests
- [ ] Every page has loading, empty, error, and success states where applicable
- [ ] UI code outside the generated primitive layer does not recreate available shadcn-vue controls
- [ ] Yarn lint, type-check, test, and production build commands pass
- [ ] Laravel formatting, static analysis, and unit/integration tests pass
- [ ] The running dashboard is verified at desktop and narrow viewport widths
- [ ] Every paid service, extra datastore, or deployment layer has a measured trigger and exit path
```

## Connected Skills

- `fabrico-implementing-backend` - for Laravel API, service, queue, test, and Docker implementation patterns
- `fabrico-building-lean-applications` - for modular-monolith defaults, dependency budgets, risk-based testing, and scaling triggers
- `fabrico-building-admin-resources` - for reusable CRUD forms, tables, filters, resource contracts, and dynamic-form versioning
- `fabrico-implementing-frontend` - for Vue component composition and design-token discipline
- `fabrico-implementing-forms` - for validation and accessible field composition
- `fabrico-sql-and-database-understanding` - for MySQL schema, indexes, transactions, and query performance
- `fabrico-ensuring-accessibility` - for keyboard, focus, semantics, and WCAG checks
- `fabrico-preparing-applications-for-ai` - for the AI-ready baseline
- `fabrico-preparing-applications-for-saas` - for the SaaS-ready baseline
