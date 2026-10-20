---
name: report-technical
description: Technical penetration test report from validated findings — produces a detailed, finding-level technical report suitable for engineering teams, security architects, and peer review. Every finding includes root cause, affected components, safe reproduction narrative, evidence references, CVSS v4.0 scoring, CWE mapping, exploitation feasibility assessment, and specific actionable remediation with code/config examples. Drafts only from existing redacted findings and evidence; never includes raw proof content, secrets, or exploit payloads in paste-ready form.
disable-model-invocation: true
risk: report-only
allowed-modes: [auto, bug-bounty, red-team, blue-team, offensive, grey-hat, reverse-engineering, mobile-pentest]
authorization-required: no
evidence-outputs: [report, finding-summary, cvss-scores, cwe-mapping, remediation-guidance, redaction-notes, technical-appendix]
---

# Technical assessment report — detailed finding documentation for engineering and security teams

Use this skill to draft a comprehensive technical report from validated, redacted findings. The audience is technical: security engineers, developers, DevOps, and architects who need enough detail to reproduce and fix each finding. Every finding must include root cause, safe reproduction narrative (not paste-ready exploits), specific affected code/config, and actionable remediation with examples. The report synthesizes data from `pentest_agent_list_findings` and `pentest_agent_list_evidence` — it never creates findings, never includes raw proof content, and never provides weaponized exploit code.

## Required inputs

- Findings from `pentest_agent_list_findings` filtered to `confirmed` and `likely` confidence. `needs-review` findings should be flagged as "requires further investigation" if included at all.
- Evidence records for each finding from `pentest_agent_list_evidence`: command output, HTTP request/response pairs, screenshots, code snippets.
- Scope file confirming assessment boundaries.
- Engagement metadata: dates, methodology, tools used, target description.
- If available: architecture diagrams, data-flow documentation, threat model output, previous assessment reports for comparison.

## Required gates

1. `pentest_agent_load_config` to verify redaction and storage policy.
2. `pentest_agent_list_findings` for the full finding inventory.
3. `pentest_agent_list_evidence` to load evidence records with references.
4. `pentest_agent_redact_evidence` for a final redaction pass on all evidence excerpts.
5. `pentest_agent_render_report` with template `technical` to produce the final document.
6. No authorization cache required.

## Workflow

### Phase 1 — methodology and scope documentation

Document how the assessment was conducted so readers understand what was tested and how.

1. **Assessment type**: black-box (no internal access or documentation), grey-box (limited access — e.g., test credentials, API docs, architecture overview), white-box (full source code and infrastructure access), or a hybrid (different access levels for different components).
2. **Phases conducted**: recon, enumeration, vulnerability identification, validation (gated), post-exploitation (if authorized and conducted), reporting.
3. **Tools used** (table):
   | Tool | Version | Purpose |
   |---|---|---|
   | httpx | 1.6.0 | HTTP response profiling, technology detection |
   | nuclei | 3.2.0 | Automated vulnerability template scanning |
   | Burp Suite Pro | 2024.12 | Manual web application testing, traffic interception |
   | ... | ... | ... |
4. **Standards referenced**: OWASP Testing Guide v4, OWASP ASVS v4.0, CVSS v4.0, CWE, MITRE ATT&CK (if applicable), NIST SP 800-115.
5. **Scope boundaries**: in-scope targets, out-of-scope exclusions, allowed and prohibited testing methods, testing windows, rate limits.
6. **Limitations**: what could not be tested and why (WAF interference, rate limiting prevented certain checks, non-production environment differed from production, time constraints, tool limitations).

### Phase 2 — finding inventory and severity distribution

Provide a summary table so readers can scan the report quickly.

1. **Severity distribution**:
   | Severity | Count | Percentage |
   |---|---|---|
   | Critical (CVSS 9.0-10.0) | [N] | [%] |
   | High (CVSS 7.0-8.9) | [N] | [%] |
   | Medium (CVSS 4.0-6.9) | [N] | [%] |
   | Low (CVSS 0.1-3.9) | [N] | [%] |
   | Informational | [N] | [%] |
2. **Category distribution** (by CWE class):
   | Category | Count |
   |---|---|
   | Injection (CWE-74, 77, 78, 79, 89, 94, 918) | [N] |
   | Broken Access Control (CWE-284, 639, 862, 863) | [N] |
   | Cryptographic Failures (CWE-310, 311, 327, 328) | [N] |
   | Security Misconfiguration (CWE-16, 209, 942) | [N] |
   | ... | ... |
3. **Finding-to-asset matrix**: which systems/components are affected by which findings. Helps prioritize if only certain systems can be patched this cycle.

### Phase 3 — detailed finding documentation

Each finding follows a strict, reproducible structure. Technical depth must be sufficient that an engineer unfamiliar with the assessment can understand and fix the issue without asking follow-up questions.

