---
name: supply-chain
description: Software supply-chain defense — SBOM generation (CycloneDX/SPDX), SLSA build provenance, artifact signing with sigstore/cosign, dependency-confusion and typosquat defense, and consumer-side verification of what you pull in.
---

# Supply Chain Defense

## When to use

This skill covers both producer and consumer sides of the software supply chain: what you build, how you prove that you built it, how you sign it, and how you verify what you consume. It complements `cve-triage` (triage of what is in your SBOM) and is invoked by `cicd-hardening` for the build-provenance side.

Triggers on:

- A question like "generate an SBOM", "set up SLSA", "how do I sign our artifacts", "are we vulnerable to dependency confusion", "cosign verify".
- A compliance question from `iso27001`, `nis2`, `dora`, or `soc2` about provenance or SBOM delivery.
- A build pipeline that publishes artifacts (npm package, PyPI wheel, Docker image, Helm chart, GitHub release binary) and lacks provenance.
- An incident where a compromised dependency or typosquat has been found (XZ-style, event-stream-style).
- A government customer demanding SSDF attestation or SBOM delivery (US Executive Order 14028, EU Cyber Resilience Act).

### When NOT (handoff)

- Per-CVE triage from the SBOM → `cve-triage`. This skill produces the SBOM; that one weighs it.
- Secrets in artifacts or in build output → `secrets-scanner`.
- CI-pipeline safety itself (pinned actions, OIDC, runner isolation) → `cicd-hardening`. Overlap on SLSA provenance is intentionally cross-referenced there.
- Container base-image hardening → `container-hardening`. Image signing is here (sigstore/cosign), image content is there.
- Code-pattern questions about dep hygiene (pinning, lockfiles) → `secure-coding` phase 6.

## Approach

Six phases. Phases 1 and 2 are producer-side (what you build and declare), phase 3 is the signing layer, phases 4 and 5 are consumer-side (what you bring in), phase 6 is verification.

### 1. SBOM generation

A Software Bill of Materials is the ingredient list of your artifact. Two common formats, both machine-readable:

- **CycloneDX** (OWASP project, JSON/XML/protobuf). Stronger security focus, native VEX integration, pURL-based identification. Default choice for security use cases.
- **SPDX** (Linux Foundation, tagValue/JSON/YAML/RDF). Stronger in license tracking, broader adoption in enterprise compliance. Default choice if license compliance is also a goal.

Generation tools:

- **syft** (Anchore, Apache-2). Scans filesystems, images, lockfiles. Can output both formats. Default choice for containers and filesystem artifacts.
- **cdxgen** (OWASP, Apache-2). CycloneDX-native, broader ecosystem coverage incl. Java/Node/Python/Go/Rust.
- **cyclonedx-bom-<lang>**: language-specific CLIs (`cyclonedx-bom` for Node, `cyclonedx-python-lib` for Python, `cyclonedx-maven-plugin` for Maven).
- **Microsoft sbom-tool** (MIT). Integrates with Azure DevOps and GitHub.

Generate at build time, not after the fact. A post-hoc SBOM on an already-deployed artifact misses transitive resolution moments and is by definition an approximation.

```bash
# syft — container-image SBOM in CycloneDX
syft <image>:<tag> -o cyclonedx-json > sbom.cdx.json

# syft — filesystem (e.g. git clone)
syft dir:. -o spdx-json > sbom.spdx.json

# cdxgen — Node project, CycloneDX
cdxgen -t js -o bom.json
```

Commit the SBOM or not? For open-source projects: publish with the release artifact (GitHub release asset, sigstore bundle). For closed-source: in an artifact registry next to the artifact. Not in git history; the lockfile is the source of truth.

### 2. Build provenance (SLSA)

SLSA (Supply-chain Levels for Software Artifacts) is a framework that defines four levels of build provenance. Provenance is a signed attestation about how an artifact was built.

