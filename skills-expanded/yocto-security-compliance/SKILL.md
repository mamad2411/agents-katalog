---
name: yocto-security-compliance
description: Official-doc-first Yocto security, CVE, license, and SBOM compliance support for AI coding agents. Use when investigating cve-check results, vulnerable packages, security patch backports, LICENSE and LIC_FILES_CHKSUM issues, license manifests, SPDX or SBOM output, source provenance, reproducibility concerns, package audit findings, or compliance-sensitive Yocto/OpenEmbedded image and recipe changes.
---

# Yocto Security Compliance

## Core Workflow

1. Identify Yocto release, image, recipe, package names, source version, and patch state.
2. Verify current vulnerability/security facts online when the user asks about CVEs, fixes, exploitability, support status, or latest security data.
3. Distinguish recipe name, source package name, runtime package name, binary package name, and CVE product/vendor names.
4. Inspect upstream source, local patches, license files, package manifests, SPDX/SBOM output, and `cve-check` output before changing metadata.
5. Prefer recipe upgrades or patch backports over blanket ignores.
6. Document compliance decisions in the layer or release notes where the project expects them.

Use [yocto_security_doc_router.py](scripts/yocto_security_doc_router.py) with a topic name for official documentation links.

## References

- [cve-workflow.md](references/cve-workflow.md): CVE investigation, patch/backport, and false-positive handling.
- [license-compliance.md](references/license-compliance.md): `LICENSE`, `LIC_FILES_CHKSUM`, manifests, and incompatible license policy.
- [sbom-spdx-workflow.md](references/sbom-spdx-workflow.md): SPDX/SBOM generation, provenance, and release review.

## Guardrails

- Do not suppress CVE, license, or QA findings without documenting the exact reason.
- Do not change `LICENSE`, `LIC_FILES_CHKSUM`, or CVE status fields without inspecting upstream source, patches, and package output.
- Do not treat build-time package names, runtime package names, source recipe names, and CVE product names as interchangeable.
- Do not put signing keys, embargoed details, or private vulnerability data into public layers or logs.
