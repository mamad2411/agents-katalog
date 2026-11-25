---
name: yocto-ci-release
description: Yocto CI, reproducible build, and release engineering skill for AI coding agents. Use for kas, repo manifests, Git submodules, containerized builds, CI runners, downloads and sstate caches, hash equivalence, PR build gates, QEMU tests, hardware smoke tests, artifact publishing, SDK releases, SBOM/license manifests, release notes, and version pinning.
---

# Yocto CI Release

## Workflow

1. Identify source orchestration: `kas`, `repo`, submodules, manifest repo, or monorepo.
2. Pin every layer and external source needed for reproducibility.
3. Separate caches from build output: `DL_DIR`, `SSTATE_DIR`, hash equivalence, container caches, and artifacts.
4. Build the smallest useful CI matrix: parse, recipe smoke, image, SDK, QEMU/testimage, hardware smoke where available.
5. Publish signed and checksummed artifacts with machine, distro, image, git refs, build config, license data, and SBOM if enabled.
6. Keep secrets out of `local.conf`, logs, and artifacts.

## References

- [ci-release-playbook.md](references/ci-release-playbook.md): CI pipeline patterns, cache strategy, release artifact checklist.

## Guardrails

- Do not use floating branch refs for release builds.
- Do not persist `tmp/` as a cache unless the project explicitly accepts the fragility.
- Do not publish images without checksums and provenance.
- Do not run hardware flashing in CI without explicit device targeting and recovery controls.
