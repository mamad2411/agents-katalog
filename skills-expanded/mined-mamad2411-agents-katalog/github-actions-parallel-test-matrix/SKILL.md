---
name: github-actions-parallel-test-matrix
description: GitHub Actions workflow uses a strategy.matrix over OS × toolchain to run all tests in parallel, with continue-on-error for nightly so unstable toolchains don't block merges.
category: ci
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [magika, ci]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Github Actions Parallel Test Matrix

**Trigger:** Multi-language project that must validate on Linux + macOS + Windows × stable + nightly without serial CI.

## Steps

- Define strategy.matrix with axes: os = [ubuntu-latest, macos-latest, windows-latest], toolchain = [stable, nightly].
- Each matrix cell runs the full suite; GitHub spawns them in parallel.
- Set continue-on-error: true for nightly so experimental compiler regressions don't block PRs.
- Cache language-specific dirs (Cargo registry, pip wheels, node_modules) keyed by lockfile hash.
- Name jobs descriptively (test (ubuntu / stable)) so matrix failures are easy to read.
- Aggregate: require stable cells to pass; let nightly be informational only.

## Counter / Caveats

- Matrix explosion (3 OS × N toolchains) burns CI minutes — macOS and Windows are ~10x more expensive on free tier.
- Flaky tests can fail on one cell and pass on another; quarantine flaky ones rather than rerunning blindly.
- Setup time often dominates short test suites; cache aggressively.
- 5GB artifact cap on free tier means you must clean up after large workflows.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `.github/workflows/rust-test.yml:1-60`
- `.github/workflows/python-build-and-release-package.yml:74-120`
