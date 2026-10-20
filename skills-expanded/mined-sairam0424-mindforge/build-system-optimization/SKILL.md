---
name: build-system-optimization
version: 1.0.0
min_mindforge_version: 10.7.0
status: stable
triggers: build system optimization, build cache architecture, incremental build design, remote build execution, dependency graph optimization, build farm design, Bazel Buck optimization, build time reduction, distributed build, build artifact caching, hermetic build, build reproducibility
---

# Skill — Build System Optimization

## When this skill activates

This skill activates when the user is optimizing build systems for speed and reliability. This includes build cache architecture, incremental builds, remote build execution, dependency graph optimization, build farm design, Bazel/Buck/Gradle optimization, build time reduction, distributed builds, artifact caching, hermetic builds, and build reproducibility.

## Mandatory actions when this skill is active

### Before writing any code

1. Establish baseline build times: clean build (no cache), incremental build (single file change), and CI build. Measure p50, p95, p99.
2. Profile the build to identify bottlenecks: dependency resolution, compilation, linking, testing, packaging. Use build system profiling tools (Gradle Build Scan, Bazel analyze-profile).
3. Audit dependency graph: identify unnecessary dependencies, circular dependencies, and overly-coupled modules.
4. Assess cache hit rates: local cache, remote cache, CI cache. Identify cache invalidation causes (non-deterministic inputs, timestamp dependencies).
5. Determine build reproducibility: same source + same toolchain = identical binary. Test by building twice and comparing checksums.

### During implementation

- **Incremental Builds:** Only rebuild changed modules and their dependents. Requires accurate dependency tracking. Bazel and Buck are incremental by design. Gradle requires careful task input/output declaration. Target: single-file change rebuild in under 30 seconds.
- **Build Caching:** Layer caching at multiple levels: local (developer machine), shared (team), remote (CI). Use content-addressable storage (hash inputs to determine cache key). Cache should serve 80%+ of CI builds from cache.
- **Remote Build Execution:** Offload compilation and tests to remote workers (Bazel Remote Execution, BuildBuddy, Gradle Enterprise). Provides massive parallelism (100+ workers). Requires hermetic builds.
- **Dependency Graph Optimization:** Reduce fan-out (modules with many dependents). Split large modules into smaller ones. Use interface modules to break circular dependencies. Visualize graph with Bazel query or Gradle's dependency graph plugin.
- **Hermetic Builds:** All inputs (source, toolchain, dependencies) must be explicit. No reliance on global state (env vars, system tools, internet access during build). Hermetic builds enable reproducibility and remote caching.
- **Build Artifact Caching:** Cache compiled binaries, test results, and packaged artifacts. Use content-addressable storage (Artifactory, Nexus, S3). Artifacts should be immutable (never overwrite).
- **Parallelization:** Build independent modules in parallel. Bazel parallelizes by default. Gradle requires `org.gradle.parallel=true`. Monitor CPU utilization (target: 80%+ during build).
- **Build Farm Design:** Centralized build cluster with auto-scaling workers. Use spot instances for cost savings. Workers should be stateless and ephemeral. Monitor queue depth and scale workers accordingly.
- **Build Time Reduction Targets:** Clean build under 10 minutes. Incremental build under 1 minute. CI build (with cache) under 5 minutes.

### After implementation

- Verify incremental builds only rebuild changed modules and dependents (use build system logs to confirm).
- Confirm cache hit rates exceed 80% in CI and 90% for developers (for incremental builds).
- Validate remote build execution distributes work across workers (monitor parallelism and CPU utilization).
- Ensure builds are hermetic by building in a clean container and comparing output checksums.
- Check that build artifact cache is content-addressable and serves artifacts in under 2 seconds.

## Self-check before task completion

- [ ] Baseline build times are measured (clean, incremental, CI) and tracked over time.
- [ ] Incremental builds only rebuild changed modules (verified via build logs).
- [ ] Build caching achieves 80%+ cache hit rate in CI.
- [ ] Remote build execution distributes work across workers with 80%+ CPU utilization.
- [ ] Dependency graph is optimized (reduced fan-out, no circular dependencies).
- [ ] Builds are hermetic (no reliance on global state or internet access).
- [ ] Build artifacts are cached in content-addressable storage and immutable.
- [ ] Build time targets are met: clean <10min, incremental <1min, CI <5min.
