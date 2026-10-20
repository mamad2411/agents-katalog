---
description: "Spring Boot Security contract for HTTP Basic APIs, deny-by-default filter chains, credentials, and method authorization."
applyTo: "**/pom.xml, **/src/main/resources/application*.yml, **/src/main/resources/application*.yaml, **/*Security*.java, **/security/**/*.java"
---

# Spring Boot Security Contract

These rules apply when an application uses Spring Security. Actuator exposure and
the health-anonymous / other-actuator-authenticated boundary stay in the Actuator
contract. Secrets policy stays in the configuration contract. Do not restate
those contracts here.

An application that exposes private APIs or non-health Actuator endpoints must
meet this contract.

The default auth model is **HTTP Basic with in-memory principals loaded from
environment variables**. A later, more advanced pattern may introduce database-backed
credentials; do not invent that stack unless the product explicitly requires it.

## Dependency

- Add `spring-boot-starter-security` when the application has anything that must
  not be anonymous.
- Add `spring-security-test` with `test` scope when writing security tests.
- Keep a one-line purpose comment above each dependency (pom contract).

## Authentication mechanism

- Use HTTP Basic for REST/API and machine-to-machine callers.
- Do not add form login unless the application is a browser form/MVC app and the
  product explicitly needs it.
- Do not add OAuth2/JWT resource-server or client stacks unless the product
  explicitly requires them.

## Filter chain

- Configure exactly the `SecurityFilterChain` beans the application needs; do not
  rely on Spring Boot's default wide-open or default-user behavior for production
  APIs.
- Deny by default: after explicit public and authenticated rules, end with
  `anyRequest().denyAll()`.
- Permit only routes that must be anonymous (for example a documented public
  health-check style API path, or OpenAPI/Swagger when enabled in development).
- Require authentication or a role for every private API route.
- For pure HTTP Basic REST APIs, set `SessionCreationPolicy.STATELESS` and disable
  CSRF. Keep CSRF enabled for browser form/MVC apps.
- Prefer `@EnableMethodSecurity` and put sensitive authorization checks on service
  methods with `@PreAuthorize` (or equivalent), in addition to URL rules
  (architecture contract: authorization that belongs to the application service).

## Credentials and user store

- Bind credentials through validated `@ConfigurationProperties` (for example under
  `app.security`), not through hardcoded strings in Java.
- Load username and password values from environment variables or an external
  secret source. Never commit plaintext passwords in YAML (configuration
  contract).
- For the default simple model, provision in-memory users with
  `UserDetailsService` / `InMemoryUserDetailsManager`.
- Encode stored passwords with a `PasswordEncoder` bean. Prefer BCrypt.
- Never use `{noop}` password encoding in real applications.
- Do not rely on Boot's `spring.security.user.name` / `spring.security.user.password`
  defaults for real apps; use explicit application properties and a declared
  `UserDetailsService`.
- Do not introduce a database-backed user store unless the product explicitly
  requires persistent accounts.

## Actuator and OpenAPI

- Keep Actuator access rules consistent with the Actuator contract: anonymous
  health (and probes); authenticate every other `/actuator/**` path.
- When Security is present in production, prefer a separate
  `management.server.port` so management traffic is not mixed with the public API
  port (Actuator contract).
- Permit OpenAPI/Swagger routes only when those endpoints are enabled
  (development). Never leave them anonymous in production.

## Testing

- Cover anonymous, authenticated, and deny-unknown paths.
- Cover a wrong-role path only when a route or method declares a role. Do not add a
  role, an endpoint, or an annotation only so that test can exist.
- Distinguish `401` (unauthenticated) from `403` (authenticated but forbidden).
- Cover method-security denials for sensitive service operations when
  `@PreAuthorize` is used.

## Forbidden

- Never leave a secured application on Spring Boot's default generated password
  without an explicit, env-driven credential configuration.
- Never use `{noop}` password encoding in real applications.
- Never commit plaintext security passwords in `application*.yml`.
- Never end a production API filter chain with a blanket `permitAll()`.
- Never omit `anyRequest().denyAll()` after the explicit allow/authenticate rules
  for a deny-by-default API.
- Never enable form login for a pure HTTP Basic REST API by default.
- Never leave non-health Actuator endpoints anonymous (Actuator contract).
- Never leave OpenAPI/Swagger anonymous when those endpoints are enabled in
  production.
