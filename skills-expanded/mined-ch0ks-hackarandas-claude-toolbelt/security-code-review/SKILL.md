---
name: security-code-review
description: Full security code review with Semgrep Pro scan, taint analysis, CWE mapping, OWASP Top 10 coverage, and generation of a formal Security Code Review Report saved to /security-review/ in the repository root. Use when reviewing code for vulnerabilities, auditing a file for security issues, or before merging security-sensitive changes.
allowed-tools: Bash, Read, Write, Grep, Glob
author: Adrian Puente Z. (@ch0ks) — www.hackarandas.com
---

Perform a thorough security code review and generate a formal Security Code Review Report.
You are acting as a Staff Security Engineer with deep expertise in SAST, taint analysis, and secure development.

---

## Step 1 — Collect Author & Repository Metadata

Before anything else, gather the context needed for the report header:

```bash
# Author identity
git config --list | grep -E "^user\.(name|email)"

# Repository name
basename $(git rev-parse --show-toplevel)

# Current branch and latest commit
git rev-parse --abbrev-ref HEAD
git log -1 --format="%H %s" 

# Files in scope (what was changed or what is being reviewed)
git diff --name-only HEAD
# If working tree is clean, fall back to:
git ls-files --others --exclude-standard
```

Format the author as: `Firstname Lastname (email@domain.com)`
Generate the report filename as: `security-code-review-report-YYYYMMDD.md` using today's date.
Generate the Document ID as: `SCR-YYYYMMDD-001`

---

## Step 2 — Run Semgrep Pro Scan

Run Semgrep Pro before any manual analysis:

```bash
# Create output directory and save raw results as a dated JSON artifact
SECURITY_REVIEW_DIR=$(git rev-parse --show-toplevel)/security-review
mkdir -p "$SECURITY_REVIEW_DIR"
DATE=$(date +%Y%m%d)
SEMGREP_JSON="$SECURITY_REVIEW_DIR/semgrep-results-${DATE}.json"

# Scoped to current file or full project — output piped through tee to save JSON artifact
semgrep scan --pro \
  --config=p/default \
  --config=p/owasp-top-ten \
  --config=p/secrets \
  --json 2>/dev/null | tee "$SEMGREP_JSON"

echo "Semgrep results saved: $SEMGREP_JSON"
```

For each finding extract:
- `check_id` — rule ID
- `path` + `start.line` — location
- `extra.message` — description
- `extra.severity` — severity
- `extra.metadata.cwe` — CWE mapping
- `extra.metadata.confidence` — confidence level

Treat Semgrep Pro interprocedural findings at high confidence as ground truth for taint flows.
If Semgrep is unavailable, note it in the report and proceed with manual analysis only.

---

## Step 3 — Manual Review

Analyze the code for the following vulnerability classes. Map every finding to a CWE.

### 1. Injection & Taint Flows
- Trace untrusted inputs: HTTP params, headers, cookies, file input, env vars, DB results
- Follow taint paths to sinks: SQL queries, shell commands, file paths, HTML rendering, deserializers, HTTP clients
- Identify missing, incomplete, or bypassable sanitizers
- CWE-89, CWE-78, CWE-79, CWE-094, CWE-918

### 2. Authentication & Authorization
- Missing or bypassable auth checks, broken access control, IDOR
- JWT issues: algorithm confusion, missing claim validation (`aud`, `iss`, `exp`), weak secrets
- Session flaws: fixation, insufficient entropy, missing invalidation on logout
- CWE-287, CWE-285, CWE-384, CWE-798

### 3. Secrets & Sensitive Data
- Hardcoded credentials, API keys, tokens, passwords
- Secrets in logs, error messages, stack traces, or API responses
- PII exposure, insecure storage
- CWE-312, CWE-315, CWE-359, CWE-798

### 4. Cryptography
- Broken/weak algorithms (MD5, SHA1, DES, ECB mode)
- Hardcoded or predictable IVs, salts, keys
- Timing-attack vulnerable comparisons (`==` vs `hmac.compare_digest`)
- Improper cert validation, TLS downgrade, weak RNG (`random` vs `secrets`)
- CWE-327, CWE-330, CWE-326, CWE-295

### 5. OWASP Top 10 (2021)
- A01 Broken Access Control · A02 Cryptographic Failures · A03 Injection
- A04 Insecure Design · A05 Security Misconfiguration · A06 Vulnerable Components
- A07 Auth Failures · A08 Data Integrity Failures · A09 Logging Failures · A10 SSRF

### 6. Dependency Risks
- Known vulnerable, deprecated, or abandoned imports
- Dependencies used for security operations with safer alternatives

