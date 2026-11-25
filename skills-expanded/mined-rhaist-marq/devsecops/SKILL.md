---
name: devsecops
description: "Covers operationalizing AppSec in CI/CD without breaking delivery: block vs warn gating, IaC and secrets scanning, policy-as-code, and rolling out supply-chain controls (SBOM, SLSA, Sigstore/cosign signing). Use when the user asks how to add security scanning to a pipeline, gate builds, catch leaked secrets, sign artifacts, or adopt OPA-style policy-as-code. (Choosing scanner types and program maturity: appsec-sdlc.)"
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# DevSecOps

Move security checks into the pipeline **without turning the pipeline into a wall of red**. The art is which gate **blocks** the merge/deploy and which only **warns**: block too much and devs route around you; block too little and nothing changes. This is the build-side enabler for `load_skill appsec-sdlc` (the SDLC/program view).

## Block vs. warn (the decision that makes or breaks adoption)

**Block** (fail the build): fast, deterministic, low false-positive, unambiguously bad:

- Verified **secret** committed (validated/active credential).
- **Critical/High CVE with a fix available** in a direct dependency (SCA), or a known-exploited (KEV) vuln.
- **IaC misconfig** that exposes data (public bucket, 0.0.0.0/0 to a DB, unencrypted volume, wildcard IAM).
- Failed **artifact signature / provenance** verification at deploy.
- Policy-as-code **hard rule** violation (no privileged containers, image must be signed).

**Warn** (annotate, track, don't block): noisy, slow, or judgement-dependent:

- SAST findings below high confidence / needing triage.
- Transitive CVEs with **no fix** yet (track + SLA, don't block delivery).
- License/style/quality lint.
- New findings on **legacy** code (use a baseline/diff so only _new_ issues gate).
  Rules: gate on **diff/new** not the whole backlog; make every block **actionable** (what + how to fix); give a documented **break-glass** override that's logged; keep critical gates **fast** (<5 min) so they run on every PR.

## IaC scanning

- Scan Terraform/CloudFormation/K8s/Helm/Dockerfiles pre-apply: **Checkov, tfsec/Trivy, KICS, Terrascan**. Run on the **plan** where possible (real values).
- Block the data-exposure / wide-open-network / unencrypted set; warn the rest. Tune out noise per-repo or devs disable it.

## Secrets management & detection

- **Don't store secrets in repos/CI vars**: use a vault / cloud secrets manager + short-lived **OIDC-federated** cloud creds (no long-lived keys in CI).
- **Detect**: `gitleaks` / `trufflehog` (validates whether a secret is _live_; run them in your own CI or workstation) in pre-commit **and** CI; enable platform **push protection** (GitHub/GitLab secret scanning) to stop the commit at the door.
- A leaked secret = **rotate first**, then remove from history. Scrubbing git history without rotating is theater. (marq's `trufflehog` tool can scan public git hosts (GitHub, GitLab, Bitbucket, Codeberg) without verifying; see `load_skill recon-footprint`.)

## SBOM + supply-chain (SLSA)

- **Generate an SBOM per build** and store it as an artifact. Formats: **CycloneDX** (OWASP, AppSec/vuln-focused; at **1.7**, Oct 2025, ECMA-424 2nd ed.) and **SPDX** (Linux Foundation, license-focused; **3.0.1**, much of the field still emits 2.3). Pick one canonical, convert as needed. Tools: Syft, Trivy, cdxgen. verify: https://cyclonedx.org/specification/overview/
- Feed the SBOM into continuous vuln matching (Grype/Trivy/Dependency-Track) so a _newly disclosed_ CVE flags against _already-shipped_ artifacts.
- **SLSA** = build-integrity levels (provenance, not vuln-freeness). v1.0 → **v1.1 approved ~Apr 2025**; **v1.2 (Nov 2025) adds a Source track**. Build track: **L0** none → **L1** provenance exists → **L2** signed provenance from a hosted build → **L3** hardened, isolated builder, non-falsifiable provenance. Target **L2 to L3** for anything you ship externally. Self-attestation is still the weak link; verify provenance, don't trust a logo. verify: https://slsa.dev/spec/v1.2/

## Signing (Sigstore / cosign)

- **Sign artifacts + attestations** so consumers verify origin. **Sigstore cosign** keyless signing is the default path: OIDC identity → short-lived **Fulcio** cert → signature logged in **Rekor** transparency log; no long-lived keys to manage.
- Current state: **Cosign v3** (Sigstore bundle format + trusted-root/signing-config on by default; keyless has been default since v2.0), **Rekor v2** GA Oct 2025 but opt-in; the public-good instance keeps Rekor v1 as default (Jun 2026, https://blog.sigstore.dev/rekor-evolution/); major registries adopted Sigstore attestations (PyPI, Maven Central, Homebrew). verify: https://blog.sigstore.dev/cosign-3-0-available/
- **Verify at admission/deploy** (policy-controller / Kyverno verifyImages): signing is pointless if nothing checks the signature. Bind verification to an expected identity, not just "is signed."

## Policy-as-code

- **OPA / Rego + Conftest** to test structured config (Terraform plan JSON, K8s YAML, Dockerfiles, Helm) in CI against org rules; single binary, drops into the pipeline.
- **Kubernetes admission**: **OPA Gatekeeper** (Rego, complex logic/external data) vs **Kyverno** (YAML, K8s-native, simpler, built-in image-verify). Common combo: Kyverno for the K8s-shaped 80%, OPA where you need real logic. verify: https://spacelift.io/blog/policy-as-code-tools
- Policy-as-code is also the **enforcement point** for the block/warn rules above: codify "image must be signed + SLSA L2 + no critical CVE" once, enforce in CI **and** at admission.

## Pairs with

- Program/SDLC view (threat modeling, secure design, AppSec gates by phase): `load_skill appsec-sdlc`.
- Web vuln classes the SAST/DAST gates are catching: injection (SQLi, SSTI), XSS, SSRF, broken access control; see OWASP Top 10.
- Feeding pipeline control state into compliance evidence: `load_skill grc-automation`.
