---
name: secure-sdlc-supply-chain
description: Secure development lifecycle and software supply chain practice — NIST SSDF SP 800-218, SLSA build provenance, SBOM, dependency and secret scanning, vulnerability management SLAs and penetration testing. Use when assessing how software is built and released rather than what it does at runtime.
---

# Secure SDLC and supply chain

Registry: `NIST-SSDF`, `SLSA`, `OWASP-TOP10` (A03:2025), `VENDOR-GITHUB-ACTIONS`.

This is the practice layer behind the `cicd-compliance` surface audit. A03:2025 Software Supply
Chain Failures entering the OWASP Top 10 confirms what the frameworks already said: the pipeline is
part of the attack surface.

## NIST SSDF (SP 800-218 v1.1) — the backbone

Four practice groups. Use these as the section headings for any SDLC assessment:

| Group | Practice | Concretely, for this repo |
|---|---|---|
| **PO** Prepare the Organization | Define security requirements, roles, toolchains, criteria | Is there a written security requirement set (ASVS L2) and an owner? |
| **PS** Protect the Software | Protect code from tampering, provide integrity verification, archive releases | Branch protection, signed commits/tags, image signing, release retention |
| **PW** Produce Well-Secured Software | Design review, threat modelling, reuse of vetted components, code review, testing, secure defaults | Peer review requirement, SAST, dependency policy, secure defaults in generated CRUD |
| **RV** Respond to Vulnerabilities | Identify, assess, remediate, and do root-cause analysis | Scanning cadence, SLA by severity, a disclosure path, post-incident learning |

## SLSA build levels

| Level | Requirement | Realistic here |
|---|---|---|
| Build L1 | Provenance exists and is available | Cheap — start here |
| Build L2 | Signed provenance from a hosted build service | GitHub-hosted runners + signing |
| Build L3 | Hardened build platform, non-falsifiable provenance | GitHub OIDC + Sigstore/cosign, in-toto attestations, verified at deploy |

The deploy-time verification step is the one people forget. Provenance nobody checks is a file.

## The concrete gate list

Grade each as its own row in the CI/CD grid — never as one "we have scanning" row:

1. **Dependency scanning** with a policy on what blocks a merge (Dependabot, or equivalent)
2. **SBOM generation** per image, retained and associated with the release tag
3. **Secret scanning** on the repo *and* in CI, with push protection
4. **SAST** on application code
5. **Container image scanning** before push and in the registry
6. **IaC / workflow linting** where infrastructure is defined
7. **Action pinning by commit SHA** for third-party actions
8. **Least-privilege tokens** — `permissions:` blocks in workflows, OIDC instead of stored cloud credentials
9. **Reproducible builds** — pinned base images by digest, `npm ci` with a committed lockfile
   (note `frontend/Dockerfile` uses `npm install --legacy-peer-deps` and `CI=false`, which is
   neither reproducible nor fail-fast)
10. **Provenance/attestation** generated and verified
11. **Test and lint gates** required before deploy
12. **Environment protection** with approval for production

## Vulnerability management

A policy is required by nearly every framework here (`SA-NCA-ECC`, `SOC2-TSC` CC7, `PCI-DSS` 6/11,
`ISO-27002`). It needs: sources of vulnerability intelligence, an assessment step, **remediation SLAs
by severity**, an exception process with expiry, and evidence that the SLAs are met. Scanning
without SLAs produces a dashboard, not a control.

## Penetration testing

Required or expected by `SA-NCA-ECC`, `PCI-DSS` (where in scope), `SOC2-TSC` and enterprise buyers.
Define: scope (all three surfaces), cadence (at minimum annual and after material change),
independence of the tester, and a tracked remediation and retest loop. An untracked pentest report
is a document, not a control.

## AI in the pipeline

`backend/.github/workflows/` contains `ai-agent.yml`, `ai-handler.yml` and `ai-review.yml`. An AI
workflow with repository write access is a supply-chain actor: assess trigger sources, whether
untrusted text can reach the prompt, token scope, and whether it can merge or deploy. Route to
`ai-governance` and `OWASP-LLM-TOP10` (Agentic).
