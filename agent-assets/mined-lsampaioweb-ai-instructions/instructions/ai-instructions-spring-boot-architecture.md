---
description: "Spring Boot Java architecture contract for feature packaging, service boundaries, repositories, DTOs, mappers, and controller dependencies."
applyTo: "**/src/**/*.java"
---

# Spring Boot Java Architecture Contract

## Package organization

- Organize application code by business feature, not by technical layer.
- Keep a feature's controller, service, service implementation, repository contract,
  repository implementation, domain model, request/response DTOs, mapper, and feature
  exceptions in that feature package.
- Use dedicated shared packages only for genuinely cross-cutting infrastructure such as
  configuration, exception handling, internationalization, OpenAPI setup, persistence
  configuration, filters, and event infrastructure.
- Do not create broad top-level `controller`, `service`, `repository`, `model`, or `dto`
  packages that collect classes from multiple business features.

## Dependency direction

- Controllers, page controllers, and message endpoints depend on service interfaces only.
- Services depend on repository interfaces, mappers, and shared infrastructure as needed.
- Repository implementations contain persistence or external-data access and are hidden
  behind repository interfaces.
- Controllers must never inject or call repository classes directly.
- Do not place business rules, persistence calls, or DTO mapping logic in controllers.
- Keep dependency injection constructor-based; do not use field injection.

## Services

- Every application feature has a service interface and a separate implementation class:
  `<Feature>Service` and `<Feature>ServiceImpl`.
- Annotate only the implementation with `@Service`.
- Put business orchestration, transaction boundaries, authorization checks that belong to
  the application service, and conversion coordination in the service implementation.
- A service may be thin when the feature has little business logic, but do not bypass the
  service layer for convenience.

## Repositories

- Every repository has an interface and a separate implementation class:
  `<Feature>Repository` and `<Feature>RepositoryImpl`.
- Annotate only the implementation with `@Repository`.
- Keep database, cache, or external-system access inside the repository implementation.
- Keep the persistence technology behind the repository interface so implementations can
  be replaced or tested independently.
- Do not expose JDBC templates, Redis operations, `RestClient`, or vendor-specific
  types through service or controller contracts.
- The default relational persistence approach is Spring JDBC, not ORM.

## DTOs and mapping

- Keep API or UI boundary types separate from domain/model types.
- Use dedicated request and response DTOs for externally visible input and output.
- Create a dedicated `<Feature>Mapper` for domain-to-DTO and
  DTO-to-domain conversion, even when the conversion is small.
- Do not map DTOs inline inside controllers or service implementations.
- Keep request validation annotations on request DTOs and apply `@Valid` at the input
  boundary (exception contract owns the full validation rules).

## Endpoint naming

- REST endpoints use `<Feature>RestController`.
- Server-rendered MVC endpoints use `<Feature>PageController`.
- WebSocket/STOMP message endpoints use `<Feature>SocketController`.
- HTTP endpoint classes must remain thin and delegate to a service interface.
- Use protocol-specific suffixes so instruction routing and code review can distinguish
  REST, server-rendered MVC, and WebSocket behavior.

## Models and visibility

- Keep domain models free of persistence-framework annotations.
- Never use JPA entities, `@Entity`, `JpaRepository`, or Hibernate mappings.
- Prefer package-private implementation classes and public boundary types when the module
  does not require cross-package access.
- Use names that expose the feature and responsibility: `<User>Service`,
  `<User>ServiceImpl`, `<User>Repository`, `<User>RepositoryImpl`, `<User>Request`,
  `<User>Response`, and `<User>Mapper`.

## Exceptions

- Keep feature-specific exceptions beside the feature that owns them.
- Keep global exception translation in a shared exception-handling package.
- Services may throw domain exceptions; controllers should not construct persistence or
  infrastructure exceptions directly.

## Forbidden

- Never organize a multi-feature application primarily into technical-layer packages.
- Never inject a repository into a controller.
- Never put business logic or DTO mapping in a controller.
- Never use a concrete service without its service interface and implementation pair.
- Never use a concrete repository without its repository interface and implementation pair.
- Never map request/response DTOs inline in a controller or service implementation.
- Never name a feature mapper `*DtoMapper`; the canonical name is `<Feature>Mapper`.
- Never use field injection with `@Autowired`.
- Never introduce JPA/Hibernate persistence.
- Never name a REST endpoint `<Feature>Controller`; use `<Feature>RestController`.
- Never name a server-rendered MVC endpoint `<Feature>Controller` or
  `<Feature>RestController`; use `<Feature>PageController`.
- Never name a WebSocket/STOMP endpoint `<Feature>Controller`; use
  `<Feature>SocketController`.
