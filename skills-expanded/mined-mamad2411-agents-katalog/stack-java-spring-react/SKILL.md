---
name: stack-java-spring-react
description: "Java 25 + Spring Boot 4.1 / Spring Modulith, PostgreSQL 17 + Flyway, Spring Security OAuth2 resource server, Testcontainers, React front end. Use when a project's Skills line names this stack - build, test, review or secure code on it."
---

# Stack pack: Java + Spring Boot + PostgreSQL + React

> Loaded per project (the project's `**Skills:**` line + `load-skills.sh`), never written into a persona
> (RULES.md -> ## tools-on-demand; row 263). Named by technology, never by product. Project facts -
> module names, lanes, ports - live in that project's `_memory/` and `architecture.md`, not here.

## The stack

- **Java 25 LTS**, **Spring Boot 4.1**, **Spring Modulith** (one module per bounded context; module
  boundaries are verified by `ApplicationModules.verify()` in a test - a cross-module call through an
  internal type is a build failure, not a review comment).
- **PostgreSQL 17** with **Flyway** migrations; JPA runs with `ddl-auto=validate` - the schema changes
  only through a new migration, never by Hibernate and never by editing an applied migration.
- **Spring Security OAuth2 resource server** (JWT). The tenant comes from the authenticated principal,
  never from a request header, path or body.
- **Testcontainers** for integration tests (real PostgreSQL), **Docker Compose** for local services.
- **React** front end (TypeScript); E2E with Playwright.

## Every role

- Test-first. A test class must match surefire's default patterns (`*Test`, `*Tests`, `Test*`) or be
  included explicitly - a suite surefire does not pick up is a silent no-op, not green. Check the
  surefire report lists it (LESSONS 2026-09-30).
- Read the project's `architecture.md` for the module list before planning lanes; one lane never
  touches two modules' internals.

## By role

- **Lead (Development):** split work into the standard lanes over Java modules or `ui/`; the approved
  plan names which lane owns which module.
- **Developers:** one worktree per lane; a change crossing a module boundary goes through the module's
  published API or an application event, never an internal class.
- **Security:** auth review on the resource-server config; tenant-from-principal everywhere; PostgreSQL
  row-level security policies on tenant tables, with a negative test that RLS denies a forged tenant
  with policies on (and a RED run with policies disabled); dependency and secret scans across Java and Node.
- **Code review:** Java/Spring and React diffs; WCAG AA on the React front end (canvas and diagram
  editors included); Flyway migration reviewed as code.
- **QA automation:** Playwright against the React front end; integration suites on Testcontainers
  (Docker Compose services); smoke run before release.
