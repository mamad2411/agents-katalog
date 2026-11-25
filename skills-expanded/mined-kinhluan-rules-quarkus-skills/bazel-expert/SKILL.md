---
name: bazel-expert
description: Expert knowledge for writing idiomatic Bazel rules, Starlark best practices, and build performance optimization. Use for Bazel build system questions.
version: 1.2.0
keywords: [bazel, starlark, monorepo, build-system, hermetic, build]
---

# bazel-expert

> Keyword: bazel | Platforms: gemini,claude,codex

General Bazel & Starlark Expert Skill - Expert guidance on writing idiomatic Bazel rules and optimizing build performance.

## Architectural Mandates

- **Hermeticity:** Actions must only depend on declared inputs
- **Granularity:** Break large targets into smaller `java_library` or `starlark` rules
- **Bzlmod:** Always use Bzlmod for external dependency management
- **Visibility:** Default `visibility = ["//visibility:private"]`, explicitly widen only as needed

## rules_java & Java Toolchains

### Toolchain Setup (Bzlmod)

```python
# MODULE.bazel
bazel_dep(name = "rules_java", version = "7.12.4")

java_toolchains = use_extension("@rules_java//java:extensions.bzl", "toolchains")
java_toolchains.toolchain(version = "21")
use_repo(java_toolchains, "remotejdk21_linux")

register_toolchains("@remotejdk21_linux//:jdk")
```

### BUILD.bazel Examples

```python
# Library target with proper granularity
java_library(
    name = "user-service",
    srcs = glob(["src/main/java/**/*.java"]),
    resources = glob(["src/main/resources/**"]),
    deps = [
        "//common/utils:json-utils",
        "@maven//:com_google_guava_guava",
        "@maven//:jakarta_inject_jakarta_inject_api",
    ],
    visibility = ["//services:__subpackages__"],
)

# Test target with testonly deps
java_test(
    name = "user-service-test",
    srcs = glob(["src/test/java/**/*.java"]),
    test_class = "com.example.UserServiceTest",
    deps = [
        ":user-service",
        "@maven//:org_junit_jupiter_junit_jupiter",
        "@maven//:org_assertj_assertj_core",
        "@maven//:org_mockito_mockito_core",
    ],
)
```

### Do vs Don't

```python
# BAD - monolithic target, slow incremental builds
java_library(
    name = "everything",
    srcs = glob(["src/**/*.java"]),
    deps = ["@maven//:all-the-things"],
    visibility = ["//visibility:public"],
)

# GOOD - granular targets, fast incremental builds
java_library(
    name = "user-model",
    srcs = ["src/main/java/com/example/User.java"],
    deps = ["@maven//:jakarta_validation_jakarta_validation_api"],
)

java_library(
    name = "user-repository",
    srcs = ["src/main/java/com/example/UserRepository.java"],
    deps = [":user-model", "@maven//:io_quarkus_quarkus_hibernate_orm_panache"],
)
```

## rules_jvm_external (Maven Dependencies)

### Setup with Bzlmod

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
    fetch_sources = True,
    lock_file = "//:maven_install.json",
)
use_repo(maven, "maven")
```

### BOM Import

```python
maven.install(
    name = "maven",
    bom_imports = [
        "io.quarkus.platform:quarkus-bom:3.20.1",
    ],
    artifacts = [
        # Versions managed by BOM - no version needed
        "io.quarkus:quarkus-arc",
        "io.quarkus:quarkus-rest",
        "io.quarkus:quarkus-hibernate-orm-panache",
    ],
    lock_file = "//:maven_install.json",
)
```

### Re-pinning Dependencies

```bash
# After adding/updating artifacts in MODULE.bazel:
RULES_JVM_EXTERNAL_REPIN=1 bazelisk run @maven//:pin
```

## Starlark Best Practices

- **Avoid Macros for Logic:** Use `rules` for complex logic, `macros` for wrapping
- **Provider Pattern:** Use custom `Providers` to pass complex information between rules
- **Depsets:** Always use `depsets` instead of `lists` for transitive dependencies

### Custom Provider Example

```python
QuarkusExtensionInfo = provider(
    doc = "Information about a Quarkus extension",
    fields = {
        "runtime_jars": "depset of runtime JAR Files",
        "deployment_jars": "depset of deployment JAR Files",
    },
)

def _quarkus_extension_impl(ctx):
    runtime = depset(
        direct = [ctx.file.runtime_jar],
        transitive = [dep[QuarkusExtensionInfo].runtime_jars for dep in ctx.attr.deps],
    )
    return [QuarkusExtensionInfo(runtime_jars = runtime, deployment_jars = ...)]
```

### Depset Do vs Don't

```python
# BAD - O(N²) when collecting transitive deps
all_jars = []
for dep in ctx.attr.deps:
    all_jars += dep[JavaInfo].transitive_runtime_jars.to_list()

