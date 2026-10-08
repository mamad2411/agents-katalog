---
name: go-cms-api
description: Use for GO CMS HTTP API design or implementation: public/admin CRUD endpoints, route contracts, request/response DTOs, validation, transport errors, pagination, filtering, sorting, site context, API versioning/compatibility, optional-feature API contributions, and wiring authorization into handlers/application services. Do not use for domain-only changes with no HTTP contract impact.
---

# GO CMS API

Follow root `AGENTS.md` and `backend/AGENTS.md`. Load `go-cms-development` when the API task changes reusable backend architecture. Load `go-cms-authorization` when permission semantics or enforcement boundaries are materially involved. Load `go-cms-runtime-integrity` when management/public HTTP contributions depend on SiteRuntime/module runtime selection.

## Discovery

Before designing or changing an endpoint, inspect:

1. nearest existing route/handler in the same API family;
2. domain/application service it calls;
3. request/response/error conventions already used by the project;
4. focused handler/service tests;
5. permission/site-resolution middleware/contracts when relevant;
6. optional-module wiring if the endpoint belongs to a feature package.

Prefer extending established API vocabulary over inventing a parallel convention.

## Boundary

Keep the flow conceptually:

```text
HTTP route/handler
  -> parse + transport validation
  -> resolve request/site/actor context
  -> application/domain service
  -> repository/domain behavior
  -> map result/error to HTTP response
```

Handlers are transport adapters, not homes for business behavior.

Do not put persistence queries, cache policy, lifecycle rules, authorization policy or cross-module orchestration directly in handlers when they belong to reusable service/domain boundaries.

HTTP DTOs may differ from domain entities. Do not expose persistence structs merely to avoid mapping code.

## Optional feature management APIs

Optional feature modules such as Mail, Forms, Search or Audit must not become compile-time dependencies of generic `kernel/app` merely because they expose management HTTP endpoints.

Forbidden growth pattern:

```text
kernel/app imports modules/mail
App.mailManagement
App.MailManagement()

then later:
App.formsManagement
App.searchManagement
...
```

`kernel/app` may know generic module/runtime/transport contribution contracts, mandatory core/admin packages already established by the architecture, and application-scoped generic registries. It must not gain one field/method/import per optional feature.

Prefer the smallest coherent generic mechanism that lets installed feature modules contribute their management HTTP surface. Depending on current architecture this may be:

- a generic HTTP/management contribution/provider contract implemented by feature modules/module runtimes;
- a generic registry/dispatcher keyed by module code/path and resolved against the current SiteRuntime;
- project/internal composition that owns selected optional feature wiring while generic kernel remains unaware.

Choose the existing architectural style with the least new machinery. Do not build a service locator, reflection DI container or generic expression language merely to mount routes.

Target invariants:

- adding Forms after Mail should not require adding `formsManagement` to `kernel/app`;
- generic server/kernel code should not import each optional feature package just to mount its routes;
- optional module removal from a profile/project should remove/unexpose its API cleanly;
- site-scoped feature routes resolve the current site's module runtime rather than a mutable global service;
- backend authorization remains authoritative;
- transport-specific `net/http` details stay in the HTTP/composition boundary rather than domain contracts where avoidable.

If project/internal composition is intentionally the owner of concrete installed feature imports, that is preferable to leaking them into generic kernel. Still avoid duplicating feature-specific lifecycle state in `App`.

Add architecture/import tests or compile-time guards where practical so optional feature imports cannot silently creep back into generic kernel packages.

## CRUD consistency

Prefer a consistent resource-oriented surface for ordinary management APIs, for example:

```text
GET    /api/sites
POST   /api/sites
GET    /api/sites/{id}
PATCH  /api/sites/{id}
DELETE /api/sites/{id}
```

Use domain actions when the operation is not naturally CRUD rather than forcing every behavior into a generic update payload.

Do not create separate domain/service implementations for admin and public APIs when both can reuse the same underlying behavior with different transport policy/projections/authorization.

## Requests and validation

Separate:

- syntactic/transport validation: malformed IDs, invalid JSON, enum representation;
- domain validation: illegal state, invalid owner/type, duplicate semantic value;
- authorization: actor is not allowed to perform the operation.