- **SLSA Level 1**: build process documented, provenance exists, but is not tamper-proof.
- **SLSA Level 2**: hosted build service, authenticated provenance, source and build are linked.
- **SLSA Level 3**: build is isolated (non-forgeable), source and build are controlled, provenance is cryptographically bound to the artifact contents.
- **SLSA Level 4** (deprecated in v1.0 spec): maximum guarantees. Merged into L3 in the current spec.

Practical route to Level 3:

- **GitHub Actions**: the `slsa-framework/slsa-github-generator` suite delivers L3 provenance out of the box for Go, Node, Python, Docker images. Build job runs in a reusable workflow isolated by GitHub; attestation is signed by the GitHub attestor identity.
- **GitLab CI**: in-toto attestation via Cosign-sign-in-CI. Less ready-made than GitHub but feasible with rekor logging.
- **Self-hosted runners**: L3 becomes harder — the isolation guarantee is then on you. Consider ephemeral runners per build (e.g. via actions-runner-controller).

Provenance is an in-toto statement with predicate type `https://slsa.dev/provenance/v1`. Contents: artifact hash, builder identity, source-repo commit, build parameters. Signing is done via sigstore (phase 3).

### 3. Signing with sigstore

Sigstore is the de facto open-source signing stack since 2021. Three components:

- **cosign** — CLI to sign and verify artifacts. Supports container images, blobs, git commits (via `gitsign`), SBOMs, attestations.
- **Fulcio** — certificate authority issuing short-lived X.509 certs based on OIDC identity. No local key management.
- **Rekor** — transparency log. Every signing action is logged as an immutable entry so verification remains possible later, even if the key is gone.

Keyless signing (recommended default):

```bash
# sign image with OIDC-bound cert, entry in rekor
cosign sign --yes <image>@sha256:<digest>

# sign attestation (SBOM)
cosign attest --yes --predicate sbom.cdx.json --type cyclonedx <image>@sha256:<digest>

# verify signer identity (GitHub Actions example)
cosign verify <image> \
  --certificate-identity-regexp "https://github.com/<org>/<repo>/.github/workflows/.+" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```

Key-based signing (when you do not want or cannot use traceable identity): `cosign generate-key-pair` plus a KMS-backed key (AWS KMS, GCP KMS, Vault). Less operationally fun but fits where OIDC integration is missing.

Gitsign for commit signing: short-lived certs instead of GPG keys that linger for years. No key management, verification against rekor.

### 4. Dependency confusion and typosquat defense

Dependency confusion: an attacker publishes a package under the same name as your internal private package on a public registry with a higher version number. Your build tool resolves the public one and runs attacker code. Known since Alex Birsan's 2021 Medium publication (primary source).

Defenses:

- **Scoped / namespaced packages.** npm `@org/pkg`, Maven groupId. Scoped packages on a public registry are by definition your namespace if you own the scope.
- **Registry config that resolves private-first.** npm `.npmrc` with `@org:registry=https://internal`. pip `index-url` on internal PyPI, `extra-index-url` only as fallback.
- **Lockfile + integrity hash.** `package-lock.json` with SHA-512 integrity, `poetry.lock` with content hashes, Go `go.sum`. Stops the same version with different contents from being accepted.
- **Mirror / proxy registry.** Nexus, Artifactory, Verdaccio, GitLab Package Registry. Internal-first, caches public deps, blocks unknowns.
- **Publish prevention for internal names.** Register your internal names on public registries as placeholders (with minimal/placeholder version) to prevent namespace squatting.

Typosquat:

- **Look at new dependencies critically.** Author, age (how long has the package existed?), download count, reverse deps. Tools: `npm-typo-check`, `socket.dev`, Snyk Advisor.
- **Deps on install.** Disable post-install scripts where possible (`npm install --ignore-scripts`). Many supply-chain attacks trigger on install.

### 5. Consumer-side verification

Verify what you bring in before you use it.

