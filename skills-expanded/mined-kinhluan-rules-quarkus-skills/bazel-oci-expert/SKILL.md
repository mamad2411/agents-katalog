---
name: bazel-oci-expert
description: Expert knowledge for building OCI container images with Bazel using rules_oci. Use for containerizing Quarkus/Java applications, multi-arch builds, and image optimization.
version: 1.0.0
keywords: [bazel, oci, container, docker, image, rules_oci, multi-arch, quarkus]
---

# bazel-oci-expert

> Keyword: oci | Platforms: gemini,claude,codex

Bazel OCI Container Expert Skill - Building, optimizing, and publishing OCI-compliant container images using `rules_oci` for Quarkus and Java applications.

## Core Mandates

- **rules_oci First:** Use `rules_oci` (not `rules_docker`) for OCI-compliant image builds. `rules_docker` is deprecated.
- **Hermetic Images:** All image layers must be built hermetically within Bazel - no `docker build`.
- **Distroless Base:** Prefer distroless or minimal base images (e.g., `gcr.io/distroless/java21-debian12`) for security.
- **Multi-Arch:** Build for both AMD64 and ARM64 using platform transitions.
- **Layer Caching:** Separate application code from dependencies to maximize layer cache hits.

---

## Setup (Bzlmod)

### MODULE.bazel

```python
bazel_dep(name = "rules_oci", version = "2.0.0")

oci = use_extension("@rules_oci//oci:extensions.bzl", "oci")

# Pull base images
oci.pull(
    name = "distroless_java21",
    digest = "sha256:abc123...",  # Pin by digest, not tag
    image = "gcr.io/distroless/java21-debian12",
    platforms = [
        "linux/amd64",
        "linux/arm64",
    ],
)

oci.pull(
    name = "ubi_minimal",
    digest = "sha256:def456...",
    image = "registry.access.redhat.com/ubi9/ubi-minimal",
    platforms = [
        "linux/amd64",
        "linux/arm64",
    ],
)

use_repo(oci, "distroless_java21", "ubi_minimal")
```

### WORKSPACE.bazel (Legacy - avoid if using Bzlmod)

```python
load("@rules_oci//oci:pull.bzl", "oci_pull")

oci_pull(
    name = "distroless_java21",
    digest = "sha256:abc123...",
    image = "gcr.io/distroless/java21-debian12",
)
```

---

## Building Container Images

### Basic Java Application Image

```python
# services/user/BUILD.bazel
load("@rules_oci//oci:defs.bzl", "oci_image", "oci_tarball")
load("@rules_pkg//pkg:tar.bzl", "pkg_tar")

# Package the JAR into a tar layer
pkg_tar(
    name = "app_layer",
    srcs = [":user-service_deploy.jar"],  # java_binary with deploy_env
    package_dir = "/app",
)

# Package dependencies into a separate layer
pkg_tar(
    name = "deps_layer",
    srcs = [":user-service-deps.jar"],
    package_dir = "/app/lib",
)

# Build the OCI image
oci_image(
    name = "user-service_image",
    base = "@distroless_java21",
    tars = [
        ":deps_layer",
        ":app_layer",
    ],
    entrypoint = ["/usr/bin/java", "-jar", "/app/user-service_deploy.jar"],
    env = {
        "JAVA_TOOL_OPTIONS": "-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0",
    },
)

# Create a tarball for docker load
oci_tarball(
    name = "user-service_tar",
    image = ":user-service_image",
    repo_tags = ["user-service:latest"],
)
```

### Quarkus Application Image

```python
# services/order/BUILD.bazel
load("@rules_oci//oci:defs.bzl", "oci_image", "oci_tarball")
load("@rules_pkg//pkg:tar.bzl", "pkg_tar")

# Layer 1: Quarkus dependencies (rarely changes)
pkg_tar(
    name = "quarkus_deps_layer",
    srcs = [":order-service-quarkus-app/lib"],
    package_dir = "/app/lib",
)

# Layer 2: Quarkus app (changes frequently)
pkg_tar(
    name = "quarkus_app_layer",
    srcs = [
        ":order-service-quarkus-app/quarkus-run.jar",
        ":order-service-quarkus-app/app",
    ],
    package_dir = "/app",
)

# Layer 3: Native libraries (if using JNI)
pkg_tar(
    name = "native_libs_layer",
    srcs = glob(["src/main/resources/*.so"]),
    package_dir = "/app/native",
)

oci_image(
    name = "order-service_image",
    base = "@ubi_minimal",
    tars = [
        ":quarkus_deps_layer",
        ":quarkus_app_layer",
        ":native_libs_layer",
    ],
    entrypoint = ["java", "-jar", "/app/quarkus-run.jar"],
    env = {
        "QUARKUS_HTTP_HOST": "0.0.0.0",
        "QUARKUS_HTTP_PORT": "8080",
        "JAVA_TOOL_OPTIONS": "-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -Djava.util.logging.manager=org.jboss.logmanager.LogManager",
    },
    exposed_ports = ["8080/tcp"],
)

oci_tarball(
    name = "order-service_tar",
    image = ":order-service_image",
    repo_tags = [
        "order-service:latest",
        "order-service:v1.0.0",
    ],
)
```

