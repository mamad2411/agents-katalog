---
name: multi-module-projects
description: >
  Extends agent's knowledge of structuring Maven multi-module projects.
  Use when designing a new project with shared core, desktop UI, and
  integration layers that must build as a single reactor.
compatibility: Java 21+
metadata:
  domain: maven
  level: intermediate
  stack: [java-21, maven-3.9]
  version: "1.0.0"
---

# Multi-Module Maven Projects

Parent POM defines modules, dependencyManagement, and pluginManagement.
Each child inherits version and groupId from the parent.

## Concepts

- **Reactor** — Maven builds all modules in dependency order; upstream
  modules are available to downstream ones without installing.
- **dependencyManagement** — declares versions in parent; children
  omit `<version>`.
- **pluginManagement** — declares plugin configs in parent; children
  reference by `<plugin>` without `<version>`.
- **Relative path** — `<relativePath/>` in child prevents Maven from
  searching filesystem first (speeds up CI).

## Rules

1. Parent POM packaging must be `<packaging>pom</packaging>`.
2. Declare all module versions in parent `<dependencyManagement>`.
3. Children reference parent with explicit `<version>`.
4. Use `<pluginManagement>` in parent for compiler, surefire, jar plugins.
5. Each module has a single responsibility (core, ui, app, it).
6. Inter-module deps use `${project.version}` in the reactor.
7. Verification modules (it) should come last in `<modules>` list.
8. Never duplicate version numbers — single source of truth in parent.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- dependency-management — version conflict resolution
- shading-and-packaging — uber-jar creation
- profiles-environments — dev/staging/prod configuration
