---
name: quarkus-native
description: Deep expertise in Quarkus Native Image builds, GraalVM integration, reflection configuration, and Profile-Guided Optimization. Use for native compilation questions.
version: 1.0.0
keywords: [quarkus, native-image, graalvm, aot, native, optimization]
---

# quarkus-native

> Keyword: quarkus-native | Platforms: gemini,claude,codex

Quarkus Native Image Expert Skill - Specialized in building, optimizing, and troubleshooting native executables for Quarkus applications.

## Core Mandates

- **Closed-World Awareness:** All classes, methods, and resources must be known at build time.
- **Reflection Explicit:** Register all reflection usage via `@RegisterForReflection` or `reflection-config.json`.
- **Resource Registration:** All runtime resources must be declared in `resource-config.json`.
- **Build-Time Initialization:** Prefer build-time initialization for faster startup; use runtime init only for side-effect classes.
- **Test in Native Mode:** Always run `@QuarkusIntegrationTest` against the native binary before production.

---

## Quick Start: Native Build

### Maven

```bash
# Build native executable
./mvnw package -Dnative

# Build in container (recommended for CI)
./mvnw package -Dnative -Dquarkus.native.container-build=true

# Build and run integration tests
./mvnw verify -Pnative
```

### Gradle

```bash
# Build native executable
./gradlew build -Dquarkus.package.type=native

# Build in container
./gradlew build -Dquarkus.package.type=native -Dquarkus.native.container-build=true
```

### Bazel (rules_quarkus)

```bash
# Using rules_quarkus
bazel build //:myapp_native

# With custom builder image
bazel build //:myapp_native \
  --@rules_quarkus//native:builder_image=quay.io/quarkus/ubi-quarkus-mandrel-builder-image:jdk-21
```

---

## Quarkus Native Configuration

### Essential Properties

```properties
# === Build Type ===
quarkus.package.type=native

# === Container Build (Recommended) ===
quarkus.native.container-build=true
quarkus.native.builder-image=quay.io/quarkus/ubi-quarkus-mandrel-builder-image:jdk-21

# === Memory ===
quarkus.native.native-image-xmx=8g

# === Debugging ===
quarkus.native.additional-build-args=-H:+ReportExceptionStackTraces

# === Reports ===
quarkus.native.enable-reports=true
# Generates: target/reports/call_tree_*.txt, target/reports/reachable_methods.txt
```

### Profile-Specific Native Config

```properties
# application.properties
%prod.quarkus.package.type=native
%prod.quarkus.native.container-build=true
%prod.quarkus.native.builder-image=quay.io/quarkus/ubi-quarkus-mandrel-builder-image:jdk-21

# Development (JVM mode for fast startup)
%dev.quarkus.package.type=jar

# Test (native for integration tests)
%test.quarkus.package.type=native
```

### Builder Images

| Image | JDK | Size | Use Case |
|-------|-----|------|----------|
| `ubi-quarkus-mandrel-builder-image:jdk-21` | 21 | Medium | General purpose |
| `ubi-quarkus-graalvmce-builder-image:jdk-21` | 21 | Large | GraalVM CE with all features |
| `ubi-quarkus-mandrel-builder-image:jdk-21.0.2.0-Final-java21` | 21 | Medium | Specific Mandrel version |

---

## Reflection Configuration

### @RegisterForReflection (Recommended)

```java
// Register a single class
@RegisterForReflection
public class UserDto {
    private String name;
    private String email;
    // getters/setters
}

// Register with specific targets
@RegisterForReflection(targets = { UserDto.class, OrderDto.class })
public class ReflectionConfig {
}

// Register all fields and methods
@RegisterForReflection(fields = false, methods = true)
public class ApiResponse {
    public String status;
    public Object data;
}
```

### reflection-config.json

```json
[
  {
    "name": "com.example.UserDto",
    "allDeclaredConstructors": true,
    "allPublicConstructors": true,
    "allDeclaredMethods": true,
    "allPublicMethods": true,
    "allDeclaredFields": true,
    "allPublicFields": true
  },
  {
    "name": "com.example.OrderDto",
    "methods": [
      { "name": "getId", "parameterTypes": [] },
      { "name": "setId", "parameterTypes": ["java.lang.Long"] }
    ],
    "fields": [
      { "name": "status" }
    ]
  }
]
```

