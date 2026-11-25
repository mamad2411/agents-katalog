---
name: fabrico-building-admin-resources
description: "Builds repeatable Laravel admin CRUD resources from versioned field and table definitions using shadcn-vue, VeeValidate/Zod, TanStack Table, and server-side Laravel validation and querying. Use when creating CRUD forms, dynamic forms, data tables, filters, resource pages, schema-driven admin modules, or reusable admin blocks; keeps database-stored JSON schemas limited to genuinely runtime-configurable forms."
---

# Building Admin Resources

Build forms, tables, filters, and CRUD pages as reusable admin resources on top of `fabrico-building-admin-dashboards`. Optimize for many applications: keep the default path typed, code-owned, inexpensive, and easy to generate; introduce a runtime form engine only when the product actually requires one.

## Make the Architecture Decision

Choose exactly one mode before implementation:

| Requirement | Mode | Definition location | Renderer |
|---|---|---|---|
| Developers own the CRUD screen and deploy changes | `standard` | Version-controlled repository file | Typed Vue components composed from shadcn-vue |
| Authorized users must change fields without a deployment | `dynamic` | Immutable, versioned JSON records in MySQL 8 | Whitelist-based schema renderer composed from shadcn-vue |

Use `standard` unless runtime configurability is an explicit acceptance criterion. Do not put ordinary CRUD definitions in the database merely to make them "generic".

Keep core entity data in relational columns. Use JSON for dynamic submissions, UI preferences, and genuinely variable long-tail attributes. Project frequently filtered, sorted, joined, or reported values into typed and indexed columns.

Do not make Vueform the default component system. Consider it only when an embedded visual form builder or its advanced runtime form features are explicit requirements. Before adoption, verify current license and total cost, Vue/Tailwind compatibility, accessibility, bundle impact, export and migration paths, and whether the team accepts a second UI abstraction beside shadcn-vue. Record approval in the architecture decision.

## Use the Default Resource Stack

- Render controls, field structure, buttons, dialogs, menus, and table visuals with shadcn-vue.
- Use VeeValidate and Zod for typed client-side validation of standard forms.
- Treat Laravel Form Requests as the authoritative validation boundary.
- Enforce authorization with Laravel policies or gates for every read and mutation.
- Use shadcn-vue table markup with TanStack Vue Table for column, selection, sorting, and visibility state.
- Execute search, filtering, sorting, pagination, and exports on the Laravel server for unbounded or growing datasets. Permit client-side state only for explicitly bounded small datasets within a documented row and payload budget.
- Use MySQL 8 for persistence and Redis for cache, queues, locks, and rate-limit coordination where applicable.

Apply `fabrico-implementing-forms` for field composition, validation timing, accessible errors, and multi-step behavior. This skill defines the resource boundary and reuse strategy; it does not replace those form fundamentals.

## Follow the Resource Workflow

Track this checklist:

```text
Progress:
- [ ] Inspect existing admin conventions and reusable registry blocks
- [ ] Classify the resource as standard or dynamic
- [ ] Define and validate the resource contract
- [ ] Implement the form and authoritative server validation
- [ ] Implement the table and server-side query contract
- [ ] Enforce permissions, tenancy, and auditability
- [ ] Add versioned persistence when the resource is dynamic
- [ ] Verify behavior, accessibility, security, and performance
```

### 1. Reuse before building

- Inspect routes, policies, Form Requests, query objects, Inertia pages, `components.json`, generated shadcn-vue primitives, and existing resource components.
- Search the configured shadcn-vue MCP registry and private registry before writing UI code.
- Prefer shared `resource-form`, `resource-filters`, and `resource-page` blocks when available. Share a small table shell and controls, but keep domain columns and query behavior local because data tables vary by resource.
- Promote stable cross-application compositions into a reviewed private shadcn-vue registry. Do not turn the first resource into an internal framework.
- Keep domain behavior outside generated `components/ui` primitives.

### 2. Define the contract

Read `references/admin-resource-schema.md` before creating or changing a resource definition. Start from `references/admin-resource.example.json` and store a standard definition under the repository's established convention, such as `resources/admin/<resource>.resource.json`.

Run:

```bash
python3 .claude/skills/fabrico-building-admin-resources/scripts/validate_admin_resource.py path/to/resource.json
```

Run the same validator in CI when resource definitions are committed. Treat the definition as declarative product and UI metadata, not executable configuration.

