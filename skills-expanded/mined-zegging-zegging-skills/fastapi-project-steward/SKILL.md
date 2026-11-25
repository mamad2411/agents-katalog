---
name: fastapi-project-steward
description: Guide the creation, iteration, and long-term maintenance of FastAPI projects with production-oriented structure, dependency design, async boundaries, schema discipline, testing, and operations hygiene. Use this skill whenever the user is building or cleaning up a FastAPI backend, organizing modules, designing services or dependencies, adding schemas/models, fixing async or blocking behavior, introducing auth or validation boundaries, setting up tests or migrations, or asking for FastAPI best practices even if they do not explicitly ask for "architecture" or "maintenance".
---

# FastAPI Project Steward

Use this skill to help users build or improve FastAPI projects in a way that stays understandable as the codebase grows.

The goal is not to produce the smallest demo app. The goal is to produce a codebase that is predictable, testable, and maintainable after many iterations. Keep changes proportional to the user's scope: improve the shape of the codebase without forcing a full rewrite for a small task.

## Operating principles

Prioritize these qualities:

1. Clear module boundaries instead of file-type sprawl.
2. Thin route handlers and explicit service/dependency layers.
3. Correct async behavior and safe handling of blocking work.
4. Strong schema discipline with Pydantic and typed interfaces.
5. Reusable validation and auth logic through dependencies or equivalent explicit abstractions.
6. Maintainable persistence, migrations, naming, and test setup.
7. Documentation and conventions that make the next change easier.

When there is a tradeoff, prefer the smallest structure that keeps future changes safe and legible.

## When you should actively use this skill

Use this skill when the user is doing any of the following in a FastAPI codebase:

- Creating a new FastAPI project or backend module.
- Designing project structure, module layout, or layering.
- Adding routes, services, dependencies, schemas, models, or config.
- Refactoring a messy FastAPI app into a more scalable shape.
- Fixing async misuse, blocking I/O in async code, or threadpool misuse.
- Introducing auth, permissions, request validation, or shared dependencies.
- Adding migrations, database conventions, or API documentation.
- Setting up or improving FastAPI unit/integration tests.
- Asking for best practices, production conventions, or maintainability advice.

## First pass

Start by identifying which lifecycle stage the user is in:

1. New project design.
2. Feature implementation in an existing service.
3. Refactor / cleanup.
4. Reliability or performance improvement.
5. Long-term maintenance standardization.

Then adapt depth accordingly.

Before proposing structure changes:

1. Inspect the current layout and naming conventions.
2. Identify the business domain or module being changed.
3. Decide whether the current request needs a surgical fix, a local refactor, or a broader reorganization.
4. Keep the recommendation compatible with the existing project unless the current shape is actively causing problems.

For a small change, do not force a giant architecture rewrite. For a growing codebase, favor patterns that reduce future churn.

## Working method

Follow this sequence unless the user already narrowed the task:

1. Identify the module or business domain being changed.
2. Decide whether the work belongs in route, dependency, service, repository, config, schema, or infrastructure layer.
3. Keep the route focused on transport concerns: request parsing, dependency wiring, response shape, status code, and documentation.
4. Move reusable validation, auth context parsing, ownership checks, and similar preconditions into dependencies or another explicit reusable boundary.
5. Keep business decisions in service classes or service functions.
6. Keep database-heavy shaping in SQL when that is simpler and cheaper than rebuilding everything in Python.
7. Add or update tests around the changed behavior.
8. Preserve or improve naming, docs, and migration hygiene.

If the user only needs advice, still anchor the answer in a concrete next step such as a proposed file layout, a refactor sequence, or an execution-boundary fix.

## Recommended project shape

Prefer module-oriented structure over splitting the whole app into global `routers/`, `models/`, `schemas/`, and `crud/` buckets.

Good default:

```text
app/
  auth/
    router.py
    schemas.py
    models.py
    dependencies.py
    service.py
    exceptions.py
    constants.py
  users/
    router.py
    schemas.py
    models.py
    dependencies.py
    service.py
    exceptions.py
  core/
    config.py
    logging.py
    middleware.py
  db/
    base.py
    engine.py
    session.py
    mixins.py
  services/
    mailer.py
    storage.py
  main.py
```

Notes:

- Put domain code together so a developer can understand one area without jumping across the repo.
- Reserve top-level shared modules for truly cross-cutting concerns.
- If the project is small, collapse lightly, but preserve the same separation of responsibilities.
- If the existing codebase already uses a different but consistent layout, improve it incrementally rather than relocating everything at once.

## Route design

Routes should stay thin.

Route handlers should usually do only these things:

- declare request and response schemas
- pull dependencies
- call a service or orchestrator
- return the result with the correct status code
- describe the endpoint clearly for docs

Avoid putting complex business logic directly in handlers.

## Dependency design

Use dependencies for reusable request-scoped concerns, especially when they validate or enrich request context.

Strong use cases:

- current user parsing
- auth token parsing
- tenant or organization context
- validating resource existence
- ownership / permission checks
- request-scoped shared objects

Design guidance:

- Prefer small dependencies that compose well.
- Chain dependencies when one validation builds on another.
- Reuse dependency outputs instead of duplicating lookup code in multiple routes.
- Remember that FastAPI caches dependency results per request, so splitting a large dependency into smaller reusable parts is often a win.
- Prefer `async` dependencies unless there is a clear reason not to.

