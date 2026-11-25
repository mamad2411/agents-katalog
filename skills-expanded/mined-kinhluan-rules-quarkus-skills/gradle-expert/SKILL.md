---
name: gradle-expert
description: Expert knowledge for Gradle Build Tool, dependency management, and Gradle-to-Bazel migration. Use for build configuration and project lifecycle questions.
version: 1.2.0
keywords: [gradle, build, kotlin-dsl, migration, java, groovy]
---

# gradle-expert

> Keyword: gradle | Platforms: gemini,claude,codex

Modern Gradle Build Tool Expert Skill - Specialized in performance, dependency management, and polyglot builds.

## Core Mandates

- **DSL Proficiency:** Expert in both **Groovy DSL** (`build.gradle`) and **Kotlin DSL** (`build.gradle.kts`).
- **Dependency Configurations:** Distinguish between `api`, `implementation`, `runtimeOnly`, and `testImplementation`.
- **Build Performance:** Leverage **Build Cache**, **Daemon**, and **Parallel execution** to optimize feedback loops.
- **Convention over Configuration:** Prefer built-in plugins (`java-library`, `application`, `maven-publish`) over custom logic.

## build.gradle.kts Examples

### Quarkus Project

```kotlin
// build.gradle.kts
plugins {
    java
    id("io.quarkus") version "3.20.1"
}

repositories {
    mavenCentral()
}

val quarkusPlatformVersion: String by project  // from gradle.properties

dependencies {
    // BOM - manages all Quarkus versions
    implementation(enforcedPlatform("io.quarkus.platform:quarkus-bom:${quarkusPlatformVersion}"))

    // No versions needed - managed by BOM
    implementation("io.quarkus:quarkus-rest")
    implementation("io.quarkus:quarkus-arc")
    implementation("io.quarkus:quarkus-hibernate-orm-panache")

    // Test
    testImplementation("io.quarkus:quarkus-junit5")
    testImplementation("io.rest-assured:rest-assured")
}

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

tasks.withType<Test> {
    useJUnitPlatform()
    systemProperty("java.util.logging.manager", "org.jboss.logmanager.LogManager")
}
```

### Multi-Module with Version Catalog

```toml
# gradle/libs.versions.toml
[versions]
quarkus = "3.20.1"
jackson = "2.18.2"
junit = "5.11.4"
assertj = "3.27.3"

[libraries]
quarkus-bom = { module = "io.quarkus.platform:quarkus-bom", version.ref = "quarkus" }
quarkus-rest = { module = "io.quarkus:quarkus-rest" }
quarkus-arc = { module = "io.quarkus:quarkus-arc" }
quarkus-hibernate = { module = "io.quarkus:quarkus-hibernate-orm-panache" }
quarkus-junit5 = { module = "io.quarkus:quarkus-junit5" }
jackson-databind = { module = "com.fasterxml.jackson.core:jackson-databind", version.ref = "jackson" }
junit-bom = { module = "org.junit:junit-bom", version.ref = "junit" }
assertj = { module = "org.assertj:assertj-core", version.ref = "assertj" }

[plugins]
quarkus = { id = "io.quarkus", version.ref = "quarkus" }
```

```kotlin
// settings.gradle.kts
rootProject.name = "my-platform"
include("common", "service-user", "service-order")
```

```kotlin
// build.gradle.kts (root)
plugins {
    java
    alias(libs.plugins.quarkus) apply false
}

subprojects {
    apply(plugin = "java")

    repositories {
        mavenCentral()
    }

    dependencies {
        implementation(platform(libs.quarkus.bom))
        implementation(platform(libs.junit.bom))
    }

    java {
        toolchain {
            languageVersion.set(JavaLanguageVersion.of(21))
        }
    }
}
```

```kotlin
// service-user/build.gradle.kts
plugins {
    alias(libs.plugins.quarkus)
}

dependencies {
    implementation(project(":common"))
    implementation(libs.quarkus.rest)
    implementation(libs.quarkus.arc)
    implementation(libs.quarkus.hibernate)

    testImplementation(libs.quarkus.junit5)
    testImplementation(libs.assertj)
}
```

## Dependency Configuration Decision Tree