### Native Image Container

```python
# services/payment/BUILD.bazel
load("@rules_oci//oci:defs.bzl", "oci_image", "oci_tarball")
load("@rules_pkg//pkg:tar.bzl", "pkg_tar")

# Native binary layer
pkg_tar(
    name = "native_binary_layer",
    srcs = [":payment-service-native"],  # GraalVM native binary
    package_dir = "/app",
)

# Native image is much smaller - use scratch or distroless
oci_image(
    name = "payment-service_image",
    base = "@distroless_static",  # Static binary base (no libc needed)
    tars = [":native_binary_layer"],
    entrypoint = ["/app/payment-service-native"],
    env = {
        "QUARKUS_HTTP_HOST": "0.0.0.0",
        "QUARKUS_HTTP_PORT": "8080",
    },
    exposed_ports = ["8080/tcp"],
)

oci_tarball(
    name = "payment-service_tar",
    image = ":payment-service_image",
    repo_tags = ["payment-service:native"],
)
```

---

## Multi-Architecture Images

### Platform-Specific Image Build

```python
# platforms/BUILD.bazel (from bazel-expert)
platform(
    name = "linux_amd64",
    constraint_values = [
        "@platforms//os:linux",
        "@platforms//cpu:x86_64",
    ],
)

platform(
    name = "linux_arm64",
    constraint_values = [
        "@platforms//os:linux",
        "@platforms//cpu:arm64",
    ],
)
```

```python
# services/user/BUILD.bazel
load("@rules_oci//oci:defs.bzl", "oci_image", "oci_image_index")

# AMD64 image
oci_image(
    name = "user-service_image_amd64",
    base = "@distroless_java21_linux_amd64",
    tars = [":app_layer"],
    entrypoint = ["/usr/bin/java", "-jar", "/app/user-service.jar"],
)

# ARM64 image
oci_image(
    name = "user-service_image_arm64",
    base = "@distroless_java21_linux_arm64",
    tars = [":app_layer"],
    entrypoint = ["/usr/bin/java", "-jar", "/app/user-service.jar"],
)

# Multi-arch index (manifest list)
oci_image_index(
    name = "user-service_image",
    images = [
        ":user-service_image_amd64",
        ":user-service_image_arm64",
    ],
)
```

### Building with Platform Flag

```bash
# Build for specific platform
bazel build //services/user:user-service_image_amd64 \
  --platforms=//platforms:linux_amd64

# Build for ARM64
bazel build //services/user:user-service_image_arm64 \
  --platforms=//platforms:linux_arm64

# Build multi-arch index
bazel build //services/user:user-service_image
```

---

## Image Optimization

### Layer Ordering (Most Stable First)

```python
oci_image(
    name = "optimized_image",
    base = "@distroless_java21",  # Layer 0: Base (rarely changes)
    tars = [
        ":system_deps_layer",     # Layer 1: System deps (rarely changes)
        ":shared_libs_layer",     # Layer 2: Shared libraries (occasionally changes)
        ":app_deps_layer",        # Layer 3: App dependencies (changes with version bumps)
        ":app_code_layer",        # Layer 4: Application code (changes frequently)
        ":config_layer",          # Layer 5: Config files (changes per environment)
    ],
)
```

### JLink for Smaller Images

```python
# Create custom JRE with only needed modules
load("@rules_java//java:defs.bzl", "java_runtime")

java_runtime(
    name = "custom_jre",
    srcs = [":jlink_output"],  # Output of jlink command
    java = "bin/java",
)

# Use custom JRE as base
oci_image(
    name = "minimal_java_image",
    base = ":custom_jre_image",
    tars = [":app_layer"],
)
```

### Spring Boot / Quarkus Layered JARs

```python
# For Quarkus fast-jar layout
pkg_tar(
    name = "quarkus_lib_layer",
    srcs = glob(["quarkus-app/lib/main/*.jar"]),
    package_dir = "/app/lib/main",
)

pkg_tar(
    name = "quarkus_app_layer",
    srcs = [
        "quarkus-app/quarkus-run.jar",
        "quarkus-app/app/*.jar",
    ],
    package_dir = "/app",
)

oci_image(
    name = "quarkus_fastjar_image",
    base = "@distroless_java21",
    tars = [
        ":quarkus_lib_layer",
        ":quarkus_app_layer",
    ],
    entrypoint = ["java", "-jar", "/app/quarkus-run.jar"],
)
```

---

## Pushing Images

### Using oci_push