For `standard` mode, use the validated definition to generate or guide ordinary typed code that the application owns. Do not ship a generic runtime interpreter merely to avoid generating a form or table.

Never place JavaScript, callbacks, SQL fragments, PHP class names, raw HTML, arbitrary component paths, or authorization decisions in a definition. Whitelist field types, condition operators, option sources, sortable keys, filter keys, row actions, and permission names on the server.

### 3. Implement the form

- Map every field to an approved shadcn-vue component through an explicit registry in code.
- Generate or write typed form values and Zod validation for `standard` resources. Mirror business validation in a Laravel Form Request; do not infer authoritative server rules from client input.
- For `dynamic` resources, compile the published definition into client constraints and separately into an allowlisted Laravel validation rule set.
- Load option sources through named, authorized adapters. Do not accept URLs, model classes, or queries from JSON.
- Preserve labels, descriptions, error associations, focus movement, disabled and loading behavior, draft recovery, and destructive-action confirmation.
- Prevent mass assignment by mapping validated fields explicitly into a command or service.

### 4. Implement the table

- Choose client-side processing only when the complete dataset is bounded, non-sensitive, cheap to fetch, and remains inside an explicit payload and browser-memory budget. Otherwise use Laravel pagination and manual TanStack server state from the first release.
- Keep TanStack Table state controlled and synchronize shareable filters, search, page, and sort state with the URL when useful.
- Debounce text search and cancel stale requests.
- Pass only allowlisted filters and sort keys to a Laravel query object. Never concatenate request values into SQL identifiers.
- Paginate on the server and return only the required fields. Do not load an unbounded collection into the browser.
- Use stable row identifiers and preserve keyboard operation for selection, menus, and bulk actions.
- Store per-user column visibility, order, and width as JSON only after intersecting preferences with the current column allowlist.
- Require explicit permission checks and audit events for row and bulk mutations.

### 5. Persist dynamic definitions safely

Use separate records for stable identity, immutable published versions, and submissions:

- `form_definitions`: stable form identity, tenant ownership, and lifecycle metadata.
- `form_definition_versions`: definition ID, monotonically increasing version, `draft|published|archived` status, schema JSON, checksum, creator, and publication timestamp.
- `form_submissions`: exact definition-version ID, tenant ID, payload JSON, status, submitter, and submission timestamp.

Never mutate a published version. Create a draft successor, validate it, preview it, publish it transactionally, and retain the version used by every submission. Apply tenant scopes to definitions, versions, option sources, and submissions.

Validate definitions and submissions in application code. Use MySQL JSON checks only as defense in depth because database JSON Schema support may not match the application validator. Add indexes or relational projections for operational queries; do not depend on scanning arbitrary JSON payloads.

## Verification Gate

```text
Validation:
- [ ] Resource definition passes validate_admin_resource.py
- [ ] Standard definitions live in Git; runtime definitions use immutable versions
- [ ] All controls and table visuals compose shadcn-vue primitives
- [ ] Client validation improves UX; Laravel validation remains authoritative
- [ ] Policies enforce every route and mutation independently of visible UI
- [ ] Table sort, filter, search, pagination, and export inputs are allowlisted
- [ ] Tenant boundaries and audit events have automated tests
- [ ] Dynamic publication, version pinning, and submission replay have tests
- [ ] Loading, empty, error, success, stale-request, and destructive states work
- [ ] Keyboard, focus, labels, errors, and responsive behavior are verified
- [ ] Query count, indexes, payload size, and large-dataset pagination are verified
```

## Connected Skills

- `fabrico-building-admin-dashboards` - for the mandatory Laravel, MySQL 8, Redis, Docker, Vue/Inertia, and shadcn-vue foundation
- `fabrico-building-lean-applications` - for reusable golden paths, complexity budgets, and evidence-based escalation
- `fabrico-implementing-forms` - for form validation, field composition, accessibility, and multi-step flows
- `fabrico-implementing-frontend` - for Vue composition, state boundaries, and design tokens
- `fabrico-implementing-backend` - for Laravel services, Form Requests, policies, queues, and tests
- `fabrico-sql-and-database-understanding` - for relational modeling, JSON tradeoffs, indexes, and transactions
- `fabrico-ensuring-accessibility` - for WCAG, keyboard, focus, and error semantics
- `fabrico-preparing-applications-for-saas` - for tenant isolation, roles, entitlements, and audit trails
