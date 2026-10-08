---
name: reporting
description: |
  This skill should be used when the user mentions "generate report", "pentest report",
  "engagement report", "findings report", "executive summary", "technical report",
  "vulnerability report", "remediation report", "remediation plan", "retest report",
  "write up findings", "document findings", "report findings", "create report",
  "final report", "assessment report", "security report", "audit report",
  "CVSS score", "CVSS vector", "risk rating", "risk assessment", "severity rating",
  "finding writeup", "finding documentation", "proof of concept", "PoC documentation",
  "evidence documentation", "screenshot evidence", "report template",
  "report structure", "report format", "deliverable", "client deliverable",
  "remediation guidance", "fix recommendations", "remediation priority",
  "retest validation", "retest verification", "regression testing",
  "OWASP report", "PTES report", "compliance report", "PCI report",
  "attack narrative", "exploitation timeline", "testing coverage",
  "exploit chain documentation", "chain of evidence", "finding prioritization",
  or discusses creating, structuring, writing, or delivering penetration testing documentation
  and assessment reports. Activate even when the user says "write up the results",
  "summarize findings", or "document what we found" in an engagement context.
version: 2.0.0
---

# Security Reporting

End-to-end pentest reporting for web and application security engagements -- from data gathering through structured report generation. This skill integrates deeply with elliot's data layer to produce comprehensive, evidence-backed deliverables aligned with OWASP Testing Guide and PTES reporting standards.

## Why This Matters

The report is the only artifact the client keeps. Every vulnerability discovered, every technique attempted, every chain identified -- it all means nothing if the report is unclear, incomplete, or poorly structured. A good report drives remediation. A bad report gets filed and forgotten.

## Report Lifecycle

```
Data Gathering --> Finding Prioritization --> Report Structure --> Writing --> Quality Review --> Delivery
```

Every phase draws on elliot's data layer. Skip nothing.

## Phase 1 -- Data Gathering

Before writing a single line, collect all engagement data from elliot's trackers.

### Vulnerability Data

```bash
# Full findings summary -- severity counts, status breakdown
node "${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js" summary

# All findings with details
node "${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js" list

# Search for specific finding types
node "${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js" search sqli
node "${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js" list --severity CRITICAL
node "${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js" list --type xss

# Export findings as formatted HTML
node "${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js" html
```

### Testing Coverage

```bash
# Technique coverage summary -- tools used, results, gaps
node "${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js" summary

# Full coverage analysis -- what was tested, what was not
node "${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js" coverage

# All tool reports generated during the engagement
node "${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js" reports

# Export techniques as formatted HTML
node "${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js" html

# Search for specific technique results
node "${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js" list --result success
node "${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js" list --result blocked
```

### Exploit Chains

```bash
# Detect exploit chains from combined findings
node "${CLAUDE_PLUGIN_ROOT}/scripts/chain-detector.js"

# Check if a specific finding participates in chains
node "${CLAUDE_PLUGIN_ROOT}/scripts/chain-detector.js" check f-001

# View chain rule glossary
node "${CLAUDE_PLUGIN_ROOT}/scripts/chain-detector.js" glossary
```

Chain detection uses 11 built-in rules that match finding combinations (e.g., SSRF + cloud metadata = cloud credential theft, SQLi + file read = source code disclosure). Chains elevate the severity of their component findings and MUST be documented in the report.

### Campaign Metadata

```bash
# Campaign state -- phases, steps, progress, blockers
node "${CLAUDE_PLUGIN_ROOT}/scripts/session-state.js" show

# Current scan profile (loud/normal/stealth/paranoid)
node "${CLAUDE_PLUGIN_ROOT}/scripts/scan-profile.js" show
```

### Target Context

```bash
# Target intelligence gathered during the engagement
node "${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js" summary

# All intel for a specific target
node "${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js" show example.com

# Intel by category
node "${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js" list --category tech-stack
node "${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js" list --category defense
node "${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js" list --category credential
```

### Hexstrike Report Tools

Load: `ToolSearch` -> `select:mcp__hexstrike-ai__create_vulnerability_report`

Use `create_vulnerability_report` for formatted individual vulnerability documentation via Hexstrike.

Load: `ToolSearch` -> `select:mcp__hexstrike-ai__create_scan_summary`

Use `create_scan_summary` to consolidate multiple tool runs into a unified summary.

Load: `ToolSearch` -> `select:mcp__hexstrike-ai__format_tool_output_visual`

Use `format_tool_output_visual` to format raw tool output for inclusion in reports.

## Phase 2 -- Finding Prioritization

After gathering data, prioritize findings for the report. This determines report structure and emphasis.

### Severity Classification

Use CVSS 3.1 base scores for technical precision. Map to qualitative ratings:

