---
name: cloud-devsecops-scanning
description: "Cloud Devsecops Scanning."
domain: cybersecurity
---

|
| **SAST (Static Application Security Testing)** | Analyzes source code without executing it to find security vulnerabilities; runs fast, catches issues early, but cannot find runtime flaws |
| **DAST (Dynamic Application Security Testing)** | Tests a running application by sending requests and analyzing responses; finds runtime issues but requires a deployed environment |
| **SCA (Software Composition Analysis)** | Scans project dependencies against vulnerability databases (NVD, GitHub Advisory) to find known-vulnerable libraries |
| **SBOM (Software Bill of Materials)** | Machine-readable inventory of all components and dependencies in an application, used for vulnerability tracking and compliance |
| **Shift Left** | Security practice of moving security testing earlier in the SDLC, from post-deployment to pre-commit and CI stages |
| **Security Gate** | A CI/CD pipeline checkpoint that blocks deployment if security scan results exceed defined severity thresholds |
| **Pre-commit Hook** | Local Git hook that runs security checks before code is committed, providing the fastest developer feedback loop |

## Verification

- [ ] Gitleaks blocks commits and PRs containing hardcoded secrets (test with a dummy API key)
- [ ] Semgrep scan runs on every PR and reports findings as annotations or comments
- [ ] Trivy filesystem scan detects a known-vulnerable dependency (test by adding a vulnerable package)
- [ ] Trivy container scan runs successfully against the built Docker image
- [ ] SBOM is generated and stored as a build artifact in CycloneDX or SPDX format
- [ ] OWASP ZAP baseline scan runs against the staging URL without crashing
- [ ] Security gate job blocks merges to main when any scan finds critical/high severity issues
- [ ] Branch protection rules enforce required status checks before merge
- [ ] Pre-commit hooks catch secrets and SAST findings locally before push
- [ ] Developer documentation explains how to interpret scan results and fix common findings
