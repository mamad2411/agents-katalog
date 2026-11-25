---
name: bazel-java-rules
description: >
  Bazel rules for owned Java codebases: java_library, java_binary, java_test,
  java_plugin, dependency visibility, toolchain/JDK selection, and hermetic builds.
  Use when structuring BUILD.bazel for Java monorepos or fixing classpath/visibility
  errors — not for arbitrary remote code execution on shared CI without authz.
---

# Bazel Java Rules

## Scope And Authorization

- **In scope:** Repositories and Bazel clusters you own or are authorized to build.
- **Out of scope:** Abusing remote executors/caches you do not control; leaking proprietary jars.
- Prefer hermetic, reproducible builds; pin toolchains.
- Pair remote cache auth with `bazel-remote-cache-auth`; use `code-quality-standards` for Java code.

## When To Use

- Creating or refactoring `java_library` / `java_binary` / `java_test` targets.
- Fixing `Target X is not visible from target Y` or classpath missing symbols.
- Migrating Maven/Gradle modules into Bazel Java rules.
- Selecting JDK toolchain versions per target.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Remote cache authentication | `bazel-remote-cache-auth` |
| Java style/Javadoc | `java-style-and-javadoc` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Rule | Purpose |
| --- | --- |
| `java_library` | Compile jars for dependents |
| `java_binary` | Runnable fat/deploy jar entrypoint |
| `java_test` | JUnit tests |
| `java_plugin` / annotation processors | Lombok, Dagger, etc. |
| `visibility` | Who may depend on the target |
| Tooling | Bazelisk, `rules_java`, JDK toolchains, `bazel query` |

## Workflow

### 1. Confirm scope and success criteria

1. Repo path, Bazel version (via `.bazelversion`), Java version, authorization.
2. Success: `bazel build //...` and `bazel test //module:tests` hermetically pass.
3. Define package visibility policy (private by default).

### 2. Inventory Java packages and BUILD files

```bash
bazel version
bazel query //... --output=label | head
rg -n "java_library|java_binary|java_test" --glob 'BUILD*'
find . -name '*.java' | head
```

1. Map source roots (`src/main/java`, `src/test/java`).
2. List external deps (`MODULE.bazel` / `WORKSPACE` / `maven.install`).
3. Note annotation processors in use.

### 3. Baseline build

```bash
bazel build //path/to/module:module
bazel test //path/to/module:module_test
```

1. Capture failures: visibility, missing deps, toolchain.
2. Record non-hermetic flags in `.bazelrc` that need cleanup.

### 4. Author Java rules

```python
# BUILD.bazel
load("@rules_java//java:defs.bzl", "java_library", "java_binary", "java_test")

java_library(
    name = "lib",
    srcs = glob(["src/main/java/**/*.java"]),
    resources = glob(["src/main/resources/**"]),
    deps = [
        "@maven//:com_google_guava_guava",
        "//other/module:lib",
    ],
    visibility = ["//visibility:private"],
)

java_binary(
    name = "app",
    main_class = "com.example.App",
    runtime_deps = [":lib"],
    visibility = ["//visibility:public"],
)

java_test(
    name = "lib_test",
    srcs = glob(["src/test/java/**/*Test.java"]),
    test_class = "com.example.LibTest",
    deps = [
        ":lib",
        "@maven//:junit_junit",
    ],
)
```

1. Prefer fine-grained libraries over one mega-target for cache friendliness.
2. Use `exports` sparingly; explicit deps improve correctness.
3. Annotation processors: `plugins = [":lombok_plugin"]` or `java_plugin` rules per `rules_java` docs.
4. Toolchains: register JDK 17/21 in MODULE/WORKSPACE; avoid relying on ambient `JAVA_HOME` alone.
5. Resources and `classpath_resources` configured for Spring-like apps carefully.

### 5. Verify with evidence

```bash
bazel build //path/to/module:app
bazel test //path/to/module:lib_test --test_output=errors
bazel query 'deps(//path/to/module:app)' --output=graph > /tmp/deps.dot
```

1. Change one source file; confirm incremental rebuild scope reasonable.
2. Visibility: depending from disallowed package fails as designed.
3. CI uses same Bazelisk version as developers.

### 6. Observe and harden

1. Remote build/cache metrics (hit rate) if enabled.
2. Forbid `visibility = ["//visibility:public"]` without review for internal libs.
3. Dependency update automation (Renovate) for Maven pins.

### 7. Hand off

1. Package layout and naming conventions (`//service/api:lib`).
2. How to add a Maven dep via `rules_jvm_external`.
3. Common error runbook (visibility, header jars, processor path).

## Visibility Patterns

| Pattern | Use |
| --- | --- |
| `//visibility:private` | Default for internal libs |
| `//service:__pkg__` | Same package only |
| `//service:__subpackages__` | Service internals |
| Explicit list | Cross-team APIs |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Deps | Explicit `deps` | Wildcard exports everywhere |
| Size | Small libraries | One `java_library` for entire monorepo |
| JDK | Pinned toolchain | Works only on my laptop JDK |
| Tests | `java_test` in CI | Manual IDE-only tests |
| Secrets | Not in BUILD files | API keys in `jvm_flags` committed |

## Output Checklist

- [ ] Bazel/Java versions pinned
- [ ] `java_library`/`binary`/`test` targets created
- [ ] Visibility policy applied
- [ ] External Maven deps hermetic
- [ ] Build and test evidenced
- [ ] Toolchain documented
- [ ] CI uses Bazelisk
- [ ] `code-quality-standards` applied to Java sources

## Rules

- Authorized build systems only.
- Prefer hermetic, pinned toolchains.
- Least visibility for libraries.
- No secrets in BUILD/bazelrc committed.
- Pair remote cache security with its skill.
