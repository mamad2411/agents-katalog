---
name: security-audit
description: Review code, configuration, and service behavior for security risks by checking trust boundaries, secret handling, auth, validation, and operational exposure, applying OWASP ASI Top 10 2026, NIST AI RMF, and CVSS 4.0 triage. Use when conducting focused security reviews of changes, pre-deployment audits, or full-service risk assessments.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Security Audit

Use this skill when reviewing a change, service, or deployment for security posture and obvious risk.

## When to Use

- focused security review of a change
- full-service risk assessment
- checking trust boundaries, secrets, auth, validation
- AI/ML review via OWASP ASI + NIST + ISO 42001

## Core Rules

- focus on real trust boundaries and attack surfaces
- prioritize exploitable risk over checklist theater
- treat code, config, and runtime exposure together
- call out unclear assumptions as risk, not as proof of safety
- avoid exposing real secrets or exploit details unnecessarily in user-visible artifacts
- **CVSS 4.0 & EPSS Triage**: Score vulnerabilities using CVSS 4.0 with CVSS-BTE nomenclature distinguishing Vulnerable System (VC/VI/VA) from Subsequent Systems (SC/SI/SA); MSS (Supplemental) metrics include Automatable and Recovery. Prioritize via the `CVSS 4.0 × EPSS × CISA KEV` triad (EPSS > 10% or CISA KEV requires 24–48h fix).
- **CVE Reachability Analysis**: Distinguish reachable from unreachable transitive CVEs via AST call-graph tracing (`govulncheck`, `osv-scanner`, `npm audit`); emit VEX `not_affected` (code_not_reachable) instead of blocking releases on dead code paths.
- **OWASP Top 10:2025 A10**: A10:2025 is "Mishandling of Exceptional Conditions" — audit error-handling paths and exception blocks; ensure fail-closed behavior (deny by default on uncaught exceptions, release DB connections, no stack trace leakage).
- **OWASP ASI01–10 (official 2026 list)**: for agentic AI systems apply the OWASP Top 10 for Agentic Applications 2026 exactly as published — ASI01 Agent Goal Hijack, ASI02 Tool Misuse & Exploitation, ASI03 Identity & Privilege Abuse, ASI04 Agentic Supply Chain, ASI05 Unexpected Code Execution (verify sandbox boundary adherence against `core/policies/execution-sandbox.md`), ASI06 Memory & Context Poisoning, ASI07 Insecure Inter-Agent Communication, ASI08 Cascading Failures, ASI09 Human-Agent Trust Exploitation, ASI10 Rogue Agents.
- **ZTA-MTLS**: Zero Trust Architecture deployments MUST enforce mTLS between all internal services using SPIFFE/SPIRE for workload identity issuance; block any service-to-service communication without a valid SVID.
- **EU-CRA-REPORTING**: EU Cyber Resilience Act reporting obligations have applied since 2026-09-11 — actively exploited vulnerabilities and severe incidents must reach ENISA/CSIRT within 24 hours; main product obligations (security-by-design, ≥5-year support period) land 2026-12-11 and machine-readable SBOM obligations by 2027-12-11. Flag any product in EU scope without a live, tested reporting runbook as a compliance finding.
- **PQC-TRANSITION**: audit cryptography against NIST IR 8547 (quantum-vulnerable RSA/ECDSA/ECDH/DH deprecated after 2030, disallowed after 2035): verify a CBOM crypto inventory (CycloneDX 1.6) exists and hybrid TLS (X25519MLKEM768 — client-side default since Chrome 131/Firefox 132) is enabled where TLS terminates server-side.
- **GenAI Red Teaming Manual**: structure adversarial testing of AI systems per OWASP GenAI Red Teaming Manual v1.0 (2026-10-20); record test coverage in the audit findings.

## Suggested Process

### 1. Identify The Security Boundary

Clarify:

- what data is sensitive
- who the actors are
- what external inputs are accepted
- what systems or credentials are trusted

### 2. Review The Main Risk Areas

Check:

- authn and authz
- input validation and output exposure
- secret and credential handling
- logging of sensitive data
- dependency and downstream trust assumptions
- unsafe default configuration or missing environment hardening

### 3. Check Change-Specific Risk

For a concrete change, verify:

- new endpoints or routes are protected appropriately
- new background or event paths do not bypass controls
- new config does not widen exposure unintentionally
- new dependencies are bounded and authenticated as expected

### 4. Check Operational Exposure

Review:

