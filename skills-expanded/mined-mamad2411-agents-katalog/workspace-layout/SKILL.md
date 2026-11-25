---
name: workspace-layout
description: >
  Extends agent's knowledge of Maven multi-module JavaFX project structure using
  ui-kickstartfx conventions. Use when scaffolding a new desktop app, organizing
  packages, or setting up a maintainable module hierarchy.
compatibility: Java 21+
metadata:
  domain: ui-kickstartfx
  level: beginner
  stack: [java-21, javafx-21, maven-3.9]
  version: "1.0.0"
---

# Workspace Layout

A well-structured Maven multi-module project prevents circular dependencies,
enables independent module testing, and keeps JavaFX concerns isolated.

## Concepts

- **Root POM**: defines `<dependencyManagement>` and `<modules>`, no source code
- **app module**: `Application` class, `module-info.java`, assembles all modules
- **core module**: domain logic, services, entities — zero JavaFX imports
- **ui module**: FXML files, controllers, CSS — depends on core, never the reverse
- **resources module** (optional): shared CSS, fonts, images across UI modules

## Rules

1. Root `pom.xml` only has `<modules>` and dependencyManagement — never put source there.
2. `core` module must not import any `javafx.*` package — keep it toolkit-agnostic.
3. Define `module-info.java` in every module with explicit `requires` clauses.
4. One package per concern: `com.pos.core.product`, not `com.pos.core.utils` catch-alls.
5. Keep FXML files adjacent to their controller in `src/main/resources`.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- navigation-patterns — structuring flows between views
- sidebar-shell-architecture — main window shell conventions
