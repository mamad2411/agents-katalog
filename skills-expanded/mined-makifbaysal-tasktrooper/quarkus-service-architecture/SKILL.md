---
name: quarkus-service-architecture
category: architecture
description: Use when building or extending a Java service with Quarkus - layered architecture, JAX-RS resources, CDI beans, Panache persistence, and native-friendly patterns
tech_stack: Java
---
# Quarkus Service Architecture

## Overview

Quarkus is the default Java stack: fast startup, low memory, native-image friendly — the closest Java gets to Go's operational profile. Build services in clean layers so the framework stays at the edges and the domain stays plain Java.

**Core principle:** Framework annotations live at the boundaries (resources, repositories). The domain and services are plain classes you can unit-test without booting Quarkus.

## Layers

| Layer | Responsibility | Quarkus surface |
|-------|----------------|-----------------|
| Resource | HTTP in/out, validation, status codes | `@Path`, JAX-RS (`@GET`/`@POST`), `@Valid` |
| Service | Use-case orchestration, business rules | `@ApplicationScoped` CDI bean, constructor-injected |
| Domain | Entities, value objects, invariants | plain Java, no annotations driving behavior |
| Repository | Persistence | Panache (`PanacheRepository`) or JPA |

Dependencies point inward: resource → service → domain; repository implements a port the service depends on. A resource never contains business logic; a service never touches `RoutingContext` or JAX-RS types.

## Patterns

- **Constructor injection**, not field injection: `public TaskService(TaskRepository repo)`. Constructor injection is testable without CDI and makes dependencies explicit.
- **DTOs at the edge**: resources accept/return DTOs (records), map to/from domain in the service. Never expose JPA entities directly over HTTP.
- **Bean Validation** on request DTOs (`@NotNull`, `@Size(max=200)`) + `@Valid` on the resource method — validate at the boundary, reject early.
- **Reactive vs imperative**: default to imperative (Quarkus REST — formerly branded "RESTEasy Reactive" — with blocking) unless the task is genuinely reactive; don't sprinkle `Uni`/`Multi` without cause. A blocking-I/O-heavy endpoint on Java 21+ may run on a virtual thread instead (`@RunOnVirtualThread`) rather than going reactive.
- **Config** via `@ConfigProperty` from `application.properties`/env — never hardcode. Group related settings with `@ConfigMapping` instead of a pile of individual `@ConfigProperty` fields.
- **Error mapping** centrally with `@ServerExceptionMapper`, returning `RestResponse<ProblemDto>` (or the repo's equivalent) — not a `try/catch` per resource method (api-design-conventions has the shape).
- **Dev Services** start a throwaway Postgres automatically in dev/test when no `quarkus.datasource.jdbc.url` is set — don't hand-wire a local Postgres for local iteration unless the repo has opted out.
- **Schema management** outside tests is `quarkus.hibernate-orm.schema-management.strategy=none` (or `validate`); this property was renamed from `quarkus.hibernate-orm.database.generation` in 3.23 — use the current name unless the repo is pinned to an older Quarkus.
- Target the current LTS (3.40, supported to 2027-09); never move a repo onto the Quarkus 4 beta in a feature task.

## Worked Example

`POST /tasks` creating a task:

```java
// resource (boundary)
@Path("/tasks")
public class TaskResource {
    private final TaskService service;
    public TaskResource(TaskService service) { this.service = service; }

    @POST
    public Response create(@Valid CreateTaskRequest req) {
        Task t = service.create(req.title());
        return Response.status(201).entity(TaskResponse.from(t)).build();
    }
}

// service (plain, unit-testable without Quarkus)
@ApplicationScoped
public class TaskService {
    private final TaskRepository repo;
    public TaskService(TaskRepository repo) { this.repo = repo; }

    @Transactional
    public Task create(String title) {
        Task t = Task.create(title);   // domain enforces the <=200 invariant
        repo.persist(t);
        return t;
    }
}
```

`CreateTaskRequest` is a record with `@Size(max=200) String title`. The `<=200` invariant is ALSO enforced in `Task.create` so the rule holds even when called from a non-HTTP path.

## Common Mistakes

- Business logic in the resource — it belongs in the service.
- Returning JPA entities over HTTP (leaks schema, causes lazy-loading serialization errors).
- Field injection (`@Inject` on a field) — breaks plain unit testing.
- `@Transactional` on the resource instead of the service.

## Red Flags

- A JAX-RS import inside a domain or service test.
- A service method that takes a JAX-RS or servlet type.
- Validation only on the DTO, with the domain invariant unprotected.