- debug or admin surfaces
- runtime permissions
- public network reachability
- auditability and rollback assumptions

### 5. Report Findings By Severity

Use:

- blocking risk for clear security flaws
- high-severity risk for likely misuse or privilege widening
- follow-up risk for hardening gaps that should be tracked

### 6. CVE Remediation & Virtual Patching

When an active CVE is identified:
- verify AST call-graph reachability before filing release-blocking issues
- apply SemVer-safe in-place upgrades; if breaking or unpatched, author virtual patch middleware (input validation/sanitization)
- run table-driven regression tests to verify exploit payload rejection

## Checklist

- [ ] trust boundary identified
- [ ] sensitive data paths reviewed
- [ ] auth and validation checked
- [ ] secret handling checked
- [ ] runtime exposure checked
- [ ] findings reported with clear severity using CVSS 4.0 BTE nomenclature
- [ ] OWASP Top 10:2025 gaps reviewed (A03 Supply Chain, A10 Exceptional Conditions, Misconfiguration)
- [ ] OWASP ASI01–10 checks applied for agentic AI systems (ASI05 execution sandbox verified per `core/policies/execution-sandbox.md`)
- [ ] ZTA mTLS / SPIFFE/SPIRE verification for zero-trust deployments
- [ ] SLSA Level 3 supply chain integrity checked for production builds
- [ ] EU CRA readiness checked for products in EU scope: 24h reporting runbook live (since 2026-09-11), support period declared, SBOM pipeline building toward the 2027-12-11 gate
- [ ] PQC readiness checked: CBOM crypto inventory present, hybrid TLS (X25519MLKEM768) enabled server-side, no quantum-vulnerable-only crypto for long-lived data

## Failure Modes

- **Audit scope too narrow**: the audit covers only one layer (e.g., code) and misses infra or identity. Mitigation: enumerate the full trust boundary before scoping.
- **Finding hidden in summary**: a high-severity finding is buried in the audit report. Mitigation: lead with severity-sorted findings; never present severity-3+ as appendix items.
- **No repro path**: a finding has no reproducible evidence. Mitigation: every finding must include a path, a command, and the expected vs actual output.
- **Remediation not validated**: a finding is closed without re-running the scan or test. Mitigation: re-run the audit after every remediation; record the before/after.
- **OWASP ASI not applied**: a finding is reported without referencing the OWASP ASI item. Mitigation: tag every finding with the relevant ASI01-ASI10 item and the agentic threat surface.
- **Credential in finding**: a finding includes a real secret or token. Mitigation: redact before publishing; never paste live credentials into audit reports.
- **Invented ASI titles**: findings tagged against non-existent ASI items (e.g. "ASI08 Missing HITL", "ASI02 Excessive Agency"). Mitigation: tag only against the official ASI01–ASI10 titles in Core Rules; treat any other label as an audit-quality defect.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: when auditing agentic systems, verify that untrusted content (tool outputs, retrieved data) cannot reframe the agent's operating objective; tag violations under the ASI01 check the Core Rules already mandate.
- **ASI03 Identity & Privilege Abuse**: authn/authz and runtime-permission review is the privilege-abuse control — flag any chain (tool call, delegation, role assumption) that widens privileges beyond the declared task scope.
- **ASI04 Supply Chain**: dependency and downstream trust assumptions are already in scope; the checklist requires SLSA Level 3 integrity for production builds — report unsigned or unpinned dependencies as findings.
- **ASI05 RCE Guard**: already mandated — verify execution sandbox boundary adherence against `core/policies/execution-sandbox.md` for every agentic system audited.
- **ASI06 Context & Memory Poisoning**: treat memory stores and retrieved context as untrusted surfaces in AI/ML reviews; check provenance validation and injection quarantine before trusting agent-internal context.
- **ASI09 Human-Agent Trust Exploitation**: findings must never be softened to unblock shipping. Mitigation: lead with severity-sorted results (CVSS 4.0 BTE), keep blocking risk visible, and redact live credentials from every user-visible artifact.

## Related Skills

- **review-code**: Review concrete code changes with broader quality checks
- **review-service**: Expand into full release-readiness review
- **manage-secrets**: Fix secret-handling issues safely
- **meeting-review**: Run a broader multi-role risk review
- **commit-code**: Prepare remediation changes for delivery
- Companion reference: `references/owasp-asi-and-cvss4-threat-modeling.md`
- Companion example: `examples/enterprise-service-security-audit-report.md`

## Output Contracts

- `contracts/schemas/security-audit.json`
