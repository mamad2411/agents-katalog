---
name: profiles-environments
description: >
  Extends agent's knowledge of Maven profiles for environment-specific
  configuration (dev, staging, prod). Use when setting up builds that
  behave differently across environments.
compatibility: Java 21+
metadata:
  domain: maven
  level: intermediate
  stack: [java-21, maven-3.9]
  version: "1.0.0"
---

# Profiles and Environments

Maven profiles let you activate different dependencies, plugins, and
properties based on OS, JDK, or a `-P` flag. They replace environment-
specific `pom.xml` files.

## Concepts

- **Activation** — by OS, JDK, property, file existence, or activeByDefault.
- **Properties per profile** — `<properties>` inside `<profile>` override
  global defaults.
- **Profile-specific dependencies** — add a test DB driver only in dev.
- **Resource filtering** — replace `${placeholder}` in `application.properties`.

## Rules

1. Define a `dev` profile (active by default) with debug deps/tools.
2. Define a `prod` profile with optimizations (minify, strip debug info).
3. Use `-Pprod` in CI to activate production profile.
4. Never put secrets in profiles — use environment variables +
   resource filtering instead.
5. Use `<activation><activeByDefault>true</activeByDefault></activation>`
   for exactly one profile. Note: `activeByDefault` profiles are automatically
   deactivated when any other profile is activated via `-P` or activation condition.
6. Prefer `<property>` activation (`-Denv=prod`) for flexibility.
7. Resource filtering: enable `<filtering>true</filtering>` in
   `<resource>` and use `${property}` placeholders.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- multi-module-projects — profiles that apply to specific modules
- reproducible-builds — pinning profile-dependent versions
- dependency-management — per-profile dependency sets
