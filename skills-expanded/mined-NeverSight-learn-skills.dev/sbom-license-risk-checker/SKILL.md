---
name: sbom-license-risk-checker
description: Vendor-neutral skill to check a CycloneDX SBOM for license policy compliance and emit a risk report.
---

## When to invoke
- You have a CycloneDX SBOM and need to flag packages with disallowed or unknown licenses.
- You want an audit-friendly report that can be used in CI.

## Inputs needed
- `--sbom`: path to a CycloneDX JSON SBOM.
- `--policy`: path to a JSON license policy containing:
  - `allow`: list of allowed SPDX identifiers
  - `deny`: list of denied SPDX identifiers
  - `warn`: list of licenses that require review

## Workflow
1. Load SBOM JSON.
2. Iterate components and extract license identifiers (best-effort).
3. Classify each component:
   - `allowed`, `warn`, `denied`, or `unknown`
4. Emit JSON report with summary counts and per-component findings.

## Output format
JSON:
- `summary`
- `findings`: list of `{name, version, purl, licenses, classification, rationale}`

## Guardrails
- If multiple licenses are present, choose the most restrictive classification (deny > warn > allow > unknown).
- Do not guess licenses when missing; mark as `unknown`.
- Keep results deterministic.

## Reference code
`check_sbom_licenses.py`
