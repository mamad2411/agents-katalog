---
description: "Spring Boot Actuator contract for endpoint exposure, health details, probes, and management hardening."
applyTo: "**/src/main/resources/application*.yml, **/src/main/resources/application*.yaml, **/pom.xml, **/*Actuator*.java, **/*Security*Config*.java"
---

# Spring Boot Actuator Contract

These rules apply to applications that ship Spring Boot Actuator. Profile file
layout and DevTools stay in the configuration contract.
Full HTTP security filter chains stay in the Security topic; this file only
states the Actuator exposure and access boundary.

## Dependency

- Add `spring-boot-starter-actuator` to every real application module.
- Keep a one-line purpose comment above the dependency (pom contract).

## Web exposure

- Expose only a whitelist under `management.endpoints.web.exposure.include`.
- Default include: `health,info,metrics`.
- Keep the default base path `/actuator`. Do not invent a custom base path unless
  the product explicitly requires it.
- Never set `include: "*"`.
- Do not expose sensitive endpoints by default (`env`, `beans`, `configprops`,
  `heapdump`, `threaddump`, `logfile`, `shutdown`, and similar). Add them only
  with an explicit product need and authentication.

## Health details by profile

- In `application.yml`, set `management.endpoint.health.show-details` to
  `when-authorized`.
- In `application-development.yml`, set `show-details` to `always`.
- In `application-production.yml`, set `show-details` to `never`.

## Probes

- For real applications that run in containers or orchestrators, enable
  Kubernetes-style probes:

  ```yml
  management:
    endpoint:
      health:
        probes:
          enabled: true
  ```

- Keep probe enablement in `application.yml` (shared), not only in one profile,
  when the app is meant to be containerized.

## Custom health

- Add a custom `HealthIndicator` only when a real dependency must gate readiness
  (database, broker, remote system). Do not invent vanity indicators.

## Access boundary

- Anonymous callers may reach `/actuator/health` and health probe routes only.
- Every other `/actuator/**` path requires authentication.
- An allow or authenticate rule for an exposed Actuator endpoint covers that endpoint
  and the subpaths it serves.
- When Spring Security is present in production, prefer a separate
  `management.server.port` so management traffic is not mixed with the public
  API port.
- Do not put Actuator credentials in YAML (configuration contract for secrets).

## Forbidden

- Never omit Actuator from a real application module.
- Never expose all endpoints with `include: "*"`.
- Never leave `show-details: always` in production.
- Never leave non-health Actuator endpoints anonymous.
- Never expose `env`, `beans`, `heapdump`, `threaddump`, `logfile`, or `shutdown`
  by default.
