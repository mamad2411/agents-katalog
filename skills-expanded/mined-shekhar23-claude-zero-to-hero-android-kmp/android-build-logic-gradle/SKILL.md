---
name: android-build-logic-gradle
description: |
  Gradle build logic patterns for Android/KMP - convention plugins, version catalogs, module consistency, build performance, and scalable project configuration. Use this skill whenever organizing shared Gradle setup, adding convention plugins, standardizing module configs, or deciding where build rules should live in a modular Android repository. Trigger on phrases like "Gradle", "build logic", "convention plugin", "version catalog", "build-logic", "module config", or "shared build setup".
---

# Android Build Logic and Gradle

## Core Principles

- Shared build rules belong in build logic, not copied across modules.
- Prefer convention plugins over large repeated `build.gradle.kts` blocks.
- Use version catalogs for dependency and version management.
- Keep module build files small, declarative, and predictable.
- Optimize build logic for clarity first, then performance.

---

## Recommended Ownership

A modular Android repo typically keeps shared build logic in:

```text
:build-logic
  -> convention plugins
  -> shared Gradle configuration helpers
  -> plugin dependency setup
```

Application and library modules should mostly apply plugins and declare only module-specific dependencies/options.

See the **android-module-structure** skill for the broader architecture view.

---

## Convention Plugins

Use convention plugins for repeated setup such as:
- Android application defaults
- Android library defaults
- feature module defaults
- Compose setup
- Koin setup
- Room/KSP setup
- Kotlin serialization setup
- test stack defaults

Example plugin names:
- `android-application`
- `android-library`
- `android-feature`
- `domain-module`
- `compose`
- `koin`
- `room`

A module should read more like configuration selection than low-level build wiring.

---

## Version Catalogs

Use `libs.versions.toml` for:
- library coordinates
- plugin coordinates
- shared versions
- bundles when they improve clarity

Rules:
- avoid hardcoded versions in module build files
- keep aliases clear and stable
- do not create confusing micro-aliases that hide meaning

Good alias examples:
- `libs.androidx.core.ktx`
- `libs.kotlinx.coroutines.core`
- `libs.plugins.android.application`

---

## Module Build File Shape

A good module build file is short:

```kotlin
plugins {
    alias(libs.plugins.myapp.android.feature)
}

android {
    namespace = "com.example.feature.notes"
}

dependencies {
    implementation(projects.feature.notes.domain)
    implementation(projects.core.presentation)
}
```

Avoid repeating the same compile SDK, Kotlin options, Compose flags, test options, or packaging exclusions in every module.

---

## Dependency Hygiene

Keep dependency direction clean:
- `presentation` depends inward
- `data` depends on domain/core data
- features do not depend on each other
- `:app` wires everything together

Build logic should reinforce this structure, not blur it.

Examples:
- feature plugin can provide common Android/Compose/test setup
- it should not automatically inject unrelated feature dependencies

---

## Build Performance Basics

Useful practices:
- avoid unnecessary all-module configuration
- keep plugin code simple and lazy where possible
- reduce annotation processing scope
- prefer incremental-friendly tooling
- review expensive tasks before adding more build complexity

Do not over-engineer build logic for tiny gains in small repos.

---

## KSP, KAPT, and Generated Code

Guidelines:
- prefer KSP when supported by the library/tooling
- centralize processor setup in convention plugins
- expose generated-source requirements consistently
- avoid mixed patterns across modules unless necessary

For Room or serialization setup, shared plugin configuration reduces drift.

---

## Environment and Signing Config

Build logic may help expose environment-aware config, but secrets still must stay outside source control.

Good uses:
- reading local properties for development-only config
- wiring build config fields consistently
- separating debug/staging/release config behavior

Bad uses:
- embedding production secrets in plugin code
- spreading secret lookup logic across many modules

---

## Testing Build Logic

When build logic becomes non-trivial:
- keep plugin code small and composable
- test critical helpers where practical
- document plugin purpose and expected module usage

The more custom plugin code exists, the more important clear naming and docs become.

---

## When to Create a New Convention Plugin

Create one when:
- 3 or more modules repeat the same config
- a setup has clear conceptual ownership
- consistency matters across many modules

Do not create one when:
- it wraps a single one-line plugin apply with no shared value
- it hides too much magic
- only one module needs the setup

---

## Checklist: Improving Build Logic

- [ ] Move repeated module config into convention plugins
- [ ] Keep versions and plugin aliases in `libs.versions.toml`
- [ ] Keep module build files short and declarative
- [ ] Centralize KSP/Kotlin/Compose/test defaults where shared
- [ ] Preserve clean dependency direction across modules
- [ ] Avoid hiding secrets or excessive magic in build logic