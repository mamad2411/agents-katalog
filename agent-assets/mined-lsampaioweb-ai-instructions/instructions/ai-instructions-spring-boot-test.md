---
description: "Spring Boot testing contract for context-load tests, WebMvc slices, service unit tests, and verification boundaries."
applyTo: "**/src/test/java/**/*.java, **/pom.xml"
---

# Spring Boot Testing Contract

These rules apply to automated tests in real application modules. i18n key-parity
tests stay in the i18n contract. Compile/test verification after edits stays in
the Java style contract. Security assertion expectations stay in the Security
contract. HTTP load scripts stay in the k6 contract; do not run k6 from Maven
Surefire. Do not restate those contracts here.

Applications must meet this contract for every feature they ship.

## Dependencies

- Add `spring-boot-starter-test` with `test` scope to every application module.
- Add `spring-boot-starter-webmvc-test` with `test` scope when the module has a
  REST controller. Real REST apps always ship `@WebMvcTest`.
- Import `@WebMvcTest` from `org.springframework.boot.webmvc.test.autoconfigure`.
  On Spring Boot 4, `spring-boot-starter-test` does not provide this class.
- Add `spring-security-test` with `test` scope when the module tests Spring
  Security behavior.
- Keep a one-line purpose comment above each dependency (pom contract).
- Place test-scoped dependencies last in `pom.xml` (pom contract).

## Mandatory baseline

- Every application module has an `*ApplicationTests` class annotated with
  `@SpringBootTest` that proves the Spring context loads.
- Every module with message bundles also has an `I18nConsistencyTest` (or
  equivalent) as required by the i18n contract.

## REST controller tests

- For each REST feature controller, ship at least one `@WebMvcTest` (or
  equivalent MockMvc slice) covering:
  - one happy-path request
  - one validation or domain-error path
- Declare the service **interface** mock at class level with `@MockitoBean` (or
  the current Boot mock annotation); constructor-inject mocks used by test methods.
  Do not call a real database from a controller slice test.
- Assert HTTP status, important headers (for example `Location` on create), and
  key JSON fields.
- Prefer `@WebMvcTest` over a full `@SpringBootTest` for controller HTTP
  contract checks.

## Service tests

- Protect non-trivial business rules with pure unit tests using
  `@ExtendWith(MockitoExtension.class)` and `@Mock` collaborators.
- Construct the service implementation under test directly; do not start a
  Spring context for ordinary service unit tests.
- Name these classes `*ServiceImplTest` or `*ServiceTest`.

## Security and full-context tests

- When Spring Security is present, cover the paths required by the Security contract
  with `spring-security-test`.
- Reserve full `@SpringBootTest` + MockMvc for filter-chain, actuator access,
  OpenAPI profile, or other cross-cutting wiring that a slice cannot express
  honestly.
- When generated documentation supports locale switching, use full-context MockMvc
  with filters to check locale-sensitive output for two supported locales.
- When generated documentation exposes JSON or YAML routes, use full-context
  MockMvc with filters to check each enabled format and denial of disabled routes
  according to the Security contract; do not require formats the app does not enable.
- Use `@ActiveProfiles("test")` and an optional `application-test.yml` only when
  the test needs dedicated overrides; do not replace `development` /
  `production` application profiles with `test` in main config (configuration
  contract).

## Naming and style

- Use clear names: `*ApplicationTests`, `*ControllerTest`, `*ServiceImplTest` /
  `*ServiceTest`, `I18nConsistencyTest`.
- Prefer AssertJ assertions from `spring-boot-starter-test`.
- Keep tests focused: one behavior per test method when practical.

## Environment-dependent tests

- Tests that require a live database, broker, container runtime, or external
  network service must not be deleted, skipped, or weakened merely to make a
  local run green (Java style contract).
- When such infrastructure is unavailable, report the result as
  environment-dependent rather than pretending the test passed.

## Forbidden

- Never omit context-load coverage from a real application module.
- Never import `@WebMvcTest` from
  `org.springframework.boot.test.autoconfigure.web.servlet`.
- Never use `@DataJpaTest`, JPA test slices, or other ORM test starters (JDBC /
  architecture contracts).
- Never hit a real database from a `@WebMvcTest` controller slice.
- Never mock a concrete service implementation for controller tests when a
  service interface exists; mock the interface.
- Never require Testcontainers in this baseline contract unless the product
  explicitly adopts them.
- Never delete, skip, or weaken failing tests only to obtain a green build.
