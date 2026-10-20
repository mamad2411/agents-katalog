---
description: "Spring Boot virtual-threads contract for enabling Loom on servlet apps and avoiding custom executors."
globs: "**/src/main/resources/application*.yml,**/src/main/resources/application*.yaml,**/*Config*.java,**/*Configuration*.java"
alwaysApply: false
---

# Spring Boot Virtual Threads Contract

These rules apply to servlet/MVC applications. A deployable servlet app must
meet this contract. YAML layout and profiles stay in the configuration contract.
Outbound `RestClient` setup stays in the HTTP-client contract.

## Enablement

- Enable virtual threads in shared `application.yml` (not only in one profile):

  ```yml
  spring:
    threads:
      virtual:
        enabled: true
  ```

- Keep the same value for `development` and `production`. Do not disable virtual
  threads in production as a default.

## Runtime model

- Keep the blocking servlet stack: MVC, JDBC, and `RestClient`.
- Do not switch the application to WebFlux to get concurrency.
- Do not add a custom `TaskExecutor`, `VirtualThreadTaskExecutor`, or
  `Executors.newVirtualThreadPerTaskExecutor()` bean unless the product needs a
  named executor beyond Spring Boot's default.
- Do not lower `server.tomcat.threads.max` as a virtual-thread trick unless you
  are measuring a specific experiment.

## Forbidden

- Never omit `spring.threads.virtual.enabled: true` from a real servlet/MVC app.
- Never place that flag only in `application-development.yml` or only in
  `application-production.yml`.
- Never introduce WebFlux solely to handle blocking I/O concurrency.
- Never add a custom virtual-thread executor as the application's default
  request concurrency mechanism.
- Never require a Tomcat `max` thread override to "enable" virtual threads.
