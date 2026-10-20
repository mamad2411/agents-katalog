---
name: cloud-containers-registry-container
description: "Cloud Containers Registry Container."
domain: cybersecurity
---

|
| Container Image Scanning | Automated analysis of container image layers to identify known vulnerabilities in OS packages and application dependencies |
| Image Signing | Cryptographic attestation that verifies the authenticity and integrity of a container image using Cosign or Notation |
| SBOM | Software Bill of Materials, a comprehensive inventory of software components, libraries, and dependencies in a container image |
| Tag Immutability | Registry setting that prevents overwriting existing image tags, ensuring that a tag always refers to the same image digest |
| Sigstore | Open-source project providing keyless signing, transparency logs, and verification tooling for software supply chain security |
| Image Attestation | Cryptographically signed metadata attached to an image (scan results, SBOM, build provenance) that can be verified before deployment |

## Tools & Systems

- **Trivy**: Comprehensive vulnerability scanner for container images, filesystems, git repos, and Kubernetes resources
- **Grype**: Anchore's vulnerability scanner with broad vulnerability database coverage for container images and SBOMs
- **Cosign**: Sigstore tool for signing, verifying, and attesting container images with key-based or keyless workflows
- **Syft**: SBOM generation tool supporting SPDX and CycloneDX formats for container images and filesystems
- **AWS ECR**: Container registry with built-in scanning, tag immutability, and lifecycle policies

## Common Scenarios

### Scenario: Implementing a Secure Image Promotion Pipeline

**Context**: A development team pushes images to a dev registry without security controls. The security team needs to implement a promotion pipeline that scans, signs, and promotes only approved images to the production registry.

**Approach**:
1. Configure ECR scanning on push for the development repository
2. Add Trivy scanning as a CI/CD gate that blocks images with CRITICAL vulnerabilities
3. Generate SBOMs with Syft and store alongside image scan results
4. Sign approved images with Cosign after scanning passes
5. Configure the production registry to require image signatures for all pushes
6. Set up Kyverno or OPA Gatekeeper in production Kubernetes to verify signatures before pod creation
7. Implement lifecycle policies to clean up untagged and old images in both registries

**Pitfalls**: Vulnerability databases are updated constantly. An image that passes scanning today may have new CRITICAL vulnerabilities discovered tomorrow. Implement continuous scanning of already-deployed images, not just at build time. Image signing keys must be securely stored in KMS or Vault, not in CI/CD environment variables.

## Output Format

```
Container Registry Security Report
=====================================
Registry: 123456789012.dkr.ecr.us-east-1.amazonaws.com
Repositories: 24
Report Date: 2026-02-23

IMAGE INVENTORY:
  Total images: 342
  Images scanned: 298 (87%)
  Images signed: 156 (46%)
  Images with SBOM: 134 (39%)

VULNERABILITY SUMMARY:
  Critical vulnerabilities:    23 (across 8 images)
  High vulnerabilities:       145 (across 34 images)
  Medium vulnerabilities:     456 (across 67 images)
  Images with no vulns:       89

CRITICAL IMAGES REQUIRING REMEDIATION:
  myapp:1.2.3           - 5 CRITICAL (CVE-2026-xxxx in openssl)
  api-gateway:2.0.1     - 3 CRITICAL (CVE-2026-yyyy in log4j)
  worker:latest         - 4 CRITICAL (CVE-2026-zzzz in glibc)

REGISTRY CONFIGURATION:
  Scan on push enabled:     18 / 24 repositories
  Tag immutability:         12 / 24 repositories
  Lifecycle policies:       20 / 24 repositories
  Image signing enforced:    8 / 24 repositories
```
