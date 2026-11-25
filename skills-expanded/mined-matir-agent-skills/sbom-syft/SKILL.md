---
name: sbom-syft
description: Software Bill of Materials (SBOM) generation using Syft for container images, filesystems, and archives.
metadata:
  version: 0.2.0
  category: secsdlc
---
# Syft SBOM Generator

## Quick Start
```bash
# Generate a CycloneDX JSON SBOM for a container image
syft <image-name:tag> -o cyclonedx-json=sbom.json
```

## Workflow
1. **Target Identification**: Identify the container image, directory, or archive to scan.
2. **SBOM Generation**: Run Syft with the desired output format (e.g., `cyclonedx-json`, `spdx-json`).
3. **Review Finding**: Inspect the generated SBOM for accuracy and completeness of detected packages and ecosystems.
4. **Vulnerability Analysis**: (Optional) Use a tool like Grype to scan the generated SBOM for known vulnerabilities.
5. **Attestation & Provenance**: (Optional) Sign the SBOM using `cosign` to provide verifiable software provenance.

## Rules & Constraints
- **RULE-1**: Use standard SBOM formats like CycloneDX or SPDX for interoperability with other security tools.
- **RULE-2**: For container images, use `--scope all-layers` when deep inspection of all image layers is required.
- **RULE-3**: Do not rely on default catalogers for proprietary or non-standard package managers; use custom configurations if needed.

## When to Use
- Generating SBOMs for container images or local filesystems.
- Tracking software dependencies for vulnerability scanning and license compliance.
- Establishing supply chain security by creating signed SBOM attestations.

## When NOT to Use
- Real-time monitoring of installed packages on a running system (use OS-native package managers).
- Identifying malware or malicious behavior within files (use anti-virus or EDR tools).

## References
- [Skill Manual](references/sbom-syft-manual.md)
- [Syft Official Repo](https://github.com/anchore/syft)
