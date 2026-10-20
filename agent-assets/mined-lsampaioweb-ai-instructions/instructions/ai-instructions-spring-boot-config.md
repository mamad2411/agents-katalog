---
description: "Spring Boot application configuration contract for YAML settings, environment profiles, and DevTools."
applyTo: "**/src/main/resources/application*.yml, **/src/main/resources/application*.yaml, **/pom.xml"
---

# Spring Boot Configuration Contract

## Configuration files

- Prefer YAML configuration (`application.yml`) over `.properties` files.
- Keep settings shared by every environment in `application.yml`.
- Quote string configuration values consistently in YAML.
- Never commit secrets, passwords, tokens, or private keys as plain values; load them
  from environment variables or an external secret source.

## Virtual threads

- Enablement of `spring.threads.virtual.enabled` is owned by the virtual-threads
  contract. Do not restate or override that flag here.

## Profiles

- Every application ships both profile files:
  - `application-development.yml`
  - `application-production.yml`
- Use the full profile names `development` and `production` only. Never use short forms
  such as `dev`, `prod`, `local`, or `prod-like`.
- Put environment-specific overrides only in the matching profile file (for example
  server port, stack-trace exposure, or Swagger enablement). Actuator health-detail
  overrides are owned by the Actuator contract.
- An optional `application-test.yml` is allowed when automated tests need a dedicated
  profile; do not replace `development` or `production` with `test`.
- Declare the active profile in `application.yml` using list form, with `production` as
  the committed default and `development` available as a commented alternative:

  ```yml
  spring:
    profiles:
      active:
        # - "development"
        - "production"
  ```

- Prefer overriding the active profile at runtime with `SPRING_PROFILES_ACTIVE`, a
  command-line argument, or container/orchestration configuration when switching
  environments, rather than editing committed defaults casually.
- Typical HTTP overrides when the application exposes a web port:
  - `development`: port `8080`, `server.error.include-stacktrace: "always"`
  - `production`: port `9443`, `server.error.include-stacktrace: "never"`
- When OpenAPI/Swagger is present, enable it in `development` and disable it in
  `production`.

## DevTools

- Add `spring-boot-devtools` to every application module that is run locally during
  development.
- Declare it with `runtime` scope and `optional` set to `true`.
- Place it last among Spring Boot / Spring Cloud / Spring Security starters in
  `pom.xml`, before third-party and test dependencies.
- Do not set `spring.devtools.restart.enabled: true` unless you are deliberately
  documenting or overriding the default; Boot already enables restart by default.
- Do not rely on DevTools behavior in production runtime images or production profile
  configuration.

## Forbidden

- Never use short profile names (`dev`, `prod`, or any other alias) for environment
  profiles.
- Never omit `application-development.yml` or `application-production.yml` from an
  application project.
- Never declare `spring.profiles.active` as a scalar string; use the YAML list form.
- Never commit a default active profile of `development` for shared/mainline
  configuration; keep `production` as the committed default.
- Never add `spring-boot-devtools` without `optional=true` and `runtime` scope.
- Never hardcode secrets in `application*.yml` files.
