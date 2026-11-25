---
name: laravel-project-patterns
description: 'Use when writing, changing, testing, or reviewing Laravel application code, schema, factories, project tooling, resources, or Pest tests. Route repository-derived conventions from each touched path to focused references; live files and nearest equivalent siblings decide applicability.'
---

# Laravel Project Patterns

Route each touched behavior surface to its domain router and only the focused
leaves matching the live contract. The executable router, not manual browsing
of [`references/MAP.md`](references/MAP.md), decides which branch to expose.
Examples are synthetic; preserve them and their placeholder entities.

## Required Workflow

1. Read the nearest `AGENTS.md` and project guidance.
2. Identify every touched path. Before any tool call that discovers, searches,
   lists, or opens pattern references, and before editing, run the
   [`executable context router`](references/context-resolver.md) with plain
   `php` and all touched paths. This preflight is mandatory.
3. Read only exact references selected by the result. Expand one or more named
   frontiers, then select only children printed by those frontiers. Never use
   `rg`, `find`, globs, directory listings, guessed paths, or broad `sed` reads
   to discover or choose references. If the touched-path set grows, rerun the
   complete preflight before further reference reads or edits; stale results do
   not authorize the new surface.
4. Identify every behavior owner. Read the exact live project code files
   and the nearest equivalent siblings before editing. Equivalent means the
   same precondition, operation, outcome, route depth, binding ownership,
   transport, and response contract, not merely a nearby directory.
   Repository search is allowed here for live code evidence because the router
   preflight has already succeeded; it is never a substitute for that preflight.
5. For each touched surface, use the router-selected focused leaves and core
   contracts. References expose possible patterns; absent behavior is not mandatory.
6. Do not edit until this routing tuple is known: touched surface, behavior
   owner, live sibling evidence, and selected reference. Continue discovery if
   any element is missing. If no equivalent sibling exists, preserve the live
   shape and keep the rule local instead of generalizing. Check versioned
   framework documentation when needed.
7. Implement, run focused verification, review the complete diff, and confirm
   every affected owner surface remains covered.

Controller tests start at their
[`router`](references/tests/Feature/Http/Controllers/README.md), then select
only the action, route depth, transport, pattern, and validation in scope.

## Non-Negotiable Router Contract

- Live evidence and nearest equivalent siblings override generic habits and examples.
  Preserve concurrent work and avoid unrelated refactors.
- Match finality, schema, migrations, generated files, and unguarded models to
  the sibling family: [`code and schema`](references/core/code-and-schema.md).
- Choose tests by behavior owner. Layered HTTP, action, model, and database
  tests are distinct when they prove different contracts. Follow persistence,
  Pest, fixture, `and()`, and `refresh()` rules in
  [`test design`](references/core/test-design-and-style.md).
- Controllers remain tested entry points when actions own persistence. Mock
  delegated actions and preserve each distinct HTTP-owned path, minimal
  Request-to-Input mapping, `$response`, and public response contract:
  [`HTTP boundaries`](references/core/http-and-request-boundaries.md).
- Form Requests own HTTP shape, normalization, scoped validation, and
  request-safe cross-field rules. Actions own transactional and dependent-state
  guards. Preserve or convert public IDs according to the live boundary.
- Actions accept business inputs only. Do not repeat binding/ownership queries.
  Default to no row lock or improvised concurrency substitute:
  [`actions and concurrency`](references/core/actions-and-concurrency.md).

## Main Routers

These links keep the full tree auditable. Do not open one to choose a task
branch unless the executable router returned it.

- [`context resolver`](references/context-resolver.md): mandatory deterministic
  path, operation, concern, gate, and progressive-leaf selection.
- [`project`](references/project/README.md): routes, configuration, tooling,
  localization, bootstrap, public files, and seeders.
- [`database`](references/database/README.md): migrations and factories.
- [`app`](references/app/README.md): PHP under `app/**`.
- [`resources`](references/resources/README.md): JavaScript, Blade, React
  Email, TypeScript, and CSS.
- [`tests`](references/tests/README.md): suite ownership, paths, and support.
- [`core`](references/core/README.md): cross-cutting contracts and completion.

See the [reference structure](references/README.md). Finish with focused tests,
PHP formatting, complete diff review, and the
[completion checklist](references/core/completion-checklist.md). Passing tests
prove execution, not that an HTTP, domain, persistence, or regression contract
was not deleted.