**Finding template**:

1. **Finding ID**: F-0XX.
2. **Title**: `[Severity] [Vulnerability Class] in [Component]` — e.g., "[CRITICAL] SQL Injection in /api/v1/products search parameter."
3. **Severity**:
   - CVSS v4.0 vector string (full).
   - Base score and severity label.
   - Environmental score if relevant (adjusted for target environment).
   - Temporal score if exploit code is public.
4. **CWE**: primary CWE ID and name. Secondary CWEs if the finding involves a chain.
5. **Affected assets**:
   - URL(s) with HTTP method(s) and parameter(s).
   - File path(s) if source code was reviewed.
   - Infrastructure component(s): web server, application server, database, cache, message queue.
   - Versions of affected software if known.
6. **Description** (2-4 sentences): what the vulnerability is, where it exists, and how the application's behavior deviates from secure design. Non-speculative, grounded in observed evidence.
7. **Root cause**: why the vulnerability exists. Is it missing input validation? Missing authorization check? Insecure default configuration? Lack of parameterized queries? Misconfigured cloud resource policy? Be specific — "missing input validation" is not specific; "the `search` parameter in the `ProductController.list()` method is concatenated directly into a SQL query string without using parameterized queries or an ORM" is specific.
8. **Evidence**:
   - Redacted HTTP request/response pair showing the vulnerability.
   - Redacted tool output confirming the finding (nuclei template match, Burp scanner finding, manual test output).
   - Code snippet if source code was reviewed (redacted — file path only unless the client approves code excerpt inclusion).
   - Screenshot description (not the raw screenshot in shared evidence — describe what the screenshot shows).
   - Evidence references: IDs from `pentest_agent_list_evidence`.
9. **Safe reproduction narrative**: describe the steps to reproduce the vulnerability WITHOUT providing weaponized payloads. Use stand-in values and describe the technique at a level that a security professional can replicate but a script kiddie cannot copy-paste.
   - Good: "Submit a POST request to `/api/v1/products` with a JSON body containing a `search` parameter value that terminates the SQL string and injects a UNION SELECT statement. The application returns data from the `users` table in the response, confirming SQL injection."
   - Avoid: Paste-ready curl command with working SQL injection payload.
10. **Impact** (technical):
    - What data, functionality, or system is at risk? (e.g., "Full database contents accessible, including 2.3 million user records with bcrypt-hashed passwords and PII fields (full name, email, phone, address).")
    - What is the worst-case realistic outcome? (e.g., "An attacker can exfiltrate the entire database, modify records, or potentially achieve remote code execution via `xp_cmdshell` on the database server.")
    - Is chaining possible? (e.g., "Combined with finding F-004 (exposed admin panel), an attacker can achieve full application takeover.")
11. **Remediation**:
    - **Immediate fix**: the minimum change to close the vulnerability. Include code example (in the appropriate language/framework) showing the secure pattern.
    - **Defense-in-depth**: additional controls that would prevent similar vulnerabilities or reduce impact. Examples: WAF rule, CSP header, database least-privilege account, network segmentation.
    - **Verification**: how to confirm the fix is effective (the specific test case that should now fail safely).
12. **References**: links to CWE, OWASP Cheat Sheet, vendor security advisory, relevant CVEs, framework-specific security documentation.

### Phase 4 — remediation prioritization and roadmap

Help engineering teams plan the work.

1. **Priority 1 — Immediate** (0-7 days): critical findings or findings with active exploitation indicators. Risk acceptance required if not fixed.
2. **Priority 2 — This sprint** (1-4 weeks): high-severity findings with no active exploitation but significant risk.
3. **Priority 3 — This quarter** (1-3 months): medium-severity findings. Defense-in-depth improvements.
4. **Priority 4 — Backlog**: low-severity and informational findings.
5. **Dependencies**: which fixes block others (e.g., "Fix the authentication bypass (F-001) before testing the IDOR finding (F-005), because the IDOR is only exploitable post-authentication").
6. **Quick wins** (low effort, high impact): findings that can be fixed in under a day and materially reduce risk. Flag these for immediate engineering attention.

### Phase 5 — positive findings and effective controls

Document what was done RIGHT. This builds credibility, avoids the "auditors just find problems" perception, and helps the organization preserve effective controls through future changes.

1. **Effective controls observed**: which security measures were in place and functioning correctly.
   - Example: "Strong Content-Security-Policy header with `script-src 'self'` and nonce-based enforcement prevented XSS exploitation even when injection points were identified."
   - Example: "Rate limiting on the authentication endpoint prevented brute-force attacks. After 5 failed attempts, the account was locked for 15 minutes."
