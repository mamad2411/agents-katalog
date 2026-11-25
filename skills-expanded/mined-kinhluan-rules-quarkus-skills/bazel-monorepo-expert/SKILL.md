---
name: bazel-monorepo-expert
description: Expert knowledge for managing large-scale Bazel monorepos with multiple services, shared libraries, and cross-cutting concerns. Use for workspace structure, visibility, and dependency management.
version: 1.0.0
keywords: [bazel, monorepo, workspace, multi-service, visibility, dependency-graph, rules]
---

# bazel-monorepo-expert

> Keyword: monorepo | Platforms: gemini,claude,codex

Bazel Monorepo Expert Skill - Structuring, managing, and optimizing large-scale Bazel workspaces with multiple services, shared libraries, and complex dependency graphs.

## Core Mandates

- **Single Source of Truth:** One workspace for all services and shared libraries.
- **Strict Visibility:** Default private, explicitly expose only public APIs.
- **Dependency Hygiene:** No circular dependencies, no diamond dependency conflicts.
- **Consistent Tooling:** Same Java version, same linter, same test framework across all packages.
- **Incremental Builds:** Granular targets for fast incremental builds and cache hits.

---

## Workspace Structure

### Recommended Layout

```
my-monorepo/
├── WORKSPACE.bazel (or MODULE.bazel)
├── .bazelrc
├── .bazelignore
├── .bazelversion
├── BUILD.bazel (root)
├── platforms/
│   └── BUILD.bazel
├── toolchains/
│   └── BUILD.bazel
├── third_party/
│   └── BUILD.bazel
├── common/
│   ├── utils/
│   │   ├── src/main/java/...
│   │   ├── src/test/java/...
│   │   └── BUILD.bazel
│   ├── models/
│   │   └── BUILD.bazel
│   └── proto/
│       └── BUILD.bazel
├── services/
│   ├── user/
│   │   ├── src/main/java/...
│   │   ├── src/test/java/...
│   │   ├── src/main/resources/
│   │   ├── k8s/
│   │   ├── helm/
│   │   └── BUILD.bazel
│   ├── order/
│   │   └── BUILD.bazel
│   └── payment/
│       └── BUILD.bazel
├── libs/
│   ├── auth/
│   │   └── BUILD.bazel
│   ├── messaging/
│   │   └── BUILD.bazel
│   └── observability/
│       └── BUILD.bazel
└── tools/
    ├── buildifier/
    ├── linters/
    └── scripts/
```

### Root BUILD.bazel

```python
# BUILD.bazel (root)
exports_files([".bazelrc", "MODULE.bazel"])

# Test suite for all tests in the repo
test_suite(
    name = "all_tests",
    tests = [
        "//common/utils:all_tests",
        "//common/models:all_tests",
        "//services/user:all_tests",
        "//services/order:all_tests",
        "//services/payment:all_tests",
        "//libs/auth:all_tests",
        "//libs/messaging:all_tests",
    ],
)

# Build all services
filegroup(
    name = "all_services",
    srcs = [
        "//services/user:user-service_image",
        "//services/order:order-service_image",
        "//services/payment:payment-service_image",
    ],
)
```

---

## Visibility Boundaries

### Package-Level Visibility

```python
# common/utils/BUILD.bazel
java_library(
    name = "utils",
    srcs = glob(["src/main/java/**/*.java"]),
    visibility = [
        "//services/...",  # All services
        "//libs/...",      # All libraries
        "//common/...",    # Other common packages
    ],
)

# Internal-only utility
java_library(
    name = "internal-utils",
    srcs = ["src/main/java/com/example/utils/InternalHelper.java"],
    visibility = ["//visibility:private"],  # Only this package
)
```

### API vs Implementation

```python
# libs/auth/BUILD.bazel
# Public API
java_library(
    name = "auth-api",
    srcs = ["src/main/java/com/example/auth/api/*.java"],
    visibility = ["//visibility:public"],
    deps = ["@maven//:jakarta_inject"],
)

# Implementation (not exposed)
java_library(
    name = "auth-impl",
    srcs = glob(["src/main/java/com/example/auth/impl/*.java"]),
    visibility = ["//libs/auth:__subpackages__"],  # Only within auth
    deps = [
        ":auth-api",
        "@maven//:io_quarkus_quarkus_security",
    ],
)

# Public facade
java_library(
    name = "auth",
    srcs = ["src/main/java/com/example/auth/AuthFacade.java"],
    visibility = ["//visibility:public"],
    exports = [":auth-api"],  # Consumers see auth-api types
    runtime_deps = [":auth-impl"],
)
```

### Visibility Package Groups

