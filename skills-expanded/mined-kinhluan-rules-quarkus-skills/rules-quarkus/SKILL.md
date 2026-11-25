---
name: rules-quarkus
description: Expert knowledge for building Quarkus applications with Bazel using the rules_quarkus build system. Use when user asks about Quarkus+Bazel builds, augmentation, or troubleshooting.
version: 1.3.0
keywords: [rules-quarkus, bazel, quarkus, build, integration, starlark]
---

# rules-quarkus

> Keyword: rules-quarkus | Platforms: gemini,claude,codex

Expert AI Agent Skill for **rules_quarkus** - Native Bazel integration for Quarkus that reconciles Quarkus's dynamic build-time "Augmentation" phase with Bazel's hermetic, deterministic build system.

**Solves:** [Quarkus Issue #11305](https://github.com/quarkusio/quarkus/issues/11305) (open since early 2020)

## Repository

- **Source:** https://github.com/kinhluan/rules_quarkus
- **Maintainers:** @kinhluan, @tructxn, @Nhannguyenus24

## Requirements

| Component | Version |
|-----------|---------|
| Bazel | 7.x+ |
| Java | 21 |
| Quarkus | 3.20.1 |

---

## Agent Behavior Directives

> **These directives tell the AI agent HOW to act, not just WHAT to know.**

### 1. Source of Truth: Always Consult the Repository

When you encounter questions, errors, or scenarios NOT covered in this skill, **go directly to the source repository** before guessing:

- **Repository:** https://github.com/kinhluan/rules_quarkus
- **Key files to read:**

| File | What you'll learn |
|------|-------------------|
| `quarkus/quarkus.bzl` | Macro signatures: `quarkus_application`, `quarkus_library` - all attributes, defaults |
| `quarkus/quarkus_bootstrap.bzl` | Augmentation rule internals - how JARs are collected and augmentor runs |
| `quarkus/quarkus_runner.bzl` | Runner script generation - runfiles resolution, `QuarkusEntryPoint` launch |
| `examples/hello-world/BUILD.bazel` | Working BUILD.bazel with correct deps/extensions/main_class |
| `examples/demo-extensions/BUILD.bazel` | Multi-extension example (Tier 1-5) |
| `MODULE.bazel` | **Critical:** All tested artifacts + required `exclusions` for deployment deps |
| `.bazelrc` | Required Java 21 build flags |
| `README.md` | Latest quick start, version requirements |
| `CHANGELOG.md` | Breaking changes between versions |

**How to access:**
```bash
# Read specific files via raw GitHub URL
# WebFetch: https://raw.githubusercontent.com/kinhluan/rules_quarkus/main/quarkus/quarkus.bzl
# WebFetch: https://raw.githubusercontent.com/kinhluan/rules_quarkus/main/MODULE.bazel

# Or clone for full exploration
git clone https://github.com/kinhluan/rules_quarkus.git /tmp/rules_quarkus
```

**When to consult the repo:**
- Adding an extension not listed in this skill → check `MODULE.bazel` for exact artifact + exclusions
- Build error you can't diagnose → read `quarkus_bootstrap.bzl` to understand the pipeline
- New version of rules_quarkus → read `CHANGELOG.md` for breaking changes
- Unsure about macro parameters → read `quarkus/quarkus.bzl` for actual function signature

### 2. Troubleshooting Strategy: Read Source → Check Issues → File Issue

When a Bazel build fails with rules_quarkus, follow this escalation path:

```
Build failed?
│
├── Step 1: Fix with knowledge in this skill
│   Use the "Troubleshooting Workflows" section below.
│   Most errors (80%+) are: missing deployment extension, missing exclusions,
│   missing main_class, or wrong artifact name.
│
├── Step 2: Read rules_quarkus source to understand the gap
│   WebFetch the relevant .bzl file and read the implementation.
│   Key comparison points:
│   - quarkus_bootstrap.bzl: How are JARs collected? (app vs runtime vs deployment)
│   - quarkus_runner.bzl: How is the run script generated? (runfiles resolution)
│   - MODULE.bazel: What exclusions are needed for this extension?
│
├── Step 3: Search existing GitHub issues
│   Search: https://github.com/kinhluan/rules_quarkus/issues
│   Look for: similar error messages, extension names, Quarkus version conflicts.
│   │
│   ├── Found matching issue → Follow the workaround or note it's known.
│   └── No matching issue → Go to Step 4.
│
├── Step 4 (optional): Cross-reference with Maven to isolate the problem
│   Only do this if you need to PROVE the issue is in rules_quarkus (not user code):
│     mvn clean compile quarkus:build
│   Maven ALSO fails → fix Quarkus code first (use quarkus-expert skill).
│   Maven succeeds → confirmed rules_quarkus issue → Go to Step 5.
│
└── Step 5: Recommend filing an issue
    → See "When to File an Issue" section below.
```

### 3. When to File an Issue

**Issue URL:** https://github.com/kinhluan/rules_quarkus/issues/new

**Recommend filing when:**
- An extension works correctly with Maven/Gradle but fails with rules_quarkus
- The augmentation phase produces errors not related to user configuration
- A new Quarkus version breaks existing rules_quarkus builds
- ClassLoader or classpath issues specific to the Bazel integration
- Missing features (native image support, dev mode, multi-module)

**Do NOT recommend filing when:**
- User forgot a deployment extension or exclusions (common config mistake)
- Java compilation error (not a rules_quarkus issue)
- Missing `RULES_JVM_EXTERNAL_REPIN=1` after changing deps
- Wrong artifact name mapping

**Issue template to suggest:**

```markdown
## Description
[What you're trying to do]

## Environment
- rules_quarkus version: [e.g., 0.1.1]
- Bazel version: [e.g., 7.5.0]
- Quarkus version: [e.g., 3.20.1]
- OS: [e.g., macOS 15, Ubuntu 24.04]

## Steps to Reproduce
1. MODULE.bazel artifacts: [list]
2. BUILD.bazel: [paste]
3. Command: `bazel build //app`

## Expected Behavior
[What should happen]

## Actual Behavior
[Error output]

## Maven Comparison (if applicable)
[Does the same setup work with `mvn quarkus:build`? Paste working pom.xml if yes]
```

---

## Quick Start: New Project from Scratch

### Step 1: Project Structure

```
my-quarkus-app/
├── MODULE.bazel
├── BUILD.bazel              # Root (may be empty)
├── .bazelrc                 # Java 21 config (required)
├── maven_install.json       # Generated lock file
├── app/
│   ├── BUILD.bazel          # quarkus_application target
│   └── src/
│       ├── main/
│       │   ├── java/com/example/
│       │   │   └── GreetingResource.java
│       │   └── resources/
│       │       └── application.properties
│       └── test/
│           └── java/com/example/
│               └── GreetingResourceTest.java
└── lib/                     # Optional shared library
    ├── BUILD.bazel
    └── src/main/java/...
```

### Step 2: .bazelrc (Required)

```bash
# .bazelrc - Java 21 configuration (MUST have)
build --java_language_version=21
build --tool_java_language_version=21
build --java_runtime_version=remotejdk_21
build --tool_java_runtime_version=remotejdk_21

# Performance
build --experimental_reuse_sandbox_directories

# Debugging
build --verbose_failures
build --color=yes
build --show_timestamps
```

### Step 3: MODULE.bazel

```python
module(
    name = "my-quarkus-app",
    version = "1.0.0",
)

# Java toolchain
bazel_dep(name = "rules_java", version = "8.6.2")

# rules_quarkus
bazel_dep(name = "rules_quarkus", version = "0.1.1")
archive_override(
    module_name = "rules_quarkus",
    urls = ["https://github.com/kinhluan/rules_quarkus/archive/refs/tags/v0.1.1.tar.gz"],
    strip_prefix = "rules_quarkus-0.1.1",
)

# Maven dependencies
bazel_dep(name = "rules_jvm_external", version = "6.5")

maven = use_extension("@rules_jvm_external//:extensions.bzl", "maven")

QUARKUS_VERSION = "3.20.1"

# Runtime artifacts + core deployment (no exclusions needed for core/arc)
maven.install(
    name = "maven",
    artifacts = [
        # Quarkus Core (core-deployment does NOT pull Maven/Sisu transitives)
        "io.quarkus:quarkus-core:%s" % QUARKUS_VERSION,
        "io.quarkus:quarkus-core-deployment:%s" % QUARKUS_VERSION,

        # Quarkus ArC / CDI (arc-deployment does NOT pull Maven/Sisu transitives)
        "io.quarkus:quarkus-arc:%s" % QUARKUS_VERSION,
        "io.quarkus:quarkus-arc-deployment:%s" % QUARKUS_VERSION,

        # Quarkus Bootstrap (required for augmentation)
        "io.quarkus:quarkus-bootstrap-core:%s" % QUARKUS_VERSION,
        "io.quarkus:quarkus-bootstrap-app-model:%s" % QUARKUS_VERSION,
        "io.quarkus:quarkus-bootstrap-runner:%s" % QUARKUS_VERSION,
        "io.quarkus:quarkus-builder:%s" % QUARKUS_VERSION,

        # Quarkus REST (runtime only - deployment needs exclusions, see below)
        "io.quarkus:quarkus-rest:%s" % QUARKUS_VERSION,
        "io.quarkus:quarkus-vertx-http:%s" % QUARKUS_VERSION,

        # Gizmo (bytecode generation) + Jandex (indexing)
        "io.quarkus.gizmo:gizmo:1.8.0",
        "io.smallrye:jandex:3.2.3",

        # Vert.x
        "io.vertx:vertx-core:4.5.11",
        "io.vertx:vertx-web:4.5.11",

        # Jakarta APIs
        "jakarta.enterprise:jakarta.enterprise.cdi-api:4.1.0",
        "jakarta.inject:jakarta.inject-api:2.0.1",
        "jakarta.annotation:jakarta.annotation-api:3.0.0",
        "jakarta.ws.rs:jakarta.ws.rs-api:4.0.0",

        # Logging
        "org.jboss.logging:jboss-logging:3.6.1.Final",
        "org.jboss.logmanager:jboss-logmanager:3.0.6.Final",
    ],
    fetch_sources = True,
    generate_compat_repositories = True,
    repositories = [
        "https://repo1.maven.org/maven2",
    ],
)

# ============================================================
# Deployment extensions that pull Maven/Sisu transitives
# MUST use maven.artifact() with exclusions.
# Note: quarkus-core-deployment and quarkus-arc-deployment
# do NOT have these transitives, so they can stay in artifacts[].
# ============================================================
maven.artifact(
    artifact = "quarkus-rest-deployment",
    exclusions = [
        "org.eclipse.sisu:org.eclipse.sisu.plexus",
        "org.apache.maven:maven-plugin-api",
        "org.apache.maven:maven-xml-impl",
        "org.codehaus.plexus:plexus-xml",
    ],
    group = "io.quarkus",
    version = QUARKUS_VERSION,
)

maven.artifact(
    artifact = "quarkus-vertx-http-deployment",
    exclusions = [
        "org.eclipse.sisu:org.eclipse.sisu.plexus",
        "org.apache.maven:maven-plugin-api",
        "org.apache.maven:maven-xml-impl",
        "org.codehaus.plexus:plexus-xml",
    ],
    group = "io.quarkus",
    version = QUARKUS_VERSION,
)

use_repo(maven, "maven")
```

### Step 4: app/BUILD.bazel

```python
load("@rules_quarkus//quarkus:quarkus.bzl", "quarkus_application")

quarkus_application(
    name = "app",
    srcs = glob(["src/main/java/**/*.java"]),
    resources = glob(["src/main/resources/**/*"]),

    # API-only dependencies (compile against, not Quarkus extensions)
    deps = [
        "@maven//:io_quarkus_quarkus_core",
        "@maven//:jakarta_enterprise_jakarta_enterprise_cdi_api",
        "@maven//:jakarta_inject_jakarta_inject_api",
        "@maven//:jakarta_ws_rs_jakarta_ws_rs_api",
    ],

    # Quarkus runtime extensions
    runtime_extensions = [
        "@maven//:io_quarkus_quarkus_arc",
        "@maven//:io_quarkus_quarkus_rest",
        "@maven//:io_quarkus_quarkus_vertx_http",
    ],

    # Quarkus deployment modules (for augmentation)
    deployment_extensions = [
        "@maven//:io_quarkus_quarkus_arc_deployment",
        "@maven//:io_quarkus_quarkus_rest_deployment",
        "@maven//:io_quarkus_quarkus_vertx_http_deployment",
    ],

    # REQUIRED: Main class for Quarkus apps
    main_class = "io.quarkus.runner.GeneratedMain",

    # JVM flags
    jvm_flags = [
        "-Xmx512m",
        "-Djava.util.logging.manager=org.jboss.logmanager.LogManager",
    ],

    visibility = ["//visibility:public"],
)
```

### Step 5: lib/BUILD.bazel (shared library)

```python
load("@rules_quarkus//quarkus:quarkus.bzl", "quarkus_library")

quarkus_library(
    name = "common",
    srcs = glob(["src/main/java/**/*.java"]),
    deps = [
        "@maven//:io_quarkus_quarkus_arc",
        "@maven//:jakarta_inject_jakarta_inject_api",
    ],
    visibility = ["//visibility:public"],
)
```

### Step 6: Build and Run

```bash
# Build the application
bazel build //app

# Run the application (two methods)
bazel run //app                     # Method 1: via bazel run
./bazel-bin/app/app                 # Method 2: run the generated script directly

# Verify it works
curl http://localhost:8080/hello
```

---

## Operational Commands

### Build

```bash
# Build single target
bazel build //app

# Build everything
bazel build //...

# Build with verbose output (for debugging augmentation)
bazel build //app --sandbox_debug --verbose_failures

# Suppress noisy output
bazel build //app --ui_event_filters=-warning,-info,-debug
```

### Run

```bash
# Run the Quarkus application (starts HTTP server)
bazel run //app

# Run with Quarkus config override
bazel run //app -- -Dquarkus.http.port=9090
bazel run //app -- -Dquarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/mydb

# Run with environment variables
bazel run //app --action_env=QUARKUS_PROFILE=staging

# Direct execution (after build)
./bazel-bin/app/app
```

### Test

```bash
# Run all tests
bazel test //...

# Run tests for a specific module
bazel test //app:all

# Run a single test class
bazel test //app:app-test --test_filter=com.example.GreetingResourceTest

# Run tests with output on failure
bazel test //app:all --test_output=errors

# Run tests with full output (for debugging)
bazel test //app:all --test_output=all
```

### Dependency Management

```bash
# Re-pin after adding/changing artifacts in MODULE.bazel
RULES_JVM_EXTERNAL_REPIN=1 bazelisk run @maven//:pin

# Query: what depends on a target?
bazel query "rdeps(//..., //lib:common)"

# Query: what does a target depend on?
bazel query "deps(//app)" --output=graph

# Check available Maven artifact target names
bazel query @maven//:all | grep quarkus
```

---

## Common Workflows

### Adding a New Quarkus Extension

Every Quarkus extension has **two** Maven artifacts: runtime + deployment. Most deployment artifacts need **exclusions** (see "Deployment Exclusions" section for which ones).

```
User says: "Add Hibernate ORM with Panache"

Step 1: Add runtime artifact to MODULE.bazel maven.install() artifacts list:
  "io.quarkus:quarkus-hibernate-orm-panache:%s" % QUARKUS_VERSION,
  "io.quarkus:quarkus-jdbc-postgresql:%s" % QUARKUS_VERSION,

Step 2: Add deployment artifact WITH exclusions:
  maven.artifact(
      artifact = "quarkus-hibernate-orm-panache-deployment",
      exclusions = [
          "org.eclipse.sisu:org.eclipse.sisu.plexus",
          "org.apache.maven:maven-plugin-api",
          "org.apache.maven:maven-xml-impl",
          "org.codehaus.plexus:plexus-xml",
      ],
      group = "io.quarkus",
      version = QUARKUS_VERSION,
  )
  maven.artifact(
      artifact = "quarkus-jdbc-postgresql-deployment",
      exclusions = [
          "org.eclipse.sisu:org.eclipse.sisu.plexus",
          "org.apache.maven:maven-plugin-api",
          "org.apache.maven:maven-xml-impl",
          "org.codehaus.plexus:plexus-xml",
      ],
      group = "io.quarkus",
      version = QUARKUS_VERSION,
  )

Step 3: Re-pin
  RULES_JVM_EXTERNAL_REPIN=1 bazelisk run @maven//:pin

Step 4: Add to app/BUILD.bazel:
  runtime_extensions = [
      ...existing...,
      "@maven//:io_quarkus_quarkus_hibernate_orm_panache",
      "@maven//:io_quarkus_quarkus_jdbc_postgresql",
  ],
  deployment_extensions = [
      ...existing...,
      "@maven//:io_quarkus_quarkus_hibernate_orm_panache_deployment",
      "@maven//:io_quarkus_quarkus_jdbc_postgresql_deployment",
  ],

Step 5: Rebuild
  bazel build //app
```

### Critical: Deployment Exclusions

**Why are exclusions needed?** Some Quarkus deployment JARs transitively pull in Maven/Sisu internals (because Quarkus's build tooling was designed for Maven). These create circular dependency errors in Bazel. The standard exclusion set is:

```python
DEPLOYMENT_EXCLUSIONS = [
    "org.eclipse.sisu:org.eclipse.sisu.plexus",
    "org.apache.maven:maven-plugin-api",
    "org.apache.maven:maven-xml-impl",
    "org.codehaus.plexus:plexus-xml",
]
```

**Which deployment artifacts need exclusions?**

| Artifact | Needs exclusions? | Why |
|----------|-------------------|-----|
| `quarkus-core-deployment` | No | Core module, no Maven/Sisu transitives |
| `quarkus-arc-deployment` | No | CDI processor, no Maven/Sisu transitives |
| `quarkus-rest-deployment` | **Yes** | Pulls org.eclipse.sisu via build tooling |
| `quarkus-vertx-http-deployment` | **Yes** | Pulls org.eclipse.sisu via build tooling |
| Most other `*-deployment` | **Yes** | Assume yes unless verified in repo MODULE.bazel |

**Rule of thumb:** If unsure, use `maven.artifact()` with exclusions. If it works without, you can simplify later. When in doubt, **read the repo MODULE.bazel** for the exact tested configuration.

### Understanding `deps` vs `runtime_extensions` vs `deployment_extensions`

```python
quarkus_application(
    # deps: API-only JARs you compile against. NOT Quarkus extensions.
    # These are standard Java libraries and Jakarta APIs.
    deps = [
        "@maven//:jakarta_ws_rs_jakarta_ws_rs_api",     # JAX-RS annotations
        "@maven//:jakarta_inject_jakarta_inject_api",     # @Inject
        "@maven//:jakarta_enterprise_jakarta_enterprise_cdi_api",  # CDI
        "@maven//:io_quarkus_quarkus_core",               # Quarkus core APIs
        "//lib:common",                                    # Your own libraries
    ],

    # runtime_extensions: Quarkus extension JARs that run in production.
    # These provide the actual implementation (CDI container, HTTP server, etc.)
    runtime_extensions = [
        "@maven//:io_quarkus_quarkus_arc",          # CDI implementation
        "@maven//:io_quarkus_quarkus_rest",          # REST implementation
        "@maven//:io_quarkus_quarkus_vertx_http",    # HTTP server
    ],

    # deployment_extensions: Quarkus extension JARs that run at BUILD TIME only.
    # These generate optimized code during augmentation. NOT in final app.
    deployment_extensions = [
        "@maven//:io_quarkus_quarkus_arc_deployment",
        "@maven//:io_quarkus_quarkus_rest_deployment",
        "@maven//:io_quarkus_quarkus_vertx_http_deployment",
    ],
)
```

### Extension Name Mapping (Maven → Bazel target)

**Rule:** Replace `:` with `_`, replace `-` with `_`, prefix with `@maven//:`.

| Maven artifact | Bazel target |
|---------------|--------------|
| `io.quarkus:quarkus-arc` | `@maven//:io_quarkus_quarkus_arc` |
| `io.quarkus:quarkus-rest` | `@maven//:io_quarkus_quarkus_rest` |
| `io.quarkus:quarkus-rest-jackson` | `@maven//:io_quarkus_quarkus_rest_jackson` |
| `io.quarkus:quarkus-hibernate-orm-panache` | `@maven//:io_quarkus_quarkus_hibernate_orm_panache` |
| `io.quarkus:quarkus-reactive-pg-client` | `@maven//:io_quarkus_quarkus_reactive_pg_client` |
| `jakarta.ws.rs:jakarta.ws.rs-api` | `@maven//:jakarta_ws_rs_jakarta_ws_rs_api` |

### Iterative Development Workflow

```bash
# Quarkus dev mode is NOT available with Bazel (requires Maven/Gradle plugin).
# Instead, use Bazel's fast incremental builds:

# Terminal 1: Build and run
bazel run //app

# Terminal 2: After code changes, rebuild (Bazel caches unchanged targets)
bazel build //app && bazel run //app

# ibazel (watch mode) - auto-rebuilds on file changes:
# Install: go install github.com/bazelbuild/bazel-watcher/cmd/ibazel@latest
ibazel run //app
```

---

## Architectural Mandates

### Three-Layer Transformation Pipeline

| Layer | Rule | Purpose |
|-------|------|---------|
| **1. Compilation** | `java_library` | Compile source to bytecode, maximize caching efficiency |
| **2. Augmentation** | `quarkus_bootstrap` | Aggregate dependency graph, construct `ApplicationModel`, execute `AugmentAction` in sandbox |
| **3. Orchestration** | `quarkus_runner` | Generate shell script that resolves Bazel runfiles, launches via `QuarkusEntryPoint` |

### How `quarkus_bootstrap` Works (Internal)

The augmentation rule:
1. Collects JARs from 3 sources via `JavaInfo` providers:
   - **Application JARs** (user code from `srcs`)
   - **Runtime JARs** (from `runtime_extensions` transitive deps)
   - **Deployment JARs** (from `deployment_extensions` transitive deps)
2. Passes JAR lists to the **augmentor tool** via parameter file (avoids "argument list too long")
3. Produces an **augmented app directory** containing the processed `quarkus-app/` structure

### How `quarkus_runner` Works (Internal)

The runner rule:
1. Takes the augmented app directory from `quarkus_bootstrap`
2. Generates a **shell script** that:
   - Resolves Bazel runfiles (handles `RUNFILES_DIR`, `.runfiles/`, execroot fallbacks)
   - Launches Java via `io.quarkus.bootstrap.runner.QuarkusEntryPoint`
   - Passes user-defined `jvm_flags`

### Why Two Artifact Types (Runtime + Deployment)?

Quarkus splits extensions into two JARs:
- **Runtime** (`quarkus-rest`): Code that runs in production. Included in final app.
- **Deployment** (`quarkus-rest-deployment`): Code that runs at **build time** during augmentation. NOT in final app.

In Maven/Gradle, the Quarkus plugin handles this split automatically. In Bazel, you must **declare both explicitly** because Bazel needs all inputs declared upfront (hermeticity).

### Core Macros

#### `quarkus_application`

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `name` | Yes | - | Target name |
| `srcs` | No | `[]` | Java source files |
| `resources` | No | `[]` | Config files (application.properties, etc.) |
| `deps` | No | `[]` | API-only dependencies (Jakarta APIs, your libraries) |
| `runtime_extensions` | No | `[]` | Quarkus runtime extension JARs |
| `deployment_extensions` | No | `[]` | Quarkus deployment JARs (build-time only) |
| `main_class` | **Yes** | - | Must be `"io.quarkus.runner.GeneratedMain"` for standard apps |
| `jvm_flags` | No | `[]` | JVM arguments for runtime |
| `visibility` | No | - | Bazel visibility |

#### `quarkus_library`

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `name` | Yes | - | Library name |
| `srcs` | No | `[]` | Java source files |
| `resources` | No | `[]` | Resource files |
| `deps` | No | `[]` | Dependencies |
| `extensions` | No | `[]` | Quarkus extensions used |
| `visibility` | No | - | Bazel visibility |

Wraps `java_library` with `-parameters` compiler flag for Quarkus compatibility.

## Extension Strategy (5-Tier Model)

| Tier | Category | Runtime artifact | Deployment artifact |
|------|----------|-----------------|-------------------|
| Tier 1 (Core) | CDI, REST, HTTP | `quarkus-arc`, `quarkus-rest`, `quarkus-vertx-http` | `quarkus-arc-deployment`, `quarkus-rest-deployment`, `quarkus-vertx-http-deployment` |
| Tier 2 (Data) | Reactive DB | `quarkus-reactive-oracle-client`, `quarkus-reactive-mysql-client`, `quarkus-redis-client` | Append `-deployment` |
| Tier 3 (Messaging) | Async | `quarkus-messaging-kafka`, `quarkus-messaging-rabbitmq`, `quarkus-grpc` | Append `-deployment` |
| Tier 4 (Observability) | Monitoring | `quarkus-micrometer-registry-prometheus`, `quarkus-smallrye-health` | Append `-deployment` |
| Tier 5 (Quarkiverse) | Community | `quarkus-unleash`, `quarkus-langchain4j-openai`, `quarkus-tika` | Append `-deployment` (note: different groupId for Quarkiverse) |

**Quarkiverse groupIds differ:**
- `io.quarkiverse.unleash:quarkus-unleash:1.10.0` (not `io.quarkus`)
- `io.quarkiverse.langchain4j:quarkus-langchain4j-openai:0.26.1`
- `io.quarkiverse.tika:quarkus-tika:2.1.0`

---

## Troubleshooting Workflows

### Decision Tree: Build Failure

```
Build failed?
│
├── "Unable to locate CDIProvider" or ClassNotFoundException
│   → Missing deployment extension. Check every runtime_extension has matching deployment_extension.
│   → Did you add exclusions for the deployment artifact? (See "Deployment Exclusions")
│   → Read quarkus_bootstrap.bzl to verify ClassLoader setup.
│
├── "Argument list too long" (especially in CI)
│   → Already handled internally via param files in quarkus_bootstrap.bzl.
│   → If still occurring: read the latest quarkus_bootstrap.bzl from repo for fixes.
│
├── "Type not found in index" (Jandex)
│   → Extension's beans not indexed. Ensure all source JARs are in augmentation classpath.
│   → Read quarkus_bootstrap.bzl to check how JARs are collected.
│
├── "dependency not found" for @maven//:io_quarkus_...
│   → Re-pin: RULES_JVM_EXTERNAL_REPIN=1 bazelisk run @maven//:pin
│   → Verify artifact name: replace : and - with _ (see mapping table)
│   → Check: bazel query @maven//:all | grep quarkus
│
├── "Circular dependency" or "conflict" in deployment deps
│   → Deployment artifact missing exclusions. Use maven.artifact() with DEPLOYMENT_EXCLUSIONS.
│   → Read MODULE.bazel from repo to see exact exclusions for your extension.
│
├── "no matching toolchains" for Java
│   → Ensure .bazelrc has Java 21 config (see Step 2 in Quick Start).
│
├── Build succeeds but app fails at startup
│   → Missing runtime extension (has deployment but not runtime).
│   → Check application.properties is in resources glob pattern.
│   → Verify main_class = "io.quarkus.runner.GeneratedMain"
│   → Run: bazel run //app -- and check Quarkus startup banner for loaded extensions.
│
└── Error not listed above
    → Read the relevant .bzl source file from repo.
    → Search GitHub issues: https://github.com/kinhluan/rules_quarkus/issues
    → If confirmed rules_quarkus bug → recommend filing issue with template above.
```

### Runtime Errors

```
App starts but endpoint returns 404?
  → Check @Path annotation matches URL.
  → Verify quarkus-rest (not quarkus-resteasy) is in runtime_extensions.

App starts but CDI injection is null?
  → Bean class must be in srcs glob of quarkus_application.
  → Or bean must be in a quarkus_library listed in deps.
  → beans.xml is NOT needed (Quarkus uses Jandex, not beans.xml).

App starts but DB connection fails?
  → application.properties must be in resources glob.
  → Verify JDBC driver extension in runtime_extensions.
```

## Key APIs & Components

- **`QuarkusBootstrap` API** - Official API for native integration
- **`ApplicationModel`** - Deterministic metadata representation
- **`AugmentAction`** - Executes bytecode transformation in sandbox
- **`QuarkusEntryPoint`** - App entry point used by quarkus_runner (`io.quarkus.bootstrap.runner.QuarkusEntryPoint`)
- **`quarkus_bootstrap`** - Custom Bazel rule for augmentation
- **`quarkus_runner`** - Generates executable shell script with runfiles resolution

## Expert Tips

- **`main_class` is required** - always set to `"io.quarkus.runner.GeneratedMain"` for standard apps
- **Every deployment artifact needs exclusions** - use the standard `DEPLOYMENT_EXCLUSIONS` set
- Every `runtime_extension` must have a matching `deployment_extension` - forgetting one is the #1 error
- Never rely on system environment variables during augmentation
- Use `ibazel run //app` for watch-mode development (auto-rebuild on file change)
- Use `bazel query "deps(//app)"` to debug the full dependency graph
- When in doubt, **read the MODULE.bazel from the repo** - it has all tested artifact combinations

## 🌐 Knowledge Sources & Deep Dives

> **Directive:** When encountering unlisted extensions or complex build errors, use `web_fetch` on the relevant GitHub file or search the Issue tracker before guessing.

### Core Repository (Source of Truth)
- **Macro Signatures:** [quarkus/quarkus.bzl](https://raw.githubusercontent.com/kinhluan/rules_quarkus/main/quarkus/quarkus.bzl) - Check attributes and defaults.
- **Augmentation Pipeline:** [quarkus/quarkus_bootstrap.bzl](https://raw.githubusercontent.com/kinhluan/rules_quarkus/main/quarkus/quarkus_bootstrap.bzl) - How JARs are collected and augmented.
- **Dependency Map:** [MODULE.bazel](https://raw.githubusercontent.com/kinhluan/rules_quarkus/main/MODULE.bazel) - See tested artifacts and required `exclusions`.

### Troubleshooting & Community
- **GitHub Issues:** [kinhluan/rules_quarkus/issues](https://github.com/kinhluan/rules_quarkus/issues) - Search for "extension-name" or "error-message".
- **Changelog:** [CHANGELOG.md](https://github.com/kinhluan/rules_quarkus/blob/main/CHANGELOG.md) - Track breaking changes between versions.
- **Reference Issue:** [Quarkus Issue #11305](https://github.com/quarkusio/quarkus/issues/11305) - Context on Bazel + Quarkus challenges.

## References

- [rules_quarkus Documentation](https://github.com/kinhluan/rules_quarkus#readme)
- [Bazel Support for Quarkus Blog](https://github.com/kinhluan/rules_quarkus/blob/main/docs/blogs/2026-03-11-bazel-support-for-quarkus.md)
- [Quarkus Official Guides](https://quarkus.io/guides/)
- [Bazel Build System](https://bazel.build/)

## Skill Interoperability

The **rules-quarkus** 🔧 skill integrates all other skills to provide a complete Quarkus development experience on Bazel:
- **java-expert** ☕, **vertx-expert** 🌀, **graalvm-expert** 🚀: For framework and runtime support.
- **maven-expert** 📦, **gradle-expert** 🐘: For migrating existing projects.
- **bazel-expert** 🏗: For core build system infrastructure.
- **quarkus-expert** ⚡: For specialized framework knowledge.