---

## Step 4 — Correlate & Deduplicate

- Merge Semgrep Pro findings with manual findings — never report the same issue twice
- Assess each Semgrep finding as TP or FP based on code context
- Document confirmed FPs with reasoning — this is signal for rule tuning
- Note manual findings Semgrep missed — these are rule coverage gaps

---

## Step 5 — Generate the Security Code Review Report

Create the `/security-review/` directory at the repository root if it does not exist:

```bash
mkdir -p $(git rev-parse --show-toplevel)/security-review
```

Write the full report to:
`$(git rev-parse --show-toplevel)/security-review/security-code-review-report-YYYYMMDD.md`

The report must follow this exact structure:

---

```markdown
# Security Code Review Report

---

## 1. Header Metadata

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| Document ID    | SCR-YYYYMMDD-001                                   |
| Date           | YYYY-MM-DD                                         |
| Author         | Firstname Lastname (email@domain.com)              |
| Repository     | <repo name>                                        |
| Branch         | <branch>                                           |
| Commit         | <short hash> — <commit message>                    |
| Files Reviewed | <list of files reviewed>                           |
| Classification | CONFIDENTIAL — Internal Security Use Only          |
| Status         | DRAFT \| FINAL                                     |
| Semgrep Engine | Pro \| OSS \| Not available                        |

---

## 2. Executive Summary

<2–3 paragraph summary of the overall security posture. Include:
- Total findings count broken down by severity (Critical / High / Medium / Low / Info)
- Highest risk areas identified
- Overall risk trajectory: e.g. MEDIUM-HIGH → LOW after remediation
- Remediation status overview: X resolved, Y pending, Z accepted risk
- One-line approval recommendation>

### Finding Counts by Severity

| Severity | Count | Resolved | Pending | Accepted Risk |
|----------|-------|----------|---------|---------------|
| Critical |       |          |         |               |
| High     |       |          |         |               |
| Medium   |       |          |         |               |
| Low      |       |          |         |               |
| Info     |       |          |         |               |
| **Total**|       |          |         |               |

---

## 3. Scope

### In Scope
<List every file, module, or component reviewed>

### Out of Scope
<List what was explicitly not reviewed and why — e.g. infrastructure config, third-party libraries, test fixtures>

### Review Method
- Static analysis: Semgrep Pro (interprocedural taint analysis)
- Manual review: taint tracing, auth/authz logic, crypto usage, secrets
- Dependency audit: import analysis

---

## 4. Findings

<!-- Repeat this block for each finding. Number sequentially: FINDING-001, FINDING-002, etc. -->

### FINDING-001 — <Short Title>

| Field       | Value                              |
|-------------|------------------------------------|
| ID          | FINDING-001                        |
| Severity    | Critical \| High \| Medium \| Low \| Info |
| Category    | <Injection \| Auth \| Crypto \| Secrets \| etc.> |
| CWE         | CWE-<id> — <name>                  |
| Location    | `<file>:<line>`                    |
| Confidence  | High \| Medium \| Low              |
| Source      | Semgrep Pro \| Manual \| Both      |
| Analysis    | Syntactic \| Semantic \| Interprocedural |
| Status      | Open \| Resolved \| Accepted Risk  |

#### Description
<What the vulnerability is and why it is exploitable. Specific to this code — not generic.>

#### Risk Assessment

| Factor      | Rating               | Rationale                        |
|-------------|----------------------|----------------------------------|
| Likelihood  | High \| Medium \| Low | <why>                           |
| Impact      | High \| Medium \| Low | <what an attacker achieves>     |
| Risk Level  | Critical \| High \| Medium \| Low | Likelihood × Impact  |

#### Evidence
```<language>
<Exact vulnerable code snippet with line numbers>
```

#### Impact Analysis
<What an attacker can concretely achieve by exploiting this. Be specific — not "data could be exposed" but "an attacker can extract all rows from the users table including password hashes.">

#### Recommendation
<Specific fix. Show a corrected code snippet. Name the safe API or pattern explicitly.>

```<language>
<Fixed code snippet>
```

#### Remediation Status
- [ ] Pending
- [ ] Resolved — <PR/commit reference if available>
- [ ] Accepted Risk — <justification and expiry date>

---

## 5. Risk Summary Matrix

| ID          | Title              | Severity | Likelihood | Impact | Risk Score | Status  |
|-------------|--------------------|----------|------------|--------|------------|---------|
| FINDING-001 |                    |          |            |        |            |         |
| FINDING-002 |                    |          |            |        |            |         |
| ...         |                    |          |            |        |            |         |

### Overall Risk Score

| Phase             | Score         | Rationale                            |
|-------------------|---------------|--------------------------------------|
| Before remediation | HIGH (7.5/10) | <reasoning>                         |
| After remediation  | LOW (2.5/10)  | <reasoning>                         |
| Risk reduction     | ~67%          |                                      |

---

## 6. Recommendations

### Immediate Actions (P0 — Block Merge)
<List all [BLOCK] findings with one-line remediation action each>

### PR Description Template
```
## Security Review

