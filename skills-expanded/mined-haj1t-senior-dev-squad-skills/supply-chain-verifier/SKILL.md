---
name: supply-chain-verifier
description: "Dependency security scanning, provenance verification, license compliance, package.json, requirements.txt, go.mod, Cargo.toml. Use when auditing supply-chain risk."
---

# Supply Chain Verifier

## Overview

This skill audits software supply chain security via dependency vulnerability scans, provenance verification, and licensing checks. It parses package manifests (e.g., `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`) to discover known vulnerabilities (CVEs), verifies that package registries (npm, PyPI, crates.io) map to trusted repository source origins (GitHub, GitLab), audits nested transitive dependencies, and checks licenses (MIT, GPL, AGPL, Apache 2.0, BSD) for compliance. The goal is to answer: "Is this dependency secure and compliant across CVEs, provenance, and license types?"

**Core principle:** If there is no verified source origin, there is no trusted dependency. Every dependency is treated as untrusted until validated.

## The Iron Law

```
NO DEPENDENCY CAN BE MERGED OR DEPLOYED TO PRODUCTION WITHOUT UNDERGOING CVE SCANNING, PROVENANCE VALIDATION, AND LICENSE COMPLIANCE CHECKS.
```

Omitting any of these three checks leaves the system vulnerable to supply chain exploits.

## When to Use

**Use this when:**
- A new dependency is proposed in a pull request.
- Performing periodic, automated audits of a project's dependency tree.
- A new CVE is disclosed, and you must verify whether your projects are affected.
- Auditing dependency licenses prior to releases or compliance audits.
- Confirming that registry artifacts (npm/PyPI packages) match their declared source code repositories.
- Scanning transitive, nested dependencies for inherited vulnerabilities.

**Use this ESPECIALLY when:**
- A supply chain security incident is disclosed in the wild (e.g., SolarWinds, event-stream, ua-parser-js) — audit all projects immediately.
- A developer asserts "this is a popular package used by thousands, it is safe" — popularity does not guarantee security.
- Restrictive copyleft licenses (e.g., AGPL) risk leaking into commercial proprietary codebases.

**Don't skip when:**
- A project claims to have zero third-party dependencies — double check the lockfiles.
- The project has automated SBOM generators; execute anomaly scans on these outputs.

## Workflow

Work through the four phases in order. Each gate must be confirmed before proceeding.

**Phase 1 — Dependency Inventory and CVE Scanning.** Locate all package manifests, run language-specific vulnerability scanners (npm audit, pip-audit, govulncheck, cargo audit), prioritize by CVSS severity, and execute context analysis on Critical/High CVEs. See [REFERENCE.md](REFERENCE.md) for per-ecosystem commands, JSON output schema, and severity prioritization guidance.

**Phase 2 — Provenance Validation.** Locate source repositories for each dependency, compare registry artifacts against declared repo states via checksum comparison, and scan for registry anomalies (typosquatting, account takeover, impersonation, astroturfing). See [REFERENCE.md](REFERENCE.md) for verification commands and a worked provenance report example.

**Phase 3 — License Compliance Audit.** Extract license identifiers for all direct and transitive dependencies, categorize by risk tier (Permissive / Copyleft / Restrictive / Unknown), assess compatibility against the project's licensing model, and identify alternatives for incompatible packages. See [REFERENCE.md](REFERENCE.md) for CLI commands, the full license risk table, and a worked compliance report example.

**Phase 4 — Transitive Dependency Auditing and Updates.** Map the full dependency tree, audit nested transitive paths for CVEs, formulate resolution steps (patch/minor/major/override), and assess update impact. See [REFERENCE.md](REFERENCE.md) for tree-mapping commands, override syntax per ecosystem, and a worked dependency-update plan example.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "This is a popular package; it would have been flagged if it had a CVE." — **Popularity does not protect you. event-stream and ua-parser-js had millions of downloads when compromised.**
- "I only need to scan direct dependencies; transitive dependencies are out of scope." — **Most supply chain attacks target nested, transitive paths.**
- "Licenses are standard; there's no need to audit them." — **An unvetted AGPL dependency can require you to open source your proprietary project.**
- "This npm artifact matches the GitHub repository link; it is safe." — **Provenance validation requires verifying integrity hashes, not just metadata strings.**
- "We can't update this package because the breaking changes are too large." — **Running code with unmitigated high CVEs is a higher operational risk than refactoring code.**
- "The npm audit returned green, so the dependencies are secure." — **Audit tools only flag cataloged CVEs; they do not check for typosquatting, zero-days, or provenance anomalies.**

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Did you verify the provenance of this package?" — You skipped registry hash checks.
- "Are the transitive dependencies included in the scan?" — You audited only direct dependencies.
- "Will this AGPL license impact our commercial license model?" — You misclassified copyleft license risks.
- "What is the impact of this CVE? Are we importing the vulnerable class?" — You skipped context impact reviews.
- "The package name in your update plan has a typo." — Pay closer attention to package naming details.
- "Why is this dependency missing from your report?" — Your path configuration was incorrect during tool execution.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Popular libraries are secure by default." | Popular libraries are primary targets for account takeover and typosquatting attacks. |
| "Transitive dependencies are too deep to audit." | 70% of supply chain vulnerabilities enter via nested transitive libraries. Audits are mandatory. |
| "All open-source licenses are permissive." | A single copyleft or restrictive license introduces legal and IP liability risks. |
| "Registry packages are identical to their Git repositories." | Registry uploads can be modified to contain backdoor payloads. Always audit provenance. |
| "Updating dependencies takes too much sprint time." | Exploits for public CVEs are often weaponized within days. Patching must be prioritized. |
| "We don't need SBOMs; our dependency count is low." | SBOMs are standard compliance artifacts required during audits. |

## Related Skills

- **security-reviewer** — Audit how vulnerable code paths in flagged dependencies are executed in application code.
- **mitre-attack-mapper** — Map supply chain vulnerabilities to MITRE ATT&CK techniques (T1195 - Supply Chain Compromise).

## Verification

Before marking complete:

- [ ] Have all package manifests been audited and dependency lists compiled?
- [ ] Has context analysis been executed for all Critical and High CVEs?
- [ ] Is provenance validated for all direct dependencies?
- [ ] Are packages audited for typosquatting, account takeovers, and impersonation?
- [ ] Are all direct and transitive licenses cataloged?
- [ ] Are restrictive copyleft licenses checked against project compliance guidelines?
- [ ] Are action steps defined for packages with undefined (UNKNOWN) licenses?
- [ ] Are dependency resolution overrides written for transitive CVEs?
- [ ] Are breaking change risks reviewed for all package updates?
- [ ] Is the final report structured for both developers and management?
- [ ] Is an SBOM generated in SPDX or CycloneDX format?