```python
# BUILD.bazel (root or common/)
package_group(
    name = "services",
    packages = ["//services/..."],
)

package_group(
    name = "libraries",
    packages = ["//libs/..."],
)

package_group(
    name = "internal",
    packages = [
        "//common/...",
        "//libs/...",
    ],
)
```

```python
# common/utils/BUILD.bazel
java_library(
    name = "utils",
    srcs = glob(["src/main/java/**/*.java"]),
    visibility = ["//:internal"],  # Use package group
)
```

---

## Dependency Management

### Dependency Graph Analysis

```bash
# Visualize dependency graph
bazel query "deps(//services/user:user-service)" --output=graph > graph.dot
dot -Tpng graph.dot -o graph.png

# Find unused dependencies
bazel query "deps(//services/user:lib) except deps(//services/user:lib, 1)"

# Find reverse dependencies
bazel query "rdeps(//..., //common/utils:utils)"

# Check for circular dependencies
bazel query "somepath(//services/user:lib, //services/order:lib)"
bazel query "somepath(//services/order:lib, //services/user:lib)"
# If both return results → circular dependency!

# Find diamond dependencies (same dep via different paths)
bazel query "allpaths(//services/user:lib, @maven//:com_google_guava_guava)"
```

### Dependency Hygiene Rules

```python
# tools/dependency_check.bzl
def _dependency_check_impl(ctx):
    # Check for banned dependencies
    banned = ["@maven//:commons_logging", "@maven//:log4j"]
    for dep in ctx.attr.deps:
        if str(dep.label) in banned:
            fail("Banned dependency: " + str(dep.label))

dependency_check = rule(
    implementation = _dependency_check_impl,
    attrs = {"deps": attr.label_list()},
)
```

### Version Pinning

```python
# MODULE.bazel
bazel_dep(name = "rules_jvm_external", version = "6.6")

maven = use_extension("@rules_jvm_external//:extensions.bzl", "maven")
maven.install(
    name = "maven",
    artifacts = [
        "io.quarkus:quarkus-arc:3.20.1",
        "io.quarkus:quarkus-rest:3.20.1",
        "com.google.guava:guava:33.4.0-jre",
    ],
    lock_file = "//:maven_install.json",  # Pin all versions
)
use_repo(maven, "maven")
```

---

## Cross-Cutting Concerns

### Shared Build Macros

```python
# tools/build_defs.bzl
def quarkus_service(name, srcs, deps, main_class = None, **kwargs):
    """Macro for standard Quarkus service setup."""
    java_library(
        name = name + "-lib",
        srcs = srcs,
        deps = deps + [
            "@maven//:io_quarkus_quarkus_core",
            "@maven//:jakarta_inject",
        ],
        visibility = ["//services/..."],
        **kwargs
    )

    java_binary(
        name = name,
        main_class = main_class or "io.quarkus.runner.GeneratedMain",
        runtime_deps = [":" + name + "-lib"],
        visibility = ["//visibility:public"],
    )

    java_test(
        name = name + "-test",
        srcs = native.glob(["src/test/java/**/*.java"]),
        test_class = "com.example." + name.replace("-", ".") + ".TestSuite",
        deps = [
            ":" + name + "-lib",
            "@maven//:io_quarkus_quarkus_junit5",
        ],
    )
```

### Using the Macro

```python
# services/user/BUILD.bazel
load("//tools:build_defs.bzl", "quarkus_service")

quarkus_service(
    name = "user-service",
    srcs = glob(["src/main/java/**/*.java"]),
    deps = [
        "//common/utils:utils",
        "//common/models:models",
        "//libs/auth:auth",
        "@maven//:io_quarkus_quarkus_hibernate_orm_panache",
    ],
)
```

### Shared Linting

```python
# tools/lint.bzl
def java_lint(name, srcs):
    native.genrule(
        name = name + "_lint",
        srcs = srcs,
        outs = [name + "_lint_report.txt"],
        cmd = "java -jar $(location //tools:spotbugs) $(SRCS) > $@",
        tools = ["//tools:spotbugs"],
    )

# In BUILD files
load("//tools:lint.bzl", "java_lint")

java_lint(
    name = "user-service",
    srcs = glob(["src/main/java/**/*.java"]),
)
```

---

## CI/CD Integration

### GitHub Actions for Monorepo

