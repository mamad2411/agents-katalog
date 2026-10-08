# EventServer Agent Instructions

Before implementation or refactoring, read in this order:

1. `copilot-instructions.md`
2. `ai/project-context.yaml`

Treat `ai/project-context.yaml` as the authoritative source for system role, architecture constraints, integration boundaries, and AI governance.

Use this file as the repository operating guide: where things live, how to validate, what to inspect first, and when to escalate.

## Repository Map

- This repository is a single Grails 3.2.9 application built with the Gradle wrapper.
- Core business logic is primarily under `grails-app/services/com/hcsaastech/ehis/event`.
- Public entry points include:
  - JAX-RS resources in `grails-app/resources/com/hcsaastech/ehis/event`
  - SOAP and Flex remoting methods in `grails-app/services/com/hcsaastech/ehis/event/EventOutsideService.groovy`
  - GSP UI under `grails-app/views`
- Persistence is GORM and Hibernate over Oracle-backed domain classes in `grails-app/domain/com/hcsaastech/ehis/event`.
- Queue, retry, and scheduled behavior include:
  - `grails-app/services/com/hcsaastech/ehis/event/EventPipelineService.groovy`
  - `src/main/groovy/com/hcsaastech/ehis/Axis2MessageJob.groovy`
- Startup, routing, and bootstrap behavior live in:
  - `grails-app/init/eventserver/Application.groovy`
  - `grails-app/init/eventserver/BootStrap.groovy`
  - `grails-app/controllers/eventserver/UrlMappings.groovy`

## How To Reason About This Repository

- Reason from this repository’s code and docs only.
- Use existing files and patterns as the primary reference for implementation shape.
- Treat legacy behavior as intentional unless the task explicitly requires a verified change.
- Prefer understanding the current flow before editing it, especially in event publishing, retry, compensation, scheduling, startup, and integration entry points.

## Build And Validation

- Use the checked-in wrapper: `gradlew.bat` on Windows.
- Preferred validation order:
  1. `gradlew.bat test`
  2. `gradlew.bat build`
- Prefer the narrowest relevant test scope first when changing a specific event flow, service, or integration path.
- Build resolution depends on internal Artifactory repositories configured in `build.gradle`.
- Integration tests may depend on local access to Oracle and Redis-backed configuration from:
  - `grails-app/conf/application.groovy`
  - `grails-app/conf/application.yml`
- Gradle is configured with `grails.pathingJar = true` to avoid Windows path-length failures. Do not remove or casually alter that setting.
- If validation cannot be run, state that explicitly and identify the blocking dependency.

## What To Inspect First By Change Type

### Event publish / retry / compensation / scheduled flow
Inspect related:
- pipeline control
- retry logic
- compensation flow
- cache usage
- event logs
- scheduled jobs

Start with:
- `grails-app/services/com/hcsaastech/ehis/event/EventPipelineService.groovy`
- `src/main/groovy/com/hcsaastech/ehis/Axis2MessageJob.groovy`

### REST / SOAP / Flex entry-point change
Inspect:
- the entry-point file
- the called service(s)
- related DTO / request / response shape
- linked wiki contract docs before restating or reshaping behavior

### Persistence / domain behavior change
Inspect:
- domain class mapping
- current GORM usage pattern
- affected services
- related tests that already exercise the behavior

### Startup / routing / configuration change
Inspect:
- `grails-app/init/eventserver/Application.groovy`
- `grails-app/init/eventserver/BootStrap.groovy`
- `grails-app/controllers/eventserver/UrlMappings.groovy`
- `grails-app/conf/application.groovy`
- `grails-app/conf/application.yml`
- `grails-app/conf/spring/resources.groovy`

## Representative Patterns

Use these as “look here first” references before inventing a new structure:

- Representative service orchestration:
  - `grails-app/services/com/hcsaastech/ehis/event/EventBrImplService.groovy`
- Representative REST resource:
  - `grails-app/resources/com/hcsaastech/ehis/event/EventResource.groovy`
- Representative domain mapping:
  - `grails-app/domain/com/hcsaastech/ehis/event/EventMst.groovy`
- Representative integration test:
  - `src/test/groovy/com/hcsaastech/ehis/event/EventPublishIntegrationTests.groovy`
- Event-flow tests are concentrated in:
  - `src/test/groovy/com/hcsaastech/ehis/event`

## Docs To Link Instead Of Restating

- Use `wiki/README.md` as the index for diagrams, web services, jobs, UI, and data dictionary references.
- Link web service behavior from:
  - `wiki/WebService/1/README.md`
  - `wiki/WebService/2/README.md`
  - `wiki/WebService/3/README.md`
- Link job behavior from:
  - `wiki/Jobs/1/README.md`
- Link domain reference material from:
  - `wiki/DataDictionary/1/README.md`
- Link UI behavior from the relevant pages under:
  - `wiki/UI`

## Escalate To Human When

Ask for confirmation before proceeding if the task would require any of the following:

- changing externally consumed SOAP or Flex contracts whose version-lock expectations are unclear
- reshaping a REST, DTO, event-code, DB, or UI contract that may be relied on externally
- changing event ordering, retry semantics, compensation behavior, or deduplication behavior
- relying on local validation against shared Oracle or Redis infrastructure when availability is uncertain
- choosing between conflicting sources when wiki behavior and observed legacy behavior diverge
- changing bootstrap assumptions such as timezone, startup wiring, routing defaults, or Spring bean wiring without an explicit task target

## Expected Working Style

- Start from the narrowest relevant files.
- Follow existing implementation patterns before proposing new ones.
- Keep explanations concrete and repository-specific.
- When uncertainty remains, describe exactly what is known from code, what is inferred, and what needs human confirmation.