```
Does the consuming module need this at compile time?
  YES → Does the consuming module also see this in ITS public API?
    YES → api (leaks to consumers' compile classpath)
    NO  → implementation (hidden from consumers)
  NO → Is it needed at runtime only?
    YES → runtimeOnly (e.g., JDBC drivers, SLF4J bindings)
    NO  → Is it only for tests?
      YES → testImplementation
      NO  → compileOnly (e.g., annotation processors, provided-like)
```

### Do vs Don't

```kotlin
// BAD - using 'api' everywhere leaks dependencies, slows compilation
dependencies {
    api("com.google.guava:guava:33.4.0-jre")         // Leaked!
    api("io.quarkus:quarkus-hibernate-orm-panache")    // Leaked!
}

// GOOD - only 'api' what consumers actually need in their code
dependencies {
    api("com.example:shared-dto:1.0")                 // Consumers use these types
    implementation("com.google.guava:guava:33.4.0-jre")  // Internal only
    implementation("io.quarkus:quarkus-hibernate-orm-panache")
}
```

## Version Conflict Resolution Workflow

### Step 1: Identify the conflict

```bash
# Show dependency tree for a specific configuration
./gradlew dependencies --configuration runtimeClasspath

# Filter for a specific module
./gradlew dependencyInsight --dependency jackson-databind --configuration runtimeClasspath

# Output:
# com.fasterxml.jackson.core:jackson-databind:2.18.2
#    variant "compile" [
#       Requested: 2.14.0  ← conflict
#       Selected:  2.18.2  ← Gradle picked highest
#    ]
```

### Step 2: Understand Gradle's resolution strategy

Gradle uses **highest version wins** by default. This is usually safe but can break binary compatibility.

### Step 3: Resolve

```kotlin
// Option A: Force a specific version (use sparingly)
configurations.all {
    resolutionStrategy {
        force("com.fasterxml.jackson.core:jackson-databind:2.18.2")
    }
}

// Option B: Use a BOM/platform (preferred)
dependencies {
    implementation(platform("com.fasterxml.jackson:jackson-bom:2.18.2"))
    // All Jackson modules now use 2.18.2
}

// Option C: Exclude transitive dependency
dependencies {
    implementation("some-lib:some-lib:1.0") {
        exclude(group = "com.fasterxml.jackson.core", module = "jackson-databind")
    }
}

// Option D: Fail on conflict (strict mode for CI)
configurations.all {
    resolutionStrategy {
        failOnVersionConflict()
    }
}
```

### Resolution Priority

| Priority | Strategy | When to use |
|----------|----------|-------------|
| 1st | BOM / `platform()` | When a BOM exists (jackson-bom, netty-bom, quarkus-bom) |
| 2nd | Version Catalog | Centralize versions in `libs.versions.toml` |
| 3rd | `exclude()` | When one lib brings a known bad transitive |
| 4th | `force()` | Last resort - overrides everything, can mask issues |

## Common Errors & Fixes

### "Could not resolve all dependencies"

```kotlin
// Cause: Missing repository or wrong coordinates
repositories {
    mavenCentral()
    // Add private repo if needed:
    maven {
        url = uri("https://nexus.example.com/repository/maven-releases/")
        credentials {
            username = providers.environmentVariable("MAVEN_USER").orNull
            password = providers.environmentVariable("MAVEN_TOKEN").orNull
        }
    }
}
```

### "Execution failed: A valid toolchain could not be found"

```kotlin
// Fix: Specify Java toolchain
java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

// Or in gradle.properties:
// org.gradle.java.home=/path/to/jdk21
```

### Build cache not working

```properties
# gradle.properties
org.gradle.caching=true
org.gradle.parallel=true
org.gradle.daemon=true
org.gradle.jvmargs=-Xmx4g -XX:+HeapDumpOnOutOfMemoryError
```

```kotlin
// settings.gradle.kts - remote cache
buildCache {
    local {
        isEnabled = true
    }
    remote<HttpBuildCache> {
        url = uri("https://cache.example.com/cache/")
        isPush = System.getenv("CI") != null  // Only push from CI
    }
}
```

### "Cannot change dependencies after configuration resolution"

```kotlin
// BAD - resolving a configuration during configuration phase
val runtimeJars = configurations.runtimeClasspath.get().files  // Triggers resolution!

// GOOD - defer to execution phase
tasks.register("listDeps") {
    val runtimeCp = configurations.runtimeClasspath
    doLast {
        runtimeCp.get().files.forEach { println(it) }
    }
}
```

