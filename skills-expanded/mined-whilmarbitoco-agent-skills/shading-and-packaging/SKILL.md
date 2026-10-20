---
name: shading-and-packaging
description: >
  Extends agent's knowledge of creating Maven uber-jars with
  maven-shade-plugin, including resource transformers and class
  relocation. Use when producing a single executable jar for
  distribution.
compatibility: Java 21+
metadata:
  domain: maven
  level: intermediate
  stack: [java-21, maven-3.9]
  version: "1.0.0"
---

# Shading and Packaging

`maven-shade-plugin` packages all dependencies into a single uber-jar.
It can also **relocate** classes to avoid conflicts when the same library
appears in the app and its consumers.

## Concepts

- **Uber-jar** — one file with all classes + resources from deps.
- **Relocation** — moves a package to a new name at build time (e.g.,
  `com.google.common` → `shaded.com.google.common`).
- **Resource transformers** — merge `META-INF/services`, `spring.handlers`,
  etc. that would otherwise be overwritten.
- **Minimize jar** — removes unused classes to reduce size.

## Rules

1. Use `maven-shade-plugin` over `maven-assembly-plugin` for uber-jars.
2. Configure `ServicesResourceTransformer` for `META-INF/services` files.
3. Relocate conflicting deps (e.g., gRPC, Guava, Netty) to `shaded.*`.
4. Use `<minimizeJar>true</minimizeJar>` to strip unused classes.
5. Set `<createDependencyReducedPom>false</createDependencyReducedPom>`
   to preserve original dependency info for consumers.
6. Add a `Main-Class` manifest entry in the shade config.
7. Test the shaded jar explicitly: `java -jar target/app-shaded.jar`.
8. Never shade provided-scope dependencies.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- dependency-management — managing versions before shading
- jpackage-basics — native packaging alternative
- reproducible-builds — ensuring jar is bit-for-bit identical
