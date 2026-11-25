---
name: security-supply-chain-review
description: "Review dependency, lockfile, build/release, provenance, license, CVE, or artifact-scan changes."
---

# Security Supply Chain Review

Check dependency provenance, lockfiles, generated code, CI gates, artifact integrity, SBOM/provenance, and container scanning.

## Trigger boundary

Use this skill when a change adds or upgrades dependencies, lockfiles, generated code, build/release scripts, SBOM/provenance, licenses, CVE gates, or artifact/container scanning.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no dependency, artifact, build, release, license, or scan impact; follow the repository's established convention directly.

## Evidence

Prefer code, tests, logs, config, API contracts, and data examples over assumptions.

## Focused References

- [01-dependencies-and-ci.md](./references/01-dependencies-and-ci.md) - Dependencies And CI
- [02-release-process-and-tools.md](./references/02-release-process-and-tools.md) - Release Process And Tools