```yaml
# .github/workflows/ci.yml
name: Monorepo CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      services: ${{ steps.changes.outputs.services }}
      common: ${{ steps.changes.outputs.common }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: changes
        with:
          filters: |
            services:
              - 'services/**'
            common:
              - 'common/**'
              - 'libs/**'

  build-affected:
    needs: detect-changes
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: bazelbuild/setup-bazelisk@v3

      - name: Mount Bazel Cache
        uses: actions/cache@v4
        with:
          path: |
            ~/.cache/bazel
            ~/.cache/bazel-disk-cache
          key: bazel-${{ runner.os }}-${{ hashFiles('**/MODULE.bazel') }}

      - name: Build Affected Targets
        run: |
          if [ "${{ needs.detect-changes.outputs.common }}" == "true" ]; then
            bazel build //...
          else
            bazel build $(bazel query "rdeps(//..., set(${{ steps.changes.outputs.changed_files }}))")
          fi

      - name: Test Affected Targets
        run: bazel test //...
```

### Bazel CI Best Practices

```bash
# .bazelrc - CI-specific settings
build:ci --disk_cache=~/.cache/bazel-disk-cache
build:ci --repository_cache=~/.cache/bazel-repo-cache
build:ci --remote_cache=grpc://cache.internal:9092
build:ci --jobs=4
build:ci --local_cpu_resources=4
build:ci --local_ram_resources=HOST_RAM*0.8

# Test settings
test:ci --test_output=errors
test:ci --test_summary=detailed
test:ci --flaky_test_attempts=3
```

---

## Performance Optimization

### Target Granularity

```python
# BAD - monolithic target
java_library(
    name = "user-service",
    srcs = glob(["src/main/java/**/*.java"]),  # 100+ files
)

# GOOD - granular targets
java_library(
    name = "user-api",
    srcs = glob(["src/main/java/com/example/user/api/*.java"]),
    visibility = ["//services/..."],
)

java_library(
    name = "user-service",
    srcs = glob(["src/main/java/com/example/user/service/*.java"]),
    deps = [":user-api"],
)

java_library(
    name = "user-repository",
    srcs = glob(["src/main/java/com/example/user/repository/*.java"]),
    deps = [":user-api"],
)
```

### Build Graph Analysis

```bash
# Find critical path (longest build chain)
bazel analyze-profile profile.json | grep "Critical path"

# Generate build profile
bazel build //... --profile=profile.json
bazel analyze-profile profile.json

# Check cache hit rate
bazel build //... --execution_log_json_file=log.json
cat log.json | jq '. | select(.cacheHit == true)' | wc -l
cat log.json | jq '. | select(.cacheHit == false)' | wc -l
```

---

## Troubleshooting

### "Too many open files"

```bash
# Increase file descriptor limit
ulimit -n 4096

# Or in .bazelrc
startup --host_jvm_args=-XX:-MaxFDLimit
```

### Slow analysis phase

```bash
# Reduce glob scope
# BAD: glob(["src/**/*.java"])
# GOOD: glob(["src/main/java/**/*.java"])

# Use --nolegacy_external_runfiles
build --nolegacy_external_runfiles

# Disable strict Java deps for faster analysis
build --java_runtime_version=remotejdk_21
```

### Memory issues

```bash
# Increase Bazel server memory
startup --host_jvm_args=-Xmx8g

# Reduce parallelism
build --local_ram_resources=HOST_RAM*0.5
```

---

## Decision Trees

### Adding a New Service

```
New service needed?
  ├── Does it share domain logic?
  │     ├── YES → Create in //services/
  │     └── NO → Could it be a library?
  │           ├── YES → Create in //libs/
  │           └── NO → Create in //services/
  ├── Does it need its own DB?
  │     ├── YES → Add to service k8s manifests
  │     └── NO → Use shared DB or in-memory
  └── Does it need its own image?
        ├── YES → Add oci_image target
        └── NO → Use as library dependency
```

### Extracting a Library

```
Code duplicated across 3+ services?
  ├── YES → Extract to //libs/<name>
  ├── Is it domain-specific?
  │     ├── YES → //libs/<domain>/
  │     └── NO → //common/<category>/
  └── Does it have external deps?
        ├── YES → Document in MODULE.bazel
        └── NO → Keep minimal
```

---

## References

- [Bazel Monorepo Best Practices](https://bazel.build/basics/monorepos)
- [Bazel Visibility](https://bazel.build/concepts/visibility)
- [Bazel Query Guide](https://bazel.build/query/guide)
- [Bazel Performance](https://bazel.build/advanced/performance)
- [Monorepo Tools](https://monorepo.tools/)

## Skill Interoperability

The **bazel-monorepo-expert** 📦 skill manages workspaces using:
- **bazel-expert** 🏗: Core Bazel build system.
- **bazel-oci-expert** 🐳: Container images for services.
- **bazel-k8s-expert** ☸️: Kubernetes deployment for services.
- **rules-quarkus** 🔧: Quarkus service builds.
- **java-expert** ☕: Java code organization.