```python
load("@rules_oci//oci:defs.bzl", "oci_push")

oci_push(
    name = "push_user_service",
    image = ":user-service_image",
    remote_tags = ["latest", "v1.0.0", "{BUILD_TIMESTAMP}"],
    repository = "ghcr.io/myorg/user-service",
)
```

```bash
# Push to registry
bazel run //services/user:push_user_service

# With authentication
CRANE_AUTH_USERNAME=$GITHUB_ACTOR \
CRANE_AUTH_PASSWORD=$GITHUB_TOKEN \
bazel run //services/user:push_user_service
```

### Using crane (for advanced scenarios)

```python
load("@rules_oci//oci:defs.bzl", "oci_tarball")

oci_tarball(
    name = "user-service_for_crane",
    image = ":user-service_image",
    repo_tags = ["ghcr.io/myorg/user-service:latest"],
)
```

```bash
# Load and push with crane
crane push $(bazel cquery --output=files //services/user:user-service_for_crane) \
  ghcr.io/myorg/user-service:latest
```

---

## Image Inspection & Testing

### Structure Test

```python
load("@rules_oci//oci:defs.bzl", "oci_image")

# Use container_structure_test for validation
load("@container_structure_test//:defs.bzl", "container_structure_test")

container_structure_test(
    name = "user-service_structure_test",
    image = ":user-service_image",
    configs = ["structure_test.yaml"],
)
```

```yaml
# structure_test.yaml
schemaVersion: "2.0.0"
commandTests:
  - name: "java exists"
    command: "java"
    args: ["-version"]
    expectedError: ["openjdk version \"21"]

fileExistenceTests:
  - name: "app jar exists"
    path: "/app/user-service.jar"
    shouldExist: true

fileContentTests:
  - name: "correct entrypoint"
    path: "/app/user-service.jar"
    expectedContents: [".*"]
```

### Image Size Check

```bash
# Check image size
bazel build //services/user:user-service_image
bazel run //tools:oci_inspect -- $(bazel cquery --output=files //services/user:user-service_image)

# Or use crane
crane manifest $(bazel cquery --output=files //services/user:user-service_image) | jq '.layers[] | .size' | awk '{sum+=$1} END {print sum/1024/1024 " MB"}'
```

---

## Troubleshooting

### "base image not found"

```bash
# Cause: oci.pull not properly configured in MODULE.bazel
# Fix: Ensure use_repo(oci, "image_name") is called
# Fix: Check digest is correct and image is accessible
```

### "exec format error" in container

```bash
# Cause: Binary architecture doesn't match container architecture
# Fix: Build with correct --platforms flag
# Fix: Ensure base image matches target platform
```

### Image too large

```bash
# Diagnosis: Check layer sizes
crane manifest ghcr.io/myorg/image:latest | jq '.layers[] | {size: .size, digest: .digest[:12]}'

# Fix: Separate deps and app code into different layers
# Fix: Use jlink to create minimal JRE
# Fix: Use distroless base instead of full OS
# Fix: Remove unnecessary files from layers
```

### Push fails with authentication error

```bash
# Fix: Set CRANE_AUTH_USERNAME and CRANE_AUTH_PASSWORD
# Fix: Use docker login first if registry requires it
# Fix: Check repository URL is correct
```

---

## Decision Trees

### Choosing Base Image

```
Java application?
  ├── Need glibc? (most Java apps)
  │     ├── Minimal size → gcr.io/distroless/java21-debian12
  │     └── Need shell/debug → registry.access.redhat.com/ubi9/ubi-minimal
  ├── Static binary (GraalVM native)
  │     └── gcr.io/distroless/static (or scratch)
  └── Need package manager
        └── alpine:latest (not recommended for Java - musl issues)
```

### Layer Strategy

```
How often does this change?
  ├── Never (JDK, OS) → Base image
  ├── Rarely (framework deps) → Separate layer
  ├── Occasionally (app deps) → Separate layer
  ├── Frequently (app code) → Top layer
  └── Per environment (config) → Topmost layer
```

---

## References

- [rules_oci GitHub](https://github.com/bazel-contrib/rules_oci)
- [OCI Image Spec](https://github.com/opencontainers/image-spec)
- [Distroless Images](https://github.com/GoogleContainerTools/distroless)
- [crane CLI](https://github.com/google/go-containerregistry/blob/main/cmd/crane/README.md)
- [Quarkus Container Guide](https://quarkus.io/guides/container-image)

## Skill Interoperability

The **bazel-oci-expert** 🐳 skill provides containerization for:
- **rules-quarkus** 🔧: Containerize Quarkus applications built with Bazel.
- **bazel-expert** 🏗: Core Bazel build infrastructure.
- **bazel-k8s-expert** ☸️: Deploy containers to Kubernetes.
- **quarkus-expert** ⚡: Quarkus-specific container configurations.
- **graalvm-expert** 🚀: Native image container builds.
