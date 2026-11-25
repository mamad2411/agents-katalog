---
name: javafx-maven-plugin
description: >
  Extends agent's knowledge of configuring the JavaFX Maven plugin
  for building, running, and packaging JavaFX 21 desktop applications.
  Use when creating or migrating a JavaFX project with Maven.
compatibility: Java 21+
metadata:
  domain: maven
  level: intermediate
  stack: [java-21, javafx-21, maven-3.9]
  version: "1.0.0"
---

# JavaFX Maven Plugin

The `org.openjfx:javafx-maven-plugin` handles classpath setup,
native library extraction, and `jlink`-based runtime images for JavaFX.

## Concepts

- **JavaFX modules** — `javafx-controls`, `javafx-fxml`, `javafx-graphics`,
  `javafx-base`, `javafx-web`, `javafx-media`.
- **Platform classifiers** — `win`, `linux`, `mac`, `mac-aarch64`, `linux-aarch64`.
- **jlink** — creates a custom JRE with only required modules.
- **JavaFX BOM** — import to manage all JavaFX versions atomically.

## Rules

1. Import `org.openjfx:javafx-bom` in `<dependencyManagement>`.
2. Use `javafx-maven-plugin` (not `maven-jar-plugin`) for the main module.
3. Avoid wildcard `*` dependencies — declare each JavaFX module explicitly.
4. Use `mvn javafx:run` during development; `mvn javafx:jlink` for
   production images.
5. Add platform-specific dependencies with `<classifier>` when needed.
6. If module-info exists, add `requires` for each JavaFX module used.
7. Test on all target platforms — JavaFX bundles native libs per OS.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- multi-module-projects — separating core from JavaFX UI
- profiles-environments — platform-specific build profiles
- jpackage-basics — native installer generation