- **Container image signatures.** Kubernetes admission controller (Kyverno, Sigstore policy-controller) that rejects unsigned or non-trusted-signer images. References in `k8s-security`.
- **Package-level attestations**: npm has supported provenance via sigstore since 2023; PyPI has trusted-publishing. On consumption: verify the attestation at install time in CI, not only on developer machines.
- **Verification policies**: Cosign `policy` with allowlist of permitted signers and attestation predicates. Match on builder identity (GitHub Actions workflow path), not on branch name (which is changeable).

### 6. Verification-loop

Layer 1: scope (do all artifacts published by the org have an SBOM and an attestation? are all consumption paths verifying?), assumptions ("we use keyless signing" only if OIDC is actually wired up), gaps (test artifacts and internal tools are often forgotten — are they intentionally excluded or just missed?), consistency (SBOM format consistent across all artifacts?).

Layer 2: SLSA-level claims backed by a concrete build setup, no hand-waving toward "we are at L3", CVEs or incidents you mention (XZ, event-stream, SolarWinds) verified for factual detail, cosign command examples checked for syntax against the current version.

## Output

Two modes depending on the trigger.

**Setup mode** (new or missing supply-chain discipline):

```
Supply-chain setup — <project/org>
Current state: <SBOM: yes/no | Signing: yes/no | SLSA level: L0–L3>

Delivered:
- SBOM generation: <tool + format + build step>
- Provenance: <SLSA-level target + toolchain>
- Signing: <cosign keyless via OIDC | KMS-backed | gitsign for commits>
- Dep-confusion defense: <scoped packages | registry config | mirror>
- Consumer verification: <policy-controller | cosign verify in CI>

To test:
1. Build artifact → SBOM exists and is populated
2. Build artifact → attestation findable in rekor
3. Verify command returns success on signed, fails on unsigned

Verification-loop: ...
```

**Incident/audit mode** (audit existing pipeline):

```
Supply-chain audit — <scope>
Findings:
- SBOM: <present for all artifacts | missing for X>
- Provenance: <effective SLSA level | claim vs. reality>
- Signing: <coverage%, unsigned artifacts listed>
- Dep-confusion: <namespace registration, registry config, mirror>
- Consumer verify: <enforcement points and gaps>

Per gap:
- What is missing
- Concrete remediation
- Priority (blocker for compliance | standard sprint item)

Verification-loop: ...
```

No report that says "we are at SLSA L3" without having seen the actual build setup. Phase 2 demands evidence.

## References

- SLSA framework — [https://slsa.dev/](https://slsa.dev/). v1.0 specification with L1–L3 definitions.
- CycloneDX — [https://cyclonedx.org/](https://cyclonedx.org/). OWASP project, SBOM format + VEX integration.
- SPDX — [https://spdx.dev/](https://spdx.dev/). Linux Foundation, ISO/IEC 5962:2021.
- Sigstore — [https://www.sigstore.dev/](https://www.sigstore.dev/). Cosign, Fulcio, Rekor, Gitsign.
- in-toto — [https://in-toto.io/](https://in-toto.io/). Attestation framework underlying SLSA provenance.
- CISA SBOM page — [https://www.cisa.gov/sbom](https://www.cisa.gov/sbom). Guidance + minimum-format definition.
- US Executive Order 14028 — [https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/](https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/). Original mandate for SBOM delivery in federal procurement.
- EU Cyber Resilience Act — [https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act). EU equivalent with SBOM obligations for digital products.
- NIST SP 800-218 (SSDF) — [https://csrc.nist.gov/pubs/sp/800/218/final](https://csrc.nist.gov/pubs/sp/800/218/final). Secure Software Development Framework, supply-chain interface.
- OpenSSF Best Practices — [https://www.bestpractices.dev/](https://www.bestpractices.dev/). OpenSSF badge, touches supply-chain discipline.
- Alex Birsan — "Dependency Confusion" (2021). [https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610). Original publication on the attack class.

## Categories

- appsec
