---
name: roadguard-endpoint-delivery
description: Use when implementing, fixing, reviewing, or smoke-testing one assigned RoadGuard ASP.NET Core endpoint and its directly required N-layer persistence slice.
---

# RoadGuard endpoint delivery

## Load only the working slice

1. Locate the actual RoadGuard root; run `git status --short --branch`. If given an archive instead of a checkout, say so; do not invent branch/commit evidence.
2. Read root and applicable nested `AGENTS.md`, `.agents/rules/roadguard.md`, `planning/V2/TASK_LIFECYCLE.md`, and the assigned task. Restore its source checkpoint/current diff before rereading only invalidated sources. Read relevant ADR 001/004/006 sections for architecture/ownership, not their historical narrative.
3. Resolve V2 tasks under `planning/V2/Person_*/`; otherwise use the assigned legacy row. Read the decision register and only referenced FR/BR/UC/US/AC, PF/SQ/state, OpenAPI schemas and DD/ERD concepts. Record them in the task's `Source evidence` table before editing; do not read all 133 tasks or treat a historical OPEN label as current authority.
4. Use scoped `rg --files` and `rg -n` to find the nearest controller, service/interface, DTO, repository seam and focused test. Read those methods plus collaborators needed to understand effects. Expand only for an unresolved symbol, invariant, failure or shared impact. Exclude bin/obj/.git/TestResults, historical logs and secrets from broad searches.
5. Read [source map](references/source-map.md) for exact layer placement. For auth, offline, spatial, AI or unresolved V2 behavior, read only the relevant heading in [product gates](references/product-gates.md).

## Scope and contract

The owner named by an approved V2 task owns its complete required endpoint slice, including directly required entity, mapping, migration, and SQL-test changes. This is delivery ownership, not permission to cross N-layer boundaries. Reserve shared hotspots and serialize migrations as required by ADR 006.

Before edits, return this exact gate unless the same scope was already approved in this session:

```text
Task / owner / branch:
Goal:
In scope:
Out of scope:
Exact files and shared hotspots:
Dependencies present in this checkout:
Verification breadth and commands:
Packages, migration, data or external side effects:
Reply: Dong y <TASK-ID>
```

Honor explicit task authorization already given; do not request it again. A `PROPOSED_CONTRACT`, `NEEDS_REPO_CHECK`, or `BLOCKED_SLICE` task is not implementation approval and does not silently override current runtime behavior or accepted decisions. When authorized work starts, set `deliveryStatus` to `IN_PROGRESS`, record base/source checkpoint and mirror it in the manifest; preserve historical completion entries.

For a multi-API request, deliver bounded endpoint slices in dependency order within the authorized scope. Keep historical Done evidence intact. Before editing, record 5–8 lines: method/route, actor/scope, input validation, success body/status, errors, state transition, concurrency/retry, audit/privacy.

Compare running/source contract with draft docs. Explicitly resolve PUT/PATCH, ProblemDetails/envelope, operationId/Idempotency-Key, body rowversion/If-Match, and pagination differences. Preserve existing behavior unless the task authorizes a contract migration. Never use a generated task as proof that proposed business rules are approved.

## Implement within the current layers

- Keep `Controller -> IService -> IRepository`. Do not introduce Minimal APIs, MediatR, AutoMapper, direct controller-to-repository access or a second architecture.
- Keep controllers limited to HTTP binding, actor extraction, service calls and result/status mapping. Keep orchestration, authorization, workflow policy and DTO mapping in Services. Do not put EF, DbContext, HttpContext, IActionResult or HTTP status decisions in Services.
- Keep EF/SQL/storage, atomic writes, rowversion, durable idempotency and outbox in Repositories. Return facts through interfaces; do not expose IQueryable or decide authorization/workflow/HTTP codes there. Load `roadguard-persistence` whenever the task changes an EF query, mapping, atomic write, migration, concurrency, idempotency, outbox, storage or SQL behavior.
- Keep BusinessObjects entity-only plus existing enums/extensions; entity-local invariants use supplied values, not ambient I/O/clock/random. Keep DTOs data-only with validation attributes; no computed business behavior or lower-layer access.
- Put each new public type in its own file at an existing responsibility-based location. Preserve namespaces copied from actual neighbors, not inferred folder names. Do not mechanically split untouched legacy files or create catch-all Helpers/Utils/Shared/Models/Managers folders. Respect the existing 500-line limit; scope a split before expanding an oversized file.
- Reuse existing DI, result/status, validation, clock, random and cancellation patterns. Propagate CancellationToken; await I/O without Result/Wait; use UTC DateTimeOffset where consistent with the contract. Do not add packages or upgrade SDK/framework as a shortcut.
- Add/update the single endpoint request in `RoadGuardSystem.API/RoadGuardSystem.API.http`; use environment variables and deterministic fixture IDs, never committed secrets. Check success plus meaningful forbidden/invalid/conflict cases.
- Load `roadguard-postman` for every API contract change and update `docs/postman/RoadGuardSystem-V2.postman_collection.json` plus the local environment/README when needed in the same task. Preserve request IDs and unrelated scripts; do not create planning-only requests.
- Before a real local API/Postman smoke, use the Development-only `DbInitializer`: provide `RoadGuardDatabase:ConnectionString`, set `RoadGuardDatabase:InitializeOnStartup=true` and `RoadGuardDatabase:SeedDevelopmentUsers=true`, then start the API. It applies migrations and idempotently seeds the four documented Postman accounts. Never enable these flags in Production and never commit connection strings or passwords.

## Verify and stop at sufficient evidence

Use `roadguard-test-selection` before running commands. Build fresh selected test binaries before `--no-build`. Run the Postman static validation required by `roadguard-postman`; verify the endpoint on a real host/test fixture when the task allows it and inspect status, body, relevant headers and durable effects. A mocked service is not SQL/concurrency evidence. Keep output short; retain full failure logs locally and read the first relevant failure. Reuse valid unchanged evidence and rerun only invalidated checks.

Report outcome, changed paths, actual commands/pass counts, reused/invalidated evidence and remaining blockers. Immediately append `Completion history` and set `DONE`, `PARTIAL` or `BLOCKED` under `TASK_LIFECYCLE.md`; mirror manifest status. Never claim tests ran from a template or zero-test run, and never mark API `DONE` from docs/static checks alone. Preserve unrelated work; do not commit/publish or perform destructive operations beyond session authorization.
