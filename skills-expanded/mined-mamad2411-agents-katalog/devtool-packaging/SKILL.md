---
name: devtool-packaging
description: Build, packaging, signing, and release specialist. Owns build pipeline, artifacts (npm, wheel, binary, container), code signing, SBOM, release automation, and provenance. Auto-invoked for build / release / signing / distribution work.
---

# DevTool Packaging & Release

An unsigned binary is a security alert; a broken release is a weekend. For a tool
others install, reproducibility, signing, and provenance carry as much trust as the
code itself.

## When to reach for this

- Designing or fixing the build → sign → publish pipeline
- Adding a distribution channel (npm, PyPI, Homebrew, container registry, installer)
- Setting up code signing, SBOM generation, or SLSA-style provenance
- Hardening the supply chain: tokens, lockfiles, pinned actions

## Principles

1. **Reproducible builds.** Pin the toolchain (exact compiler/runtime version in a
   committed file), commit lockfiles, build in clean containers/runners — never from a
   developer laptop. Same commit must yield the same artifact.
2. **Sign everything shipped.** Authenticode for Windows binaries, notarization +
   hardened runtime for macOS, sigstore/cosign for containers and language packages,
   GPG where the ecosystem expects it. Unsigned macOS/Windows binaries trip Gatekeeper
   and SmartScreen — that's lost installs, not just lost polish.
3. **Provenance by default.** Generate SLSA build provenance and an SBOM (CycloneDX or
   SPDX, via syft or the ecosystem tool) per release artifact, publish them alongside
   it, and document how a consumer verifies.
4. **Least-privileged publish credentials.** Prefer OIDC trusted publishing
   (PyPI, npm, crates.io support it) over long-lived tokens; where tokens are
   unavoidable, scope them to one package, store in CI secrets, rotate on a schedule.
5. **Pre-release canaries.** Tag `-beta.N`/`-rc.N` to the pre-release channel
   (npm dist-tag, PyPI pre-release, separate Homebrew tap) before stable — never
   `main` straight to `latest`.
6. **Releases are one trigger, zero hands.** Version bump (changesets /
   release-please) → tag → matrix build → sign → attest → publish → release notes.
   Any manual step is the step that gets skipped at 6pm Friday.

## Release pipeline skeleton

| Stage | Gate to pass |
|---|---|
| Version + changelog | changeset/conventional-commit derived; human approves the bump |
| Matrix build | all targets (incl. linux-arm64, macos-arm64) green; artifacts hashed |
| Sign + notarize | signature verification re-run on the built artifact, not assumed |
| SBOM + provenance | generated per artifact, attached to the release |
| Publish to pre-release channel | smoke install on each OS: `tool --version` works |
| Promote to stable | manual approval; promotion republishes the *same* artifacts |
| Announce | release notes + docs deploy triggered by the same tag |

## Pitfalls

- Rebuilding for the stable promotion instead of promoting the already-tested artifact
- Publish token with org-wide scope sitting in CI for years
- Unpinned third-party CI actions/orbs (`uses: some/action@main`) in the release path
- Lockfile not committed, or `latest` base images, making builds time-dependent
- Signing verified only by "the step didn't fail" — verify the artifact itself
- Forgetting the install-test: artifact publishes fine but `npm i -g` / `pipx install`
  fails on a platform nobody smoke-tested
- Shipping dev/test files in the package (check artifact contents, e.g.
  `npm pack --dry-run`)

---
*Related: `devtool-cli-ux` (completion scripts and install UX), `devtool-library-api`
(what the artifact must export), `devtool-docgen` (release-triggered docs publish) ·
domain agent: `devtool-architect` (distribution strategy, versioning policy) ·
output/ADR format: `playbook-conventions`*
