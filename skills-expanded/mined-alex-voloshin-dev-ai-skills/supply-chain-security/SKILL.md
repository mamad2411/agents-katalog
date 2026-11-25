---
name: supply-chain-security
description: Use this skill when the agent is running a security audit, scanning dependencies, prioritizing CVEs by exploit likelihood, signing release artifacts, generating SBOMs for compliance, or reviewing CI/CD artifact integrity — software supply chain security knowledge covering SBOM generation (Syft, CycloneDX, SPDX), SLSA provenance levels 1 through 4, Sigstore Cosign artifact signing, EPSS exploit-prediction scores, CISA KEV known-exploited catalog, dependency-confusion / typosquatting / lockfile-validation patterns, and EO 14028 and EU Cyber Resilience Act SBOM mandates.
disable-model-invocation: true
---

# Supply Chain Security

Modern security audits must cover the software supply chain end-to-end: what's in the build (SBOM), how it was built (SLSA provenance), whether the artifact is genuine (Cosign signatures), and which known vulnerabilities are actively exploited (EPSS + CISA KEV). This skill is the reference catalog for those tools and standards.

## SBOM — Software Bill of Materials

A Software Bill of Materials enumerates every component (direct + transitive) in a build artifact. Required by US Executive Order 14028 (2021) for federal software and by the EU Cyber Resilience Act (2024+) for software shipped to EU markets.

### Formats

| Format | Maintainer | Use case |
|---|---|---|
| **CycloneDX** | OWASP | Most common in security tooling; rich vulnerability metadata |
| **SPDX** | Linux Foundation | License-focused; ISO/IEC 5962 standard |
| **SWID** | NIST/ISO | Installed-software tagging; less common in CI |

### Tooling

- **Syft** (Anchore) — generate SBOM from source, container, or filesystem:
  ```bash
  syft <repo> -o cyclonedx-json
  syft <image>:<tag> -o spdx-json
  ```
  https://github.com/anchore/syft
- **Grype** (Anchore) — consume SBOM, match against vuln databases:
  ```bash
  grype sbom:./sbom.json
  ```
  Natively consumes EPSS + KEV for prioritization. https://github.com/anchore/grype
- **Trivy** (Aqua) — SBOM + container + IaC scanning in one CLI: https://trivy.dev
- **Dependency-Track** (OWASP) — continuous SBOM monitoring + vulnerability triage server: https://dependencytrack.org
- **GUAC** (OpenSSF) — graph SBOMs + attestations + vulnerabilities; query supply-chain risk: https://docs.guac.sh

## SLSA — Supply-chain Levels for Software Artifacts

SLSA (pronounced "salsa") defines build-integrity levels. Maintained by OpenSSF. Reference: https://slsa.dev

| Level | Provenance | Build platform requirements | Practical use |
|---|---|---|---|
| **L1** | Provenance exists, may be unsigned | Documented build process | Minimum hygiene; trivially forgeable |
| **L2** | Signed provenance from hosted build service | Hosted build (GitHub Actions, GitLab CI) | **Practical baseline** for most projects |
| **L3** | Build is hardened against tampering | Isolated, ephemeral build envs; non-falsifiable provenance | Required for high-trust artifacts (OS distros, security tools) |
| **L4** | Two-party review, hermetic + reproducible builds | Hermetic, reproducible, two-person review on build config | Aspirational; rare in practice |

### Reaching SLSA L2