### Slow builds diagnostic

```bash
# Generate build scan (interactive report)
./gradlew build --scan

# Profile locally
./gradlew build --profile
# Opens report in build/reports/profile/

# Check configuration cache compatibility
./gradlew build --configuration-cache
```

### Slow builds optimization checklist

| Check | Action |
|-------|--------|
| Daemon enabled? | `org.gradle.daemon=true` in gradle.properties |
| Parallel builds? | `org.gradle.parallel=true` |
| Build cache? | `org.gradle.caching=true` |
| Configuration cache? | `--configuration-cache` (Gradle 8.1+) |
| Unnecessary `api` deps? | Switch to `implementation` to reduce recompilation |
| `allprojects{}` / `subprojects{}` blocks? | Migrate to convention plugins |
| Task Configuration Avoidance? | Use `tasks.register` not `tasks.create` |

## Gradle-to-Bazel Migration

### Configuration Mapping Table

| Gradle | Bazel | Notes |
|--------|-------|-------|
| `api` | `exports = [...]` | Visible to transitive consumers |
| `implementation` | `deps = [...]` | Hidden from consumers |
| `runtimeOnly` | `runtime_deps = [...]` | Not on compile classpath |
| `compileOnly` | `deps = [...] + neverlink = True` | Compile but not package |
| `testImplementation` | test target `deps` | Separate test target |
| `project(":sub")` | `"//sub:target"` | Bazel label |
| `./gradlew build` | `bazel build //...` | Build all |
| `./gradlew test` | `bazel test //...` | Test all |
| Version Catalog | `rules_jvm_external` | Different mechanism |

### Exporting Dependencies for Bazel

```bash
# Generate dependency list from Gradle
./gradlew dependencies --configuration runtimeClasspath \
  | grep '\\---' | sed 's/.*--- //' | sort -u

# Then translate to rules_jvm_external format in MODULE.bazel
```

## Advanced Patterns

- **Build Scan:** Using Gradle Build Scans for debugging performance and dependency issues.
- **Custom Tasks:** Writing idiomatic tasks using the **Task Configuration Avoidance API**.
- **Version Catalogs:** Managing versions and libraries centrally via `libs.versions.toml`.

## Expert Tips

- Avoid using the deprecated `compile` configuration; use `implementation` or `api`.
- Use `./gradlew dependencies --configuration runtimeClasspath` to visualize the dependency graph.
- Prefer **Kotlin DSL** for better IDE support and type safety in complex builds.
- Use `gradle wrapper --gradle-version=8.12` to pin Gradle version for reproducibility.
- Always use `tasks.register` (lazy) over `tasks.create` (eager) for Task Configuration Avoidance.
- Use `./gradlew build --dry-run` to preview task execution order without running anything.

## 🌐 Gradle Knowledge Sources

> **Directive:** Use `web_fetch` to find Kotlin DSL syntax, version catalog patterns, or Gradle-to-Bazel migration strategies if a build configuration is complex.

- **Gradle Kotlin DSL Primer:** [Kotlin DSL Guide](https://docs.gradle.org/current/userguide/kotlin_dsl.html) - Type-safe build scripts.
- **Dependency Management:** [Managing Dependencies](https://docs.gradle.org/current/userguide/dependency_management.html) - Configurations, platforms, and catalogs.
- **Gradle-to-Bazel Migration:** [Migrating from Gradle to Bazel](https://bazel.build/migrate/gradle) - Step-by-step transition.
- **Build Performance:** [Optimizing Gradle Builds](https://docs.gradle.org/current/userguide/performance.html) - Cache, daemon, and parallel execution.
- **Quarkus Gradle Tooling:** [Quarkus Gradle Guide](https://quarkus.io/guides/gradle-tooling) - Plugin configuration.

## References

- [Gradle Official User Guide](https://docs.gradle.org/current/userguide/userguide.html)
- [rules_jvm_external Documentation](https://github.com/bazelbuild/rules_jvm_external)
- [Gradle Version Catalogs](https://docs.gradle.org/current/userguide/platforms.html#sub:version-catalog)
- [Quarkus Documentation](https://quarkus.io/guides/)

## Skill Interoperability

The **gradle-expert** 🐘 skill provides expertise in modern build DSLs and performance, supporting:
- **rules-quarkus** 🔧: Facilitates the migration of Gradle-based projects to Bazel.