### Native Image Agent (Auto-Generate)

```bash
# Run tests with agent to auto-generate reflection config
./mvnw test -Dquarkus.native.agent.enabled=true

# Or run the application with agent
java -agentlib:native-image-agent=config-output-dir=src/main/resources/META-INF/native-image \
  -jar target/quarkus-app/quarkus-run.jar

# Merge with existing config
java -agentlib:native-image-agent=config-merge-dir=src/main/resources/META-INF/native-image \
  -jar target/quarkus-app/quarkus-run.jar
```

---

## Resource Configuration

### resource-config.json

```json
{
  "resources": {
    "includes": [
      { "pattern": "\\Qapplication.properties\\E" },
      { "pattern": "\\Qdb/migration/.*\\E" },
      { "pattern": "\\QMETA-INF/.*\\E" },
      { "pattern": "\\Qtemplates/.*\\E" }
    ],
    "excludes": [
      { "pattern": "\\Q*.test\\E" }
    ]
  },
  "bundles": [
    { "name": "messages" },
    { "name": "ValidationMessages" }
  ]
}
```

### Quarkus Resource Registration

```properties
# Register resources in application.properties
quarkus.native.resources.includes=db/migration/.*,templates/.*
quarkus.native.resources.excludes=*.test,*.dev
```

---

## Initialization Configuration

### Build-Time vs Runtime Initialization

```properties
# application.properties
quarkus.native.additional-build-args=\
  --initialize-at-build-time=com.example.ConfigClass,\
  --initialize-at-run-time=com.example.NetworkClient,\
  --trace-class-initialization=com.example.*
```

### Common Initialization Patterns

```java
// Build-time initialization (fast startup)
@io.quarkus.runtime.annotations.RegisterForReflection
public class BuildTimeConfig {
    public static final String VERSION = "1.0.0";  // Initialized at build time
}

// Runtime initialization (for classes with side effects)
public class RuntimeConfig {
    static {
        // This runs at runtime, not build time
        System.loadLibrary("native-lib");
    }
}
```

---

## Profile-Guided Optimization (PGO)

### Step-by-Step PGO

```bash
# Step 1: Build instrumented native binary
./mvnw package -Dnative \
  -Dquarkus.native.additional-build-args=--pgo-instrument

# Step 2: Run instrumented binary to collect profile data
./target/myapp-1.0.0-SNAPSHOT-runner
# Exercise typical workloads: API calls, database operations, etc.
# This generates: default.iprof

# Step 3: Build optimized binary with profile
./mvnw package -Dnative \
  -Dquarkus.native.additional-build-args=--pgo=default.iprof
```

### PGO with Custom Profile Name

```bash
# Build instrumented with custom profile name
./mvnw package -Dnative \
  -Dquarkus.native.additional-build-args=--pgo-instrument=myapp.iprof

# Run and collect profile
./target/myapp-1.0.0-SNAPSHOT-runner

# Build optimized
./mvnw package -Dnative \
  -Dquarkus.native.additional-build-args=--pgo=myapp.iprof
```

---

## Native Image Testing

### @QuarkusIntegrationTest

```java
@QuarkusIntegrationTest
class NativeUserResourceIT {

    @Test
    void shouldListUsers() {
        given()
            .when().get("/api/users")
            .then()
            .statusCode(200);
    }

    @Test
    void shouldCreateUser() {
        given()
            .contentType(ContentType.JSON)
            .body("{\"name\": \"Alice\", \"email\": \"alice@example.com\"}")
            .when().post("/api/users")
            .then()
            .statusCode(201);
    }
}
```

### Conditional Native Testing

```java
@QuarkusTest
class UserResourceTest {

    @Test
    @DisabledOnNativeImage
    void shouldTestDevOnlyFeature() {
        // Only runs in JVM mode
    }

    @Test
    @EnabledOnNativeImage
    void shouldTestNativeOnlyFeature() {
        // Only runs in native mode
    }
}
```