| Severity | CVSS Range | Characteristics | Report Priority |
|----------|-----------|-----------------|-----------------|
| Critical | 9.0 - 10.0 | RCE, full DB access, payment compromise, pre-auth admin takeover | Lead the report, executive summary highlight |
| High | 7.0 - 8.9 | Auth bypass, IDOR with sensitive data, SQLi with data access | Second tier, individual writeups |
| Medium | 4.0 - 6.9 | Stored XSS, info disclosure, missing rate limits, CSRF | Grouped by category, standard writeups |
| Low | 0.1 - 3.9 | Reflected XSS requiring interaction, minor info leak, verbose errors | Grouped, abbreviated writeups |
| Informational | 0.0 | Best practices, hardening suggestions, version disclosure | Table format, no individual writeups |

See `references/finding-writeup.md` for CVSS vector string construction.

### Chain Elevation

When the chain detector identifies exploit chains, elevate the severity of the chain as a whole:

- Document the chain as a separate finding with its own ID
- Chain severity is typically one level above the highest component finding
- Reference component finding IDs in the chain writeup
- Include the full attack path: entry point -> pivots -> objective

### Risk Matrix

Map findings to business impact dimensions:

| Dimension | What to Assess | Example |
|-----------|---------------|---------|
| **Financial** | Payment manipulation, fraud potential, regulatory fines | SQLi on payment DB = potential PCI breach |
| **Data** | PII exposure, data breach potential, record counts | IDOR exposing 50K user records |
| **Availability** | DoS potential, service disruption, recovery time | ReDoS on login form = full app lockout |
| **Reputation** | Defacement, customer-facing impact, media risk | Stored XSS on public-facing pages |
| **Compliance** | Regulatory violation, audit failure | Missing HTTPS = PCI-DSS failure |

## Phase 3 -- Report Structure

Choose the appropriate report type based on the engagement and audience.

### Report Types

| Report Type | Audience | When to Use | Template |
|-------------|----------|-------------|----------|
| Executive Summary | C-suite, board, non-technical stakeholders | Every engagement | `references/executive-summary.md` |
| Full Technical Report | Development team, security team, sysadmins | Standard pentest deliverable | `references/report-templates.md` |
| Remediation Plan | Development team, project managers | When client requests actionable fix list | `references/remediation-guidance.md` |
| Retest Report | Security team, compliance | After remediation, verifying fixes | `references/report-templates.md` |
| Finding Writeup | Bug bounty, individual vuln documentation | Per-finding documentation | `references/finding-writeup.md` |

### Report Output Location

Reports are written to the project directory under `reports/`:

```
reports/
  executive-summary-<target>-<YYYYMMDD>.md
  technical-report-<target>-<YYYYMMDD>.md
  remediation-plan-<target>-<YYYYMMDD>.md
  retest-report-<target>-<YYYYMMDD>.md
  evidence/
    screenshots/          # Annotated screenshots
    requests/             # HTTP request/response pairs
    tool-output/          # Formatted tool output
  findings-export.html    # From findings-tracker.js html
  techniques-export.html  # From techniques-tracker.js html
```

## Phase 4 -- Writing

### Full Technical Report Structure

Follow this structure for the primary deliverable. See `references/report-templates.md` for the complete template.

```
1. Cover Page
2. Table of Contents
3. Executive Summary (1-2 pages max)
4. Scope and Methodology
5. Risk Summary (severity matrix, finding counts)
6. Findings (ordered by severity, then by category)
   - Each finding: title, severity, CVSS, description, evidence, impact, remediation
7. Exploit Chains (from chain-detector.js)
8. Testing Coverage (from techniques-tracker.js coverage)
9. Recommendations Summary (prioritized timeline)
10. Appendices
    A. Tool Versions
    B. Methodology Reference (OWASP/PTES)
    C. CVSS Scoring Reference
    D. Glossary
```

### Writing Individual Findings

Every finding follows the same structure. See `references/finding-writeup.md` for the complete guide.

```markdown
### F-001: SQL Injection in Login Endpoint

| Field | Value |
|-------|-------|
| Severity | HIGH |
| CVSS 3.1 | 8.6 — AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N |
| Affected Asset | https://example.com/api/v1/auth/login |
| Parameter | username |
| Category | Injection |
| Status | Confirmed |
| CWE | CWE-89: Improper Neutralization of Special Elements in SQL |

**Description**: <what the vulnerability is>

**Evidence**: <request/response, screenshots, tool output>

**Impact**: <what an attacker can achieve — be specific about business impact>

**Remediation**:
- **Immediate**: <what to do right now>
- **Long-term**: <architectural change>

**References**: <CVE, CWE, OWASP links>
```

### Writing Exploit Chain Findings

