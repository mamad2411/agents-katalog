---
name: yocto-ci-kas-build
description: Official-doc-first Yocto CI, kas, and reproducible build workflow support for AI coding agents. Use when creating or modifying kas YAML files, CI pipelines, containerized Yocto builds, shared DL_DIR or SSTATE_DIR caching, build matrix jobs, smoke builds, artifact publishing, reproducibility checks, or repository onboarding workflows for Yocto/OpenEmbedded projects.
---

# Yocto CI Kas Build

## Core Workflow

1. Inspect existing build entrypoints first: `kas*.yml`, wrapper scripts, Dockerfiles, CI YAML, README build instructions, and release scripts.
2. Identify release, layer refs, `MACHINE`, `DISTRO`, image targets, SDK targets, and artifact expectations.
3. Keep repository source orchestration explicit: kas repos, branch pins, commit pins, lockfiles, submodules, or repo manifests.
4. Keep `DL_DIR` and `SSTATE_DIR` cache policy explicit and separate from generated build output.
5. Use CI jobs to validate representative machines/images, not every possible target unless requested.
6. Publish artifacts with checksums, provenance, manifests, and release metadata.

Use [yocto_ci_doc_router.py](scripts/yocto_ci_doc_router.py) with a topic name for official documentation links.

## References

- [kas-patterns.md](references/kas-patterns.md): kas file structure, repos, layers, local config, and lock/pin patterns.
- [ci-cache-patterns.md](references/ci-cache-patterns.md): downloads, sstate, hash equivalence, runner storage, and cache keys.
- [build-reproducibility.md](references/build-reproducibility.md): source pinning, host/container policy, artifacts, and release metadata.

## Guardrails

- Do not hardcode host-specific absolute paths.
- Do not commit generated build output, `tmp`, `sstate-cache`, `downloads`, or deploy artifacts unless the repo intentionally tracks fixtures.
- Do not use floating refs for release builds unless the workflow is explicitly non-release.
- Do not leak mirror credentials, signing keys, or private registry tokens into CI logs.