This PR has been reviewed by a Staff Security Engineer.

Findings addressed: <list FINDING IDs>
Remaining open findings: <list with justification>
Semgrep Pro scan: PASSED | FAILED (see /security-review/<report filename>)

Reviewer: <Author Name>
Date: <YYYY-MM-DD>
```

### Long-Term Recommendations
<Grouped by theme — e.g. "Adopt parameterized query helpers project-wide", "Add Semgrep rule for X pattern", "Enforce secrets scanning in CI">

---

## 7. Compliance Impact

| Framework   | Control                        | Before        | After         |
|-------------|-------------------------------|---------------|---------------|
| SOC 2       | CC6.1 — Logical Access        | At Risk       | Compliant     |
| SOC 2       | CC6.6 — Data in Transit       | At Risk       | Compliant     |
| ISO 27001   | A.14.2.1 — Secure Dev Policy  | Partial       | Compliant     |
| ISO 27001   | A.10.1 — Cryptography Policy  | Non-Compliant | Compliant     |
| GDPR        | Art. 25 — Data by Design      | At Risk       | Compliant     |
| GDPR        | Art. 32 — Security of Processing | At Risk    | Compliant     |

<Adjust rows to reflect only the controls actually affected by the findings in this review.
Remove frameworks not applicable to the project.>

---

## 8. Conclusion

<2–3 paragraphs covering:
- Summary of what was found and the overall risk level
- What was remediated and the resulting risk reduction
- Specific conditions under which the code is approved to merge — or what must be resolved first
- Explicit approval recommendation: APPROVED | APPROVED WITH CONDITIONS | NOT APPROVED>

---

## 9. Sign-Off

### Author
| Field      | Value                                   |
|------------|-----------------------------------------|
| Name       | <Firstname Lastname>                    |
| Role       | Staff Security Engineer                 |
| Email      | <email>                                 |
| Date       | <YYYY-MM-DD>                            |
| Signature  | <Firstname Lastname>                    |

### Distribution List
| Name       | Role                   | Reason                          |
|------------|------------------------|---------------------------------|
|            | Engineering Lead       | Code owner — action required    |
|            | Security Team          | FYI — findings archive          |
|            | Compliance             | FYI — compliance impact section |

---

## Appendix A — Semgrep Pro Raw Findings

| Rule ID | Location | Severity | CWE | Confidence | Assessment |
|---------|----------|----------|-----|------------|------------|
|         |          |          |     |            | TP \| FP \| NEEDS_REVIEW |

## Appendix B — Confirmed False Positives

| Rule ID | Location | Reason | Action |
|---------|----------|--------|--------|
|         |          |        | nosec comment \| rule tuning \| acceptable risk |

## Appendix C — Coverage Gaps

<Vulnerability classes or code paths that neither Semgrep nor manual review could assess confidently.
These are candidates for new Semgrep rules or integration tests.>

## Appendix D — Taint Flow Map

**Sources identified:**
**Sinks reached:**
**Sanitizers present:**
**Unsanitized paths:**
**Semgrep Pro coverage vs. manual:**
```

---

## Step 6 — Confirm Report Written

After writing the report file, confirm:

```bash
ls -lh $(git rev-parse --show-toplevel)/security-review/
```

Print the full path of the report file and a one-line summary:
`Report written: /path/to/security-review/security-code-review-report-YYYYMMDD.md — N findings (X critical, Y high, Z medium)`

Also output the `[BLOCK]` findings directly in the terminal session so the developer sees them immediately without opening the report.

---

## Review Principles

- Semgrep Pro interprocedural findings at high confidence are `[BLOCK]` unless there is a clear FP reason
- Assess exploitability and reachability — unreachable sinks are `[WARN]` not `[BLOCK]`
- Distinguish syntactic / semantic / interprocedural analysis tier on every finding
- A `[BLOCK]` finding means the code must not merge as-is
- Confirmed FPs must be documented — they are as valuable as TPs for rule quality
- Partial mitigations are often worse than none — flag incomplete controls explicitly
- Never skip a section silently — write "None identified" if a class has no findings
- The report is the deliverable — the terminal output is a summary only