```markdown
### CHAIN-001: SSRF to Cloud Credential Theft

| Field | Value |
|-------|-------|
| Severity | CRITICAL |
| Chain Components | F-003 (SSRF, HIGH) + F-007 (Cloud Metadata, MEDIUM) |
| Attack Path | SSRF -> IMDS -> IAM credentials -> S3 bucket access |

**Chain Narrative**: <step-by-step attack flow connecting the component vulnerabilities>

**Combined Impact**: <business impact of the full chain, not individual components>

**Remediation**: <must address all links in the chain>
```

### Evidence Documentation

See `references/evidence-collection.md` for evidence standards. Key requirements:

- Every finding MUST have supporting evidence
- HTTP request/response pairs: full headers + body, highlight the vulnerable parameter
- Screenshots: annotated with arrows/highlights pointing to the vulnerability
- Tool output: relevant sections only, formatted for readability
- PoC scripts: working reproduction scripts with sanitized targets

## Phase 5 -- Quality Review

Run through the quality checklist before delivery. Each report type has its own checklist.

### Universal Quality Checklist

- [ ] All findings from `findings-tracker.js list` are documented
- [ ] Exploit chains from `chain-detector.js` are documented as separate findings
- [ ] Every finding has supporting evidence
- [ ] CVSS vectors are correct (validate at first.org/cvss/calculator/3.1)
- [ ] Severity ratings match CVSS scores
- [ ] CWE IDs are accurate
- [ ] Remediation recommendations are specific and actionable
- [ ] Testing coverage from `techniques-tracker.js coverage` is documented
- [ ] Target context from `target-intel.js summary` informs the scope section
- [ ] No duplicate findings (check `findings-tracker.js` deduplication)
- [ ] Consistent terminology throughout
- [ ] Timestamps in UTC
- [ ] Report filename follows convention: `<type>-<target>-<YYYYMMDD>.md`

### Executive Summary Checklist

- [ ] Under 2 pages
- [ ] No technical jargon without explanation
- [ ] Finding counts by severity in a table
- [ ] Top 3 most impactful findings highlighted
- [ ] Overall risk rating with justification
- [ ] Strategic recommendations (not tactical fixes)
- [ ] Compliance implications noted

### Technical Report Checklist

- [ ] Scope clearly defines in-scope and out-of-scope assets
- [ ] Methodology section references OWASP/PTES
- [ ] Findings ordered by severity (Critical first)
- [ ] Each finding has: title, severity, CVSS, description, evidence, impact, remediation, CWE
- [ ] Evidence is verifiable (requests can be replayed, screenshots are clear)
- [ ] Remediation plan has prioritized timeline
- [ ] Coverage section shows what was and was NOT tested
- [ ] Appendices include tool versions

### Remediation Plan Checklist

- [ ] Findings grouped by fix type (not by severity)
- [ ] Timeline is realistic (immediate / short-term / medium-term / ongoing)
- [ ] Each fix has verification steps
- [ ] Quick wins identified separately
- [ ] Dependencies between fixes noted
- [ ] Compensating controls for findings that cannot be immediately fixed

### Retest Report Checklist

- [ ] References original report and finding IDs
- [ ] Each finding has status: Fixed / Partially Fixed / Not Fixed / Regressed
- [ ] Verification evidence for each status
- [ ] New findings discovered during retest documented
- [ ] Overall remediation progress percentage

## Phase 6 -- Delivery

### Report Generation Commands

```bash
# Generate HTML exports for appendices
node "${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js" html
node "${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js" html
```

### Post-Delivery Logging

```bash
# Log report delivery in session state
node "${CLAUDE_PLUGIN_ROOT}/scripts/session-state.js" add-note "Report delivered: technical-report-example.com-20260320.md"
node "${CLAUDE_PLUGIN_ROOT}/scripts/session-state.js" metric reports-delivered
```

## Cross-Skill Integration

- **Web assessment** findings feed directly into the report via `findings-tracker.js`
- **API testing** findings use the same tracker and report structure
- **Cloud lateral** findings include IAM-specific evidence and cloud-native remediation
- **WAF bypass** findings document both the bypass technique and the underlying vulnerability
- **WordPress hacking** findings reference WPScan output and WordPress-specific remediation
- **Password attacks** findings document cracked credentials with appropriate masking

## Reference Files

| File | When to Read |
|------|-------------|
| `references/report-templates.md` | When generating any report -- contains full templates for technical report, retest report, and finding blocks |
| `references/finding-writeup.md` | When writing individual finding entries -- CVSS vectors, CWE mapping, evidence requirements, writeup structure |
| `references/executive-summary.md` | When writing executive summaries -- non-technical language, risk posture, strategic recommendations |
| `references/evidence-collection.md` | When documenting evidence -- screenshot standards, request/response capture, PoC documentation, chain-of-evidence |
| `references/remediation-guidance.md` | When writing remediation recommendations -- fix steps by vuln type, priority ordering, verification procedures |
