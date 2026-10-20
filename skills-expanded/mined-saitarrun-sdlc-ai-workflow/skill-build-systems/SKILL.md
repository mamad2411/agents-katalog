---
name: skill-build-systems
description: Hermetic builds, dependency management, build caching, reproducible builds, cross-compilation, build optimization. Use when optimizing build speed, ensuring reproducibility, or designing build infrastructure.
version: 1.0.0
---

# Skill: Build Systems

Fast, reproducible, hermetic builds. No network calls. Same output every time.

## Hermetic Builds

**Requirements**:
- ✓ All dependencies vendored (in repo or locked)
- ✓ No network calls during build
- ✓ Deterministic output (bit-for-bit same)
- ✓ Works offline

**Example** (Bazel):
```
bazel build //app:binary
→ uses //third_party/go/dependencies.bzl (locked)
→ no network needed
→ same binary every time
```

## Reproducible Builds

```bash
# Build 1
$ bazel build //app --action_env=BUILD_TIME=0
$ sha256sum bazel-bin/app/binary
→ abc123...

# Build 2 (week later)
$ bazel build //app --action_env=BUILD_TIME=0
$ sha256sum bazel-bin/app/binary
→ abc123...  # Identical!
```

## Caching Strategy

- **Local cache**: ~/.cache/bazel (fast)
- **Shared cache**: S3/GCS (team)
- **CI cache**: Previous builds (speed up)

**Cache hit = skip recompilation**

## Dependency Locking

```yaml
# dependencies.lock
requests:
  version: 2.28.0
  sha256: abc123...
  url: https://pypi.org/packages/...

urllib3:
  version: 1.26.0
  sha256: def456...
```

**Freeze dependencies** → reproducible

## Build Optimization

- **Parallelism**: `-j 8` (8 parallel builds)
- **Incremental**: Only rebuild changed files
- **Caching**: Reuse previous outputs
- **Sandboxing**: Isolation (prevents hidden dependencies)

## Binary Optimization

```bash
# Strip debug symbols
$ strip -s app

# Compress
$ upx -9 app

# Size reduction: 50MB → 5MB
```

---

**Status**: Ready for build work  
**Best for**: Build optimization, hermetic builds, reproducibility