GitHub Actions + [SLSA GitHub Generator](https://github.com/slsa-framework/slsa-github-generator) achieves L2 with minimal config. The generator emits an [in-toto attestation](https://in-toto.io) signed via Sigstore.

## Sigstore Cosign — artifact signing

Sigstore provides keyless signing of build artifacts using OIDC identity (no long-lived keys to rotate). https://www.sigstore.dev

```bash
# Sign a release blob
cosign sign-blob --bundle release.sig dist/app-1.0.0.tar.gz

# Sign a container image
cosign sign ghcr.io/org/app:1.0.0

# Verify at deploy time
cosign verify-attestation --type slsaprovenance ghcr.io/org/app:1.0.0
```

Pair with admission control (Kyverno, Gatekeeper) in Kubernetes to reject unsigned images at deploy.

## EPSS — Exploit Prediction Scoring System

EPSS is a 0.0–1.0 probability that a CVE will be exploited in the next 30 days. Maintained by FIRST.org. Free API: https://api.first.org/data/v1/epss

- **EPSS ≥ 0.5** = high near-term exploitation likelihood
- **EPSS ≥ 0.1** = elevated; investigate
- Useful for prioritizing thousands of "medium" CVSS findings down to the few that actually matter

`grype` consumes EPSS natively (`grype --by-cve --add-cpes-if-none`).

## CISA KEV — Known Exploited Vulnerabilities

The CISA Known Exploited Vulnerabilities catalog is a curated list of CVEs confirmed exploited in the wild. https://www.cisa.gov/known-exploited-vulnerabilities-catalog

- KEV-listed CVEs are **confirmed in-the-wild** (not predicted)
- US federal agencies must patch within mandated deadlines
- Use as a "must fix before merge" gate in CI

EPSS and KEV are complementary: KEV is ground truth for past/active exploitation; EPSS is forward-looking probability.

## Prioritization rule of thumb

A practical CVE triage policy:

| Signal | Action |
|---|---|
| CVE in CISA KEV | Must fix before merge |
| EPSS ≥ 0.5 | Must fix before merge |
| EPSS ≥ 0.1 and CVSS ≥ 7 | Fix this sprint |
| EPSS < 0.1 and CVSS < 7 | Background queue |
| No fix available | Document in REMEDIATION-PLAN with risk acceptance + escalation deadline |

## Dependency-confusion, typosquatting, lockfile attacks

### Dependency confusion

Attacker publishes a package with the same name as an internal private package to a public registry (npm, PyPI). The default resolution preferring the higher version number pulls the malicious public package into the build.

**Mitigation:**
- Scoped/namespaced internal packages (`@org/internal-lib`)
- Explicit registry config per scope in `.npmrc` / `pip.conf`
- Reserve internal package names on public registries

### Typosquatting

Attacker publishes `reqeusts`, `colourama`, `lodahs`. Developer typos the install command; malicious package runs.

**Mitigation:**
- Lockfile-pinned installs (`npm ci`, `pip install -r requirements.txt --require-hashes`)
- Package allowlists in CI
- Pre-install hooks that verify package names against an allowlist

### Lockfile validation

A lockfile (`package-lock.json`, `poetry.lock`, `Cargo.lock`, `go.sum`) pins exact versions and hashes. CI must:
- Reject PRs that modify the lockfile without modifying the manifest
- Enforce hash verification (`npm ci`, `pip install --require-hashes`, `cargo --frozen`)
- Audit lockfile changes for unexpected transitive additions

## Regulatory landscape

- **EO 14028** (US, 2021) — mandates SBOMs for software shipped to US federal government
- **EU Cyber Resilience Act** (2024+) — mandates SBOMs and vulnerability disclosure for software in EU markets
- **NIST SSDF** (SP 800-218) — Secure Software Development Framework, references SBOM + SLSA
- **OpenSSF Scorecard** — automated checks for repo security posture: https://securityscorecards.dev

## When this applies

| Workflow | Apply this knowledge |
|---|---|
| `/security-audit` | Generate SBOM, run SCA, prioritize via EPSS+KEV, report supply-chain posture (signed artifacts? SLSA level?) |
| `/code-review` (security gate) | Flag lockfile changes that look suspicious; flag new dependencies not pinned to a hash |
| `/security-scan` | Primary surface — run Syft + Grype, gate on KEV + EPSS thresholds |
| `/release` / `/deploy-production` | Sign release artifacts with Cosign; emit SLSA provenance; verify signatures at deploy |

## Integration

- **Used by**: `/security-audit`, `/security-scan`, `/code-review`, `/release`, `/deploy-production`
- **Companion knowledge**: `@owasp-coverage` (A06 vulnerable components, A08 integrity failures, LLM03 model supply chain)
- **External references**:
  - SLSA: https://slsa.dev
  - Sigstore: https://www.sigstore.dev
  - CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
  - EPSS: https://www.first.org/epss/
  - CycloneDX: https://cyclonedx.org
  - SPDX: https://spdx.dev
  - in-toto attestations: https://in-toto.io
  - OpenSSF Scorecard: https://securityscorecards.dev
