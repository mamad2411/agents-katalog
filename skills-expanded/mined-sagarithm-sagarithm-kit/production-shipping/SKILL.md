---
id: "delivery.shipping-and-launch"
name: "Production Shipping & Release Governance"
version: "1.2.0"
domain: "delivery"
description: "Governs production deployments, releases, and distribution. Enforces formal verification gates, SemVer versioning, changelog synchronization, and multi-platform CI/CD attestation."
triggers:
  - "Preparing a production release or npm/container publication"
  - "Tagging a version or updating CHANGELOG.md"
  - "User says 'ship it', 'deploy to production', or 'prepare release'"
---

# 🚢 Production Shipping & Release Governance

> **"Shipping is not just pushing a git tag; it is an irrevocable contract with users and downstream dependencies. A release must carry empirical proof of correctness."**

Releasing software without systematic verification leads to registry rollback panics, broken client lockfiles, and reputational damage. This skill ensures that every release candidate passes through strict pre-flight gates before touching production or public registries.

---

## 🔒 The 4 Pre-Release Verification Gates

Every production release candidate must pass all four gates sequentially:

1. **Gate 1: Verification Gate Attestation**:
   - Execute `sagarithm verify` in strict mode.
   - All 5 vectors must return `✅ PASS`:
     - `STATIC`: Clean compilation and zero lint errors.
     - `SECURITY`: 0 issues detected, Shannon entropy scan clean.
     - `ARCHITECTURE`: Dependency graph verified acyclic, zero directory anti-patterns.
     - `BEHAVIORAL`: Automated test suite passed with 100% green exit code.
     - `DOCUMENTATION`: Project topology manifest (`sagarithm.manifest.json`) synchronized.
2. **Gate 2: Strict SemVer Evaluation**:
   - **Patch (`x.y.Z`)**: Backward-compatible bug fixes or packaging updates.
   - **Minor (`x.Y.z`)**: Backward-compatible new features, skills, or CLI commands.
   - **Major (`X.y.z`)**: Any breaking change to public APIs, configuration schemas, or CLI behavior.
3. **Gate 3: Changelog Synchronization**:
   - `CHANGELOG.md` updated under Keep a Changelog standards.
   - Changes categorized into `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, or `Security`.
4. **Gate 4: Clean Git Tree & Tagging**:
   - Working tree strictly clean (`git status` returns nothing to commit).
   - Annotated signed tag created: `git tag -a vX.Y.Z -m "Release vX.Y.Z - <summary>"`.

---

## 🛑 Anti-Rationalization Matrix

| Agent Excuse / Shortcut | Architectural Reality | Mandatory Action |
|---|---|---|
| *"Tests passed locally yesterday, so we can skip running them."* | Uncommitted changes or environment drift frequently break builds silently. | Run full test and verification suite immediately prior to release tagging. |
| *"It's just a tiny internal fix; we can overwrite the existing version."* | Registry versions on npm, crates.io, and PyPI are immutable. Overwrites cause severe caching collisions. | Always bump the patch version strictly according to SemVer. |
| *"We can update the CHANGELOG after pushing the release."* | Post-release changelog edits get forgotten, leaving users with mystery versions. | Changelog updates must be committed in the exact release commit. |
| *"CI failed on only 1 OS, but it passed on Windows so it's probably fine."* | Multi-OS failures indicate hidden path separator or runtime incompatibilities. | Release is blocked until all CI matrix runners (Ubuntu, macOS, Windows) are 100% green. |