Reject unknown/unsupported fields when silent acceptance would hide client mistakes.

For partial updates, define presence semantics explicitly. Do not conflate missing, `null`, zero and empty unless intentional.

Do not let transport defaults silently override domain semantics when omission has meaning.

When a request carries an expected version/precondition, validate it server-side and use the established conflict response for stale state.

## Responses and errors

Use one established response/error convention across API families.

Map errors by meaning, not string matching. Prefer typed/sentinel/domain errors.

Distinguish at least where applicable:

```text
400 malformed transport input
401 unauthenticated
403 authenticated but forbidden
404 target not visible/found according to policy
409 state/version/uniqueness conflict
422 structurally valid request rejected by domain validation
500 unexpected server failure
```

Do not leak SQL errors, connector details, package paths, stack traces or sensitive authorization reasons.

## List APIs

List endpoints are bounded and return projections appropriate to the list.

Use a common query vocabulary for pagination/filtering/sorting/search where supported.

Prefer deterministic ordering with stable tie-breaker.

Do not fetch full large bodies/documents merely because a detail entity already exists. Define summary DTO/domain projections when the list UI only needs metadata.

For high-cardinality collections such as LibraryItems, follow the domain skill and prefer cursor/keyset pagination on hot/deep paths rather than large OFFSET scans.

Do not fetch all rows and paginate/filter in Go/frontend when repository queries can do it efficiently.

## Site context

Site-scoped APIs obtain site identity through established resolver/request/runtime context. Do not rely on mutable global current-site state.

Validate target ownership/site association where relevant. Avoid insecure direct-object access from global lookup without site boundary.

A site selector in admin UI is presentation state; backend site authorization remains authoritative.

## Authorization wiring

Transport may authenticate actor and pass context inward, but authorization must not exist only as button visibility or handler-local checks.

Prefer reusable authorizer/application/domain boundaries. Every protected read/change enforces relevant permissions server-side.

When an operation accepts references to another protected domain object (for example Mail manually receiving a File ID), authorize that referenced object using the correct actor before converting it into trusted persisted state. A later background worker may use trusted/system access only after the initiating operation has established authorization or the input came from a trusted automatic backend source.

Use `go-cms-authorization` for permission-model changes.

## Compatibility and evolution

Current `main` is the source of truth. Do not add legacy aliases, duplicate endpoints, fallback payloads or version bridges unless explicitly requested.

When changing an established public contract, identify direct consumers/tests before editing. If destructive compatibility expectations are unclear, use `go-cms-requirements`.

## API-driven frontend rule

Backend APIs expose semantic capabilities/data, not Vue implementation details.

Do not send component paths, executable JS, framework CSS classes or frontend package internals through generic backend contracts.

For dynamic forms/navigation/widgets expose semantic IDs, capabilities, field metadata and validated values; frontend resolves installed implementation.

Backend preview/render endpoints are authoritative when output depends on security-sensitive rendering/templating. Frontend must not become the source of truth for final recipients/content.

## Tests

Choose focused tests for the changed contract:

- request decoding/validation;
- success response shape/status;
- domain error -> HTTP mapping;
- unauthenticated/forbidden behavior;
- site isolation/ownership;
- pagination/filter/sort determinism;
- lightweight list vs full detail projection;
- partial update presence semantics;
- optimistic version/precondition conflicts;
- referenced-object authorization;
- domain service called rather than duplicated handler behavior;
- optional feature can be wired/removed without feature-specific fields/imports in generic `kernel/app`.

Run focused package tests while iterating. Use broad backend validation once near completion for cross-package refactors.

## Anti-patterns

Do not:

```text
handler -> SQL/connector directly
handler-local business lifecycle rules
permission enforced only by frontend visibility
unbounded list endpoints
full body/blob fetch for metadata-only lists
fetch-all then paginate in memory
raw persistence structs as accidental API contracts
string-match errors to choose status codes
site-scoped lookup without ownership validation
untrusted related-object IDs resolved with System actor
optional module imported/stored directly in generic kernel/app per feature
new /admin-specific domain service when generic domain behavior already exists
silent backward-compatibility/fallback endpoints not requested
```
