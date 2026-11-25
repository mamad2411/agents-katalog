---
name: supply-chain-security
description: Pins dependencies and CI actions, checks package provenance and trims workflow permissions to reduce the damage a poisoned package could do.
---

# Supply chain security

Reduce what a bad package can do, and make surprises visible.

## Steps

1. Lockfiles: confirm one is committed for each ecosystem, and that CI installs from it strictly (`npm ci`, `pip install --require-hashes`, `cargo --locked`, `go mod verify`). Fail the build when the lockfile is out of date.
2. Pin versions: no `latest` or open ranges in production manifests. Pin Docker base images by digest. Pin GitHub Actions to full commit SHAs, with the tag in a comment.
3. Review the dependency list for look-alike names, abandoned packages and ones with install scripts. Disable lifecycle scripts in CI where not needed (`--ignore-scripts`).
4. Provenance: use registry features such as npm provenance and `npm audit signatures`, sigstore or checksums for downloaded binaries. Verify checksums in scripts that `curl` installers; never pipe to a shell.
5. CI permissions: set `permissions: contents: read` at the top of each workflow and grant more per job. Avoid `pull_request_target` with untrusted code checkout. Scope secrets to environments that need approval. Prefer short-lived OIDC credentials to stored cloud keys.
6. Automate updates with Dependabot or Renovate, with grouped PRs and a cooldown of a few days for new releases.
7. Generate an SBOM (`syft` or `cyclonedx`) and store it with releases.

## Rules

- Change one layer per commit.
- Never remove a control to make a build pass without saying so.

## Report

Controls added, files changed, risks still open and what each would cost to close.
