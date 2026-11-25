# Vulnerability Scanning & Assessment Skill

## Key Activation Triggers

The skill activates when users request CVE scanning, dependency audits (Python/Node/Go/Java/Rust), configuration reviews (nginx/SSH/Docker/Kubernetes), or CVSS scoring analysis.

## Core Functions

**Dependency Auditing:** Claude analyzes package files to extract versions, query vulnerability databases, calculate CVSS scores, and identify minimum safe versions. Supports pip, npm, Maven, Cargo, Bundler, and Composer ecosystems.

**Configuration Security:** Direct analysis of configuration files against checklists—nginx requires secure TLS protocols and security headers; SSH requires key-only auth and disabled root login; Docker/Kubernetes require non-root users and privilege restriction.

**CVSS v3.1 Scoring:** Calculates severity from vector strings using eight metrics (Attack Vector, Complexity, Privileges Required, User Interaction, Scope, Confidentiality, Integrity, Availability) mapped to ranges from Low (0.1–3.9) through Critical (9.0–10.0).

**Network Scanning:** Integrates Nmap output to map service versions to CVEs, identify misconfigurations, and recommend NSE scripts for deeper assessment.

**Report Generation:** Produces structured findings with CVE IDs, CVSS vectors, affected/safe versions, evidence, and remediation steps mapped to compliance frameworks.

## Integration Points

Findings flow downstream to exploit development, blue team defense, and SOC automation workflows.