---

## Troubleshooting Decision Tree

```
Native build failed?
  ├── "ClassNotFoundException" at runtime
  │     └── Missing reflection config
  │         ├── Add @RegisterForReflection to the class
  │         ├── Add to reflection-config.json
  │         └── Run with native-image agent
  ├── "NoSuchMethodException" at runtime
  │     └── Missing method in reflection config
  │         └── Add method to reflection-config.json
  ├── "MissingResourceException"
  │     └── Resource not included in native image
  │         ├── Add to resource-config.json
  │         └── Use quarkus.native.resources.includes
  ├── "UnsupportedFeatureError"
  │     └── Using unsupported JVM feature
  │         ├── Check GraalVM limitations
  │         └── Use --report-unsupported-elements-at-runtime
  ├── "OutOfMemoryError" during build
  │     └── Increase build memory
  │         └── quarkus.native.native-image-xmx=8g (or 12g)
  ├── Build timeout
  │     └── Increase timeout or use more powerful machine
  │         └── quarkus.native.additional-build-args=--timeout=600
  └── "Image build request failed"
        └── Docker/container issues
            └── Check Docker daemon, pull builder image manually
```

### Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ClassNotFoundException` | Missing reflection config | Add `@RegisterForReflection` or `reflect-config.json` |
| `NoSuchMethodException` | Method not in reflection config | Add method to `reflect-config.json` |
| `MissingResourceException` | Resource not included | Add to `resource-config.json` |
| `IllegalArgumentException: Proxy` | Missing proxy config | Add to `proxy-config.json` |
| `OutOfMemoryError` | Insufficient build memory | Increase `quarkus.native.native-image-xmx` |
| `UnsupportedFeatureError` | Unsafe/JNI usage | Use `--report-unsupported-elements-at-runtime` |
| `Image build request failed` | Docker not running | Start Docker daemon |
| `Build timeout` | Complex application | Increase timeout, use more memory |

---

## Optimization Strategies

### Reducing Image Size

```properties
# Remove unused beans
quarkus.native.remove-unused-beans=true

# Remove metadata for smaller image
quarkus.native.enable-reports=false

# Exclude unnecessary resources
quarkus.native.resources.excludes=*.md,*.txt
```

### Improving Startup Time

```properties
# Use SerialGC for small heaps (default for native)
quarkus.native.additional-build-args=--gc=serial

# Or G1GC for larger heaps
quarkus.native.additional-build-args=--gc=G1

# Enable PGO for better performance
quarkus.native.additional-build-args=--pgo=default.iprof
```

### Memory Tuning

```properties
# Set max heap for native image
quarkus.native.additional-build-args=-R:MaxHeapSize=256m

# Set initial heap
quarkus.native.additional-build-args=-R:MinHeapSize=64m
```

---

## Bazel Native Build

### BUILD.bazel for Native Image

```python
load("@rules_quarkus//quarkus:defs.bzl", "quarkus_application")

quarkus_application(
    name = "myapp_native",
    srcs = glob(["src/main/java/**/*.java"]),
    resources = glob(["src/main/resources/**"]),
    deps = [
        "//common/utils",
        "@maven//:io_quarkus_quarkus_core",
        "@maven//:io_quarkus_quarkus_rest",
    ],
    native = True,
    native_image_xmx = "8g",
    additional_build_args = [
        "-H:+ReportExceptionStackTraces",
        "--initialize-at-build-time=com.example.Config",
    ],
)
```

---

## References

- [Quarkus Native Guide](https://quarkus.io/guides/building-native-image)
- [GraalVM Native Image](https://www.graalvm.org/latest/reference-manual/native-image/)
- [Mandrel Documentation](https://github.com/graalvm/mandrel)
- [Quarkus Native Reference](https://quarkus.io/guides/native-reference)

## Skill Interoperability

The **quarkus-native** skill specializes in:
- **graalvm-expert** 🚀: Core GraalVM Native Image knowledge.
- **quarkus-expert** ⚡: Quarkus-specific native build configuration.
- **rules-quarkus** 🔧: Bazel integration for native builds.