# GOOD - O(1) depset merging, lazy evaluation
all_jars = depset(transitive = [
    dep[JavaInfo].transitive_runtime_jars for dep in ctx.attr.deps
])
```

## Performance Optimization

- **Param Files:** Use `ctx.actions.args().use_param_file("@%s")` for long command lines
- **Remote Execution:** Ensure rules are compatible with remote execution
- **Action Mnemonics:** Use descriptive `mnemonic` and `progress_message` for debugging

### Build Performance Decision Tree

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Full rebuild on small change | Target too coarse | Split into smaller `java_library` targets |
| Slow first build, fast incremental | Expected behavior | Enable remote cache: `--remote_cache=grpc://...` |
| Slow even with cache | Cache misses | Run `--execution_log_json_file=log.json`, check non-hermetic inputs |
| "Argument list too long" | Too many classpath entries | Use `ctx.actions.args().use_param_file("@%s")` |
| OOM during analysis | Too many targets | Use `--host_jvm_args=-Xmx8g`, reduce `glob()` scope |
| Flaky test results | Non-hermetic test | Add `tags = ["no-sandbox"]` to debug, then fix inputs |

### Remote Cache & Execution

```bash
# .bazelrc - remote cache setup
build --remote_cache=grpc://cache.example.com:9092
build --remote_upload_local_results=true
build --remote_timeout=60

# Remote execution (requires RBE)
build:remote --remote_executor=grpc://rbe.example.com:8980
build:remote --jobs=200
build:remote --spawn_strategy=remote
```

## Troubleshooting

### "no matching toolchains found for //target"

```bash
# Diagnosis: Java toolchain not registered
bazel query @rules_java//toolchains:all

# Fix: Register in MODULE.bazel
register_toolchains("@remotejdk21_linux//:jdk")
```

### "dependency not found" after adding to maven.install

```bash
# Cause: lock file out of date
RULES_JVM_EXTERNAL_REPIN=1 bazelisk run @maven//:pin

# Verify target name (underscores replace dots/hyphens/colons):
# io.quarkus:quarkus-arc → @maven//:io_quarkus_quarkus_arc
bazel query @maven//:all | grep quarkus
```

### Circular dependency between targets

```python
# BAD - A depends on B, B depends on A
java_library(name = "A", deps = [":B"])
java_library(name = "B", deps = [":A"])

# FIX - Extract shared code into a third target
java_library(name = "shared", srcs = ["Shared.java"])
java_library(name = "A", deps = [":shared"])
java_library(name = "B", deps = [":shared"])
```

### Remote cache not being hit

```bash
# Debug: compare action keys
bazel build //target --execution_log_json_file=exec1.json
# Change something, rebuild
bazel build //target --execution_log_json_file=exec2.json
# Diff to find non-hermetic inputs
diff <(jq '.actionKey' exec1.json) <(jq '.actionKey' exec2.json)
```

### Build is hermetic locally but fails on CI

Common causes:
1. **Absolute paths leaking** → use `ctx.actions.args()` with `map_each` to relativize
2. **Timestamp in outputs** → ensure tools produce deterministic output
3. **Different host platform** → specify `--platforms=//platforms:linux_x86_64`
4. **Missing `data` attribute** → runtime files must be declared in `data`, not `srcs`

## Decision Trees

### When to use `macro` vs `rule`

```
Need custom providers or actions?
  YES → Write a rule
  NO → Does it wrap existing rules with defaults?
    YES → Write a macro
    NO → Does it need to inspect file contents or run tools?
      YES → Write a rule
      NO → Macro is fine
```

### When to use `genrule` vs custom rule

```
Is the action a single shell command?
  YES → genrule (but avoid for Java - use java_binary + rule)
  NO → Custom rule
Does it need to integrate with Java toolchain?
  YES → Custom rule (access ctx.toolchains)
  NO → genrule may suffice
```

## 🌐 Bazel Knowledge Sources

> **Directive:** Use `web_fetch` to find the latest macro signatures or Bzlmod extensions if a build fails with toolchain or dependency errors.

- **Bzlmod Migration:** [Bazel External Dependencies Guide](https://bazel.build/external/overview) - Managing the new MODULE.bazel system.
- **Starlark Rule Writing:** [Rules (Bazel)](https://bazel.build/extending/rules) - Providers, Actions, and toolchains.
- **Build Performance:** [Optimizing Bazel Builds](https://bazel.build/run/performance) - Profiling and caching.
- **Remote Execution:** [Remote Execution Overview](https://bazel.build/remote/rbe) - Scaling builds.

## References

- [Official Bazel Documentation](https://bazel.build/)
- [rules_java GitHub Repository](https://github.com/bazelbuild/rules_java)
- [rules_jvm_external Documentation](https://github.com/bazelbuild/rules_jvm_external)
- [Starlark Language Specification](https://github.com/bazelbuild/starlark/blob/master/spec.md)

## Skill Interoperability

The **bazel-expert** 🏗 skill provides the core build infrastructure for:
- **rules-quarkus** 🔧: Integrates Quarkus build and augmentation logic into the Bazel ecosystem.
