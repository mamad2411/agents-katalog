---
name: supply-chain-security
description: Use when adding dependencies, updating packages, or configuring build pipelines to prevent supply chain attacks.
invoke_when: Use when adding new dependencies, updating packages, reviewing lock files, or configuring CI/CD build steps.
---

# Supply Chain Security

## Core Rule

**Every dependency is code you did not write, did not review, and chose to trust.** Treat that trust as a liability to be actively managed, not a default to be assumed.

## Lock File Integrity

- **Always commit lock files** (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Pipfile.lock`, `poetry.lock`, `go.sum`). Lock files pin the exact dependency tree that was tested. Without them, `npm install` on CI may produce a different tree than the developer tested locally.
- **Review lock file diffs.** When a lock file changes, check that the changes match the intended update. A lock file diff that introduces unexpected packages is a red flag.
- **Use `--frozen-lockfile` in CI.** Run `npm ci` (not `npm install`), `yarn install --frozen-lockfile`, or `pip install --require-hashes`. If the lock file is out of date, the build should fail, not silently update dependencies.

## Dependency Pinning

- **Pin exact versions for production dependencies.** Use `1.2.3`, not `^1.2.3` or `~1.2.3`. Semver ranges trust that upstream maintainers will not introduce breaking or malicious changes in patch releases. That trust has been violated repeatedly.
- **Allow ranges for development dependencies** only if you accept the risk. Test tooling is lower risk than production runtime code, but a compromised dev dependency can still steal credentials or modify build output.
- **Pin GitHub Actions by SHA**, not by tag. Tags are mutable: `uses: actions/checkout@v4` can point to different code tomorrow. Use `uses: actions/checkout@<full-sha>`.

## Audit Before Every Commit

Run the appropriate audit command and fix critical/high vulnerabilities before committing:

- **Node.js:** `npm audit` or `yarn audit`. Use `npm audit --omit=dev` to focus on production dependencies.
- **Python:** `pip audit` (install via `pip install pip-audit`). Or `safety check` for the Safety DB.
- **Go:** `govulncheck ./...` (install via `go install golang.org/x/vuln/cmd/govulncheck@latest`).
- **Rust:** `cargo audit`.
- **Ruby:** `bundle audit`.

**Policy:** No CRITICAL vulnerabilities in production code. HIGH vulnerabilities must be triaged within 7 days. If a fix is not available, evaluate whether the dependency can be replaced or the vulnerable code path is reachable.

## Typosquatting Awareness

Typosquatting is when an attacker publishes a malicious package with a name similar to a popular one (e.g., `lodash` vs `lodassh`, `requests` vs `requets`).

- **Double-check package names** before installing. Copy-paste from the official documentation, not from memory.
- **Verify publisher identity.** On npm, check the package page for the publisher name, download count, and GitHub link. A package with 12 downloads and no GitHub repo is suspicious.
- **Watch for name variations:** `_` vs `-`, missing letters, extra letters, different letter order.
- **Use namespace/scoped packages** where available (`@angular/core` is harder to typosquat than `angular-core`).

## Minimal Dependency Philosophy

Before adding a dependency, answer these questions:

1. **Can I write this in 50 lines or fewer?** If yes, write it yourself. The maintenance cost of 50 lines of your own code is lower than the supply chain risk of an external dependency.
2. **How many transitive dependencies does it bring?** Run `npm ls <package>` or check on bundlephobia.com. A package that pulls in 200 transitive dependencies expands your attack surface 200x.
3. **Is it actively maintained?** Check the last commit date, open issue count, and response time. An unmaintained package will not receive security patches.
4. **Is there a smaller alternative?** Prefer focused packages over kitchen-sink frameworks. `date-fns` over `moment`. `got` over `request`.

## Build Reproducibility

- **Deterministic builds** mean the same source always produces the same artifact. This makes it possible to verify that a build was not tampered with.
- **Avoid post-install scripts** (`postinstall` in package.json). These execute arbitrary code during `npm install` and are a common attack vector. Use `--ignore-scripts` where possible, and explicitly allow only trusted scripts.
- **Vendor dependencies** for high-security projects. Commit the entire `vendor/` or `node_modules/` directory to make builds fully reproducible without any network access.

## CI/CD Pipeline Security

- **Never run arbitrary code from pull requests** without review. A malicious PR can modify CI scripts to exfiltrate secrets. Use `pull_request_target` carefully in GitHub Actions -- it runs with write access.
- **Pin CI dependencies.** Your CI pipeline is a build environment. Apply the same pinning and auditing rules as your application.
- **Restrict secret access.** Not every CI job needs every secret. Use scoped secrets and environment-level access controls.
- **Review third-party CI actions/plugins.** A CI action is code that runs with your repository's secrets. Audit it before using it.

## SBOM Generation

Generate a Software Bill of Materials (SBOM) for every release:

- **Tools:** `syft` (Anchore), `cyclonedx-cli`, `spdx-sbom-generator`, or `npm sbom` (Node.js 19+).
- **Formats:** CycloneDX or SPDX. Both are industry standards.
- **When:** Generate at build time in CI. Attach to the release artifact.
- **Why:** SBOMs enable downstream consumers to check if they are affected by newly discovered vulnerabilities. They are increasingly required by regulations (US Executive Order 14028, EU CRA).

## License Compliance

- **Scan licenses** of all dependencies. Use `license-checker` (npm), `pip-licenses` (Python), or `go-licenses` (Go).
- **Define an allowlist** of acceptable licenses: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC.
- **Flag copyleft licenses** (GPL, AGPL, LGPL) for legal review before inclusion. Copyleft licenses may impose obligations on your distribution.
- **Reject unknown or missing licenses.** A package with no license is not permissively licensed -- it is all rights reserved.

## Package Provenance Verification

- **npm provenance:** npm supports package provenance attestations (via Sigstore). Check for the provenance badge on npmjs.com. It links the published package to a specific CI build and source commit.
- **Sigstore for containers:** Use `cosign` to verify signed container images.
- **Go module checksums:** The Go checksum database (`sum.golang.org`) provides a transparency log for module checksums. `go mod verify` checks local modules against it.
- **Python:** Use `--require-hashes` with pip to verify downloaded package hashes against known-good values.