## Service design

Prefer explicit service boundaries over route-level business sprawl.

Use service classes when they improve organization, especially if:

- a domain has several related operations
- shared context or collaborators are needed
- the service file is becoming a grab bag of unrelated functions

Keep services focused on business behavior, not HTTP transport details.

If persistence logic becomes substantial, it is reasonable to split repository/data-access concerns from higher-level service logic.

Do not create a service class only for ceremony. A small module-level service function is fine when the domain is still simple.

## Async and blocking work

Treat async boundaries as a correctness concern, not just a style preference.

- Use `async def` for handlers and dependencies that await non-blocking I/O.
- Do not run blocking operations directly inside async handlers.
- If forced to use a sync SDK for I/O, move that call into a threadpool.
- Do not pretend CPU-heavy work becomes cheap by awaiting it or moving it to threads. For real CPU-heavy workloads, use a worker or separate process.

If you spot `time.sleep`, blocking file/network SDK calls, or long sync computations inside async routes, call it out and fix the execution boundary.

## Schemas and typing

Use Pydantic models and Python types aggressively to make data contracts explicit.

Recommended patterns:

- define request and response schemas clearly
- validate constraints close to the boundary
- use enums and constrained fields where appropriate
- introduce a custom base schema if the project needs shared config or serializers
- split settings by domain when configuration is growing

Be careful with validation behavior:

- user-facing schema validation errors can expose detailed `ValueError` messages
- response-model validation has a runtime cost; avoid unnecessary double model construction in hot paths

## Persistence and SQL

Prefer clear SQL/data-access logic over excessive Python-side data reshaping.

- Push joins and simple aggregation into SQL when it makes the code simpler and faster.
- Use explicit naming conventions for database keys and indexes.
- Keep migrations deterministic, descriptive, and reversible.
- Give migration files human-readable names.

Avoid hidden or deeply nested session lifecycle management inside service methods. Prefer explicit session ownership patterns that are consistent across the codebase.

## REST and naming conventions

Favor consistent RESTful design so validation and dependencies can be reused cleanly.

- use stable path parameter names for the same concept
- keep naming explicit and predictable
- prefer lower snake case in database names
- use suffixes like `_at` for datetimes and `_date` for dates

Consistency matters because it reduces duplicated validation and makes the codebase easier to scan.

## Documentation behavior

When adding or changing endpoints:

- include `response_model`, `status_code`, summary, and description when useful
- document alternate responses when the endpoint can return materially different schemas
- consider hiding OpenAPI/docs outside allowed environments for internal services

If a custom response strategy is used, watch for drift between actual responses and declared API docs.

## Testing expectations

When changing core behavior, add tests.

Prefer:

- async-friendly integration tests for API behavior
- request/response tests at the route boundary
- focused unit tests for service logic with clear inputs and outputs

For async stacks, set up the test client and fixtures in an async-friendly way early rather than patching it later after event loop issues appear.

When the user is refactoring without changing behavior, prioritize tests around the boundaries most likely to regress before moving code around.

## Configuration and operations hygiene

Keep configuration explicit and maintainable.

- split settings by domain when the app grows
- centralize environment loading strategy
- keep secrets handling deliberate
- standardize lint/format/test commands

When the project needs background jobs, worker processes, or event/message hubs, introduce them as explicit architecture choices rather than as ad hoc helper calls hidden in routes.

## Anti-patterns to correct

When you see these, prefer to fix them rather than copying them forward:

- fat route handlers with mixed transport and business logic
- generic top-level `crud.py` sprawl across the whole app
- blocking I/O inside async handlers
- excessive local session creation in nested service methods
- duplicated validation logic across routes
- missing types on request/response/service boundaries
- migrations with vague names or non-reversible logic
- tests added too late to support safe refactoring

## Output expectations

Match the output to the task.

If the user asks for implementation:

- produce code that fits the existing module layout
- explain why files were placed where they were
- mention any follow-up tests or migration steps

If the user asks for architecture advice:

- give a recommended structure
- explain tradeoffs and when to keep it simpler
- identify the smallest safe next step, not only the ideal end state

If the user asks for review/refactor guidance:

- identify concrete anti-patterns
- propose a staged refactor path
- preserve behavior while improving boundaries

Keep answers concrete. Prefer showing the smallest safe structure or patch over a generic catalog of best practices.

## Examples

**Example 1:**
Input: "帮我给 FastAPI 项目加一个订单模块，顺便把代码结构整理一下。"
Output: Propose a module-oriented `orders/` package, keep routes thin, introduce request/response schemas, move business rules into service layer, add dependencies for auth/resource validation, and mention tests/migrations.

**Example 2:**
Input: "Why is my FastAPI app becoming unresponsive when one endpoint calls a legacy SDK?"
Output: Inspect whether blocking sync I/O is being called inside `async def`, move the legacy SDK call to a threadpool if it is I/O-bound, and explain when a worker process is needed instead.

**Example 3:**
Input: "我们想把现在到处 scattered 的鉴权校验整理一下。"
Output: Consolidate repeated checks into reusable dependencies or explicit permission abstractions, reduce duplication in routes, and keep auth context parsing request-scoped and composable.