2. **Security maturity observations**: practices beyond individual controls that contributed to security posture.
   - Example: "The engineering team had already identified and patched 3 of the 5 endpoints we had planned to test, based on their internal threat model. This demonstrates strong security-awareness in the development lifecycle."
3. **Recommended preservations**: controls or practices that should be extended to other components.
   - Example: "The API gateway enforces JWT validation and scope checking. Extend this pattern to the legacy SOAP endpoints, which currently rely on IP-allowlisting only."

### Phase 6 — appendices

Provide reference material that supports the findings without cluttering the main report.

1. **Appendix A — Tool output index**: list of all tool output files, their evidence IDs, and a one-line description.
2. **Appendix B — Scope document**: the agreed-upon scope in full (or reference to the scope file location).
3. **Appendix C — Methodology details**: step-by-step methodology for each assessment phase.
4. **Appendix D — Glossary**: definitions of vulnerability classes, severity ratings, and technical terms for readers who may not be security specialists.
5. **Appendix E — Retest notes** (if retesting was conducted): which findings were retested, on what date, and result (fixed, partially fixed, not fixed, regression).

## Decision points

- **Finding was identified by automated scanner but not manually verified**: label confidence as `needs-review` or `likely` (not `confirmed`). Clearly state "Identified by automated scanning; manual verification recommended before remediation."
- **Finding relies on a specific version or configuration**: document the version and configuration. If the production environment differs, the finding may not apply.
- **Multiple findings share the same root cause**: consolidate remediation into one recommendation. Reference all affected findings. Explain how fixing the root cause addresses all instances.
- **Remediation requires significant architectural change**: provide both a tactical fix (quick, partial) and a strategic fix (comprehensive, longer). Let the engineering team choose based on their timeline.
- **Finding impacts a third-party component**: document the vendor, component version, and whether a patch is available. Recommend contacting the vendor if no patch exists.

## Prohibited behavior

- Including paste-ready exploit code, working payloads, or weaponized scripts.
- Including raw proof file contents, raw secrets, passwords, API keys, or tokens.
- Including PII, PHI, or customer data from evidence excerpts. Reference data types by category.
- Including unredacted internal hostnames, IP addresses (internal), or infrastructure details in the main report body (place in a confidential appendix if needed).
- Claiming a finding is `confirmed` based solely on automated scanner output without manual verification.
- Speculating about business impact without organizational context (leave business impact to the executive report skill).
- Naming individual developers or administrators.

## Stop conditions

- Evidence for a `confirmed` finding is insufficient to write a clear reproduction narrative → downgrade to `likely` and note "Insufficient evidence to provide reproduction steps — manual verification required."
- Key remediation (e.g., a critical library upgrade) is known to break other functionality → flag as "Requires integration testing before deployment." Do not recommend without the caveat.
- A finding appears to be a false positive upon closer inspection → downgrade to `false-positive` with explanation and evidence. Do not include in the main report body; reference in an appendix if context is useful.

## Evidence template

```text
Technical assessment report for: [TARGET]
Assessment period: [DATES]
Methodology: [black-box / grey-box / white-box]
Total findings: [N] (Critical: [N], High: [N], Medium: [N], Low: [N], Informational: [N])

=== FINDING INVENTORY ===
| ID | Severity | Title | CWE | Affected Component | Confidence |
|---|---|---|---|---|---|
| F-001 | Critical | SQL Injection in /api/v1/products | CWE-89 | ProductController.list() | Confirmed |
| F-002 | High | IDOR in /api/v1/users/{id} | CWE-639 | UserController.get() | Confirmed |
| ...

=== PRIORITY ROADMAP ===
Priority 1 (0-7d): [findings with remediation effort and dependencies]
Priority 2 (1-4w): [...]
Priority 3 (1-3m): [...]
Priority 4 (backlog): [...]

=== EFFECTIVE CONTROLS OBSERVED ===
[What was working well, what should be preserved or extended]

=== LIMITATIONS ===
[What was not tested, why, and the potential impact on findings completeness]

Redaction notes:
  - All payloads abstracted to technique description only.
  - All secrets, tokens, and API keys replaced with <REDACTED>.
  - All PII references replaced with data category labels.
  - Internal IPs and hostnames in a confidential appendix (not in the main report body).
  - Evidence excerpts use stand-in values; original evidence records are available via evidence IDs.
```

## Handoff

1. Store the technical report under `.pi/pentest-agent/engagements/<id>/reports/technical/`.
2. `pentest_agent_export_report` for a standalone Markdown and JSON version.
3. If the client requests, provide findings in a machine-readable format (JSON, CSV) for import into their ticketing system.
4. Explicitly note: this report contains no paste-ready exploits, no raw secrets, no PII, and no unredacted internal infrastructure details. All findings are traceable to evidence records, and reproduction narratives describe techniques without providing weaponized payloads.
