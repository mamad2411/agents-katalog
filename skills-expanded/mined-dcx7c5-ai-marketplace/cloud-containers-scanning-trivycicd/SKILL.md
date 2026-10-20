---
name: cloud-containers-scanning-trivycicd
description: "Cloud Containers Scanning Trivycicd."
domain: cybersecurity
---

|
| CVE | Common Vulnerabilities and Exposures — standardized identifiers for publicly known security vulnerabilities |
| Vulnerability DB | Trivy's regularly updated database aggregating CVE data from NVD, vendor advisories, and language-specific sources |
| Misconfiguration | Security-relevant configuration issue in Dockerfiles, Kubernetes manifests, or IaC templates |
| SBOM | Software Bill of Materials — complete inventory of all components and dependencies in a container image |
| Ignore Unfixed | Flag to skip CVEs without available patches, reducing noise from vulnerabilities with no actionable fix |
| VEX | Vulnerability Exploitability eXchange — machine-readable statements about whether a vulnerability is exploitable in context |
| Exit Code | Non-zero return code from Trivy when findings exceed the severity threshold, used to fail CI/CD pipelines |

## Tools & Systems

- **Trivy**: Open-source vulnerability scanner by Aqua Security supporting images, filesystems, repos, and IaC
- **trivy-action**: Official GitHub Action for running Trivy scans in GitHub Actions workflows
- **Trivy Operator**: Kubernetes operator that continuously scans cluster workloads with Trivy
- **Grype**: Alternative image scanner by Anchore for comparison and validation of scan results
- **Harbor**: Container registry with built-in Trivy integration for automatic image scanning on push

## Common Scenarios

### Scenario: Multi-Stage Build with Separate Scan and Push

**Context**: A team builds multi-stage Docker images and needs to scan the final production image before pushing to ECR, while also scanning the build stage for supply chain risks.

**Approach**:
1. Build the Docker image with `--target production` for the final stage
2. Run Trivy with `--severity CRITICAL,HIGH --exit-code 1 --ignore-unfixed` to block on exploitable issues
3. Generate an SBOM in CycloneDX format and store as a build artifact
4. Upload SARIF results to GitHub Security tab for visibility
5. Only push to ECR if the Trivy scan exits with code 0
6. Tag the pushed image with the scan timestamp and Trivy DB version for audit traceability

**Pitfalls**: Scanning only the final stage misses vulnerable packages that were present in build stages and may have influenced the build. Run `trivy fs` on the build context separately. Caching the Trivy DB too aggressively (weekly) means newly published CVEs take days to appear in scans.

## Output Format

```
Trivy Container Scan Report
=============================
Image: app:a1b2c3d4
Base Image: python:3.12-slim-bookworm
Scan Date: 2026-02-23
DB Version: 2026-02-23T00:15:00Z

VULNERABILITY SUMMARY:
  Total: 47
  Critical: 2
  High: 5
  Medium: 18
  Low: 22
  Unfixed: 8 (excluded from gate)

CRITICAL FINDINGS:
  CVE-2025-12345  libssl3    3.0.11-1  3.0.13-1  OpenSSL buffer overflow
  CVE-2025-67890  curl       7.88.1-10 7.88.1-12 curl HSTS bypass

HIGH FINDINGS:
  CVE-2025-11111  zlib1g     1.2.13    1.2.13.1  zlib heap buffer overflow
  CVE-2025-22222  python3.12 3.12.1    3.12.3    CPython path traversal
  CVE-2025-33333  requests   2.31.0    2.32.0    requests SSRF in redirects

MISCONFIGURATION:
  DS002  [HIGH]   Dockerfile: USER instruction not set (running as root)
  DS026  [MEDIUM] Dockerfile: No HEALTHCHECK defined

QUALITY GATE: FAILED (2 Critical, 5 High findings)
```
