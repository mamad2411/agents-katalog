---
name: supply-chain-audit
audience: team
description: >
  Software supply-chain vulnerability scanning, license-compliance analysis, and CVE correlation
  across NuGet, npm, and pip — with vulnerability-DB references, scanning-tool guidance, CVSS
  severity interpretation, and license-compatibility matrices. Also performs NuGet package
  security reviews with manager-friendly executive summaries. Use to audit package dependencies,
  scan for vulnerabilities, check license compliance, or assess supply-chain security.
---

# Supply Chain Audit

> "Trust, but verify -- and in software supply chains, verify everything twice."
> -- Tanya Janca, *Alice and Bob Learn Application Security*

## Core Philosophy

Software supply chain security is not about avoiding dependencies -- it is about understanding the trust decisions you make with every `install`, `add`, or `restore` command. Every dependency is a delegation of trust: you are trusting that the package author writes secure code, that the registry has not been compromised, that no one has published a malicious version, and that the transitive dependencies you never chose are equally trustworthy.

**The three pillars of supply chain audit:**
1. **Vulnerability Scanning** -- Are any dependencies known to be vulnerable? Which CVEs apply? Are the vulnerable code paths reachable?
2. **License Compliance** -- Are the licenses compatible with the project's distribution model? Are there copyleft licenses that require source disclosure?
3. **Maintenance Health** -- Are dependencies actively maintained? Are security issues being addressed? Is the package at risk of abandonment?

The 10 domain principles, the knowledge-base lookup table and search protocol, the AI discipline
rules, the anti-pattern catalog, and the error-recovery procedures live in
`references/vulnerability-sources.md` under "Audit Methodology & Discipline."

## Workflow

### Phase 1: Vulnerability Scan

**Objective:** Identify all dependencies with known CVEs.

Run the ecosystem scanners (NuGet, npm, pip, yarn, pnpm), map each finding to CVSS severity, then
adjust raw CVSS for **contextual risk** — reachability (is the vulnerable code path invoked?),
exposure (internet-facing vs. internal vs. air-gapped), data sensitivity (PII, financial,
credentials), exploitability (public exploit available?), and compensating controls (WAF, network
segmentation). Never report raw CVSS as project risk.

Scanner commands + CVSS severity table + contextual-risk factors: `references/vulnerability-sources.md`.

### Phase 2: License Compliance

**Objective:** Verify all dependency licenses are compatible with the project's distribution model.

Detect licenses, classify by category (permissive / weak copyleft / strong copyleft /
proprietary / unknown), and flag genuine incompatibilities against the **actual** distribution
model — a GPL-3.0 dependency may be acceptable in SaaS but a compliance failure in shipped desktop
software.

License detection commands + classification matrix: `references/license-matrix.md`.

### Phase 3: Maintenance Health

**Objective:** Assess the ongoing viability and security responsiveness of each dependency.

Evaluate health indicators (last release, open security issues, contributor count, repository
status) and present them with **evidence, not judgment** — state the dates and counts, let the
human draw the conclusion.

Health-indicator thresholds + check commands: `references/vulnerability-sources.md`.

**Load on demand — `references/operating-guide.md`:** NuGet-Specific Review. Deeper detail: `references/nuget-executive-summary-templates.md`, `references/nuget-severity-guidelines.md`.

## State Block

```
<supply-chain-state>
mode: scan | license | health | report
project_path: [absolute path to project root]
ecosystems: [NuGet, npm, pip, etc.]
dependencies_scanned: [count]
cves_found: [count]
license_issues: [count]
health_concerns: [count]
last_action: [what was just completed]
next_action: [what should happen next]
</supply-chain-state>
```

## Output Template

| Template | Required Fields |
|----------|----------------|
| Vulnerability Report | Project, Scan Date, Scanners Used; Critical Findings table (CVE / Package / Installed / Fixed In / CVSS / Reachable / Contextual Risk); per-CVE detail (Reachability Analysis, Contextual Risk, Rationale, Remediation) |
| License Compliance Report | Project, Distribution Model, Project License; License Summary table (License / Count / Compatibility / Action); Findings Requiring Review (Package / License / Issue / Risk / Recommendation) |
| Maintenance Health Report | Project, Direct Dependencies count; Health Summary table (Status / Count / Packages); per-concern detail (Last Release, Open Issues, Contributors, Status, Risk, Recommendation, Alternatives) |

Full templates: `references/vulnerability-sources.md` | `references/license-matrix.md` | `references/nuget-security-review.md`

## Integration with Other Skills

- **dependency-mapper** -- use to understand structural implications of dependencies before auditing. Coupling metrics reveal which dependencies are most deeply embedded and hardest to replace.
- **technical-debt-assessor** -- outdated packages, license risks, and abandoned dependencies are quantifiable debt items with cost-to-fix and cost-to-carry.
- **oss-vetting** -- per-package approve/reject assessment for federal/CUI use before a dependency is adopted; this skill audits the dependencies a project already has.
- **architecture-review** -- dependency choices are architectural decisions that constrain the system's evolution.
