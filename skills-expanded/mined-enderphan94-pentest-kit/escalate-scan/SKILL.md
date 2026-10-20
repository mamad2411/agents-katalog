---
name: escalate-scan
description: >
  Reads one or more pentest scan reports (front-end-scan, stress-scan, server-scan output)
  and performs finding consolidation: merges all findings, deduplicates by URL+title,
  re-verifies each finding using class-specific automated verification (Mythos method —
  skips already-verified stress-scan findings), categorizes by severity, assesses business
  impact, and generates CVSS 3.1 scores. Outputs a verified, scored, deduplicated findings
  file for chain-scan and exploit-scan to consume.
  Use when the user invokes "escalate-scan", "escalation scan", "verify findings",
  "re-verify findings", "score findings", "CVSS scoring", or passes
  "--report <path>" arguments to combine and verify scan results.
---

# Escalation Scan — Finding Verification & CVSS Scoring

## Purpose

Take the findings from one or more completed scan reports (front-end-scan, stress-scan,
server-scan) and:
1. **Merge & deduplicate** — unified findings list from all scans
2. **Re-verify** each finding to confirm it is real and not a false positive
3. **Assess business impact** — what can an attacker actually achieve?
4. **CVSS score** every finding
5. Output a **verified findings report** for chain-scan and exploit-scan

All verification steps remain **passive read/observe only**.

> **This skill focuses on verification and scoring.** Chaining analysis is handled by
> chain-scan (step 5). POC writing and final reporting are handled by exploit-scan (step 6).

## Scan Progress Checklist

```
Escalation Progress:
- [ ] Step 0:   Report loading, validation, and scope confirmation
- [ ] Step 1:   Finding categorization and priority queue
- [ ] Step 2:   Re-verification of all findings (max 2 requests per finding)
- [ ] Step 3:   Business impact assessment
- [ ] Step 3b:  Reportability gate (5-question filter)
- [ ] Step 4:   CVSS 3.1 scoring
- [ ] Step 5:   Verified findings report compiled (JSON + Markdown in reports/)
```

---

## Step 0 — Argument Parsing & Report Loading

1. The user should invoke this skill with one or more report paths, e.g.:
   ```
   escalate-scan --report reports/report_frontend_20240115_120000.json
   escalate-scan --report reports/report_stress_*.json --report reports/report_frontend_*.json
   ```
2. If no `--report` argument is provided, list all JSON files in `reports/` and ask the
   user to specify which to use.
3. For each report file:
   - Validate it exists and is valid JSON matching `templates/report_schema.json`
   - Extract: `scan_type`, `target`, `timestamp`, and full `findings` list
4. Merge all findings into a unified list, deduplicating by `affected_url + title`.
   When duplicates exist, keep the one with `verified: true` if available.
5. **Check `OUT_OF_SCOPE_VULNS`** in `scope.txt`. If set, remove any findings whose
   vulnerability class matches an out-of-scope entry. Log: "Excluded N findings
   matching out-of-scope classes: <list>". These findings are dropped entirely —
   they do not appear in the final report, not even as informational.
6. Print a summary: "Loaded N findings from M reports for target: <target>"

---

## Step 1 — Finding Categorization & Priority Queue

Triage the merged findings:

1. **Group by severity**: Critical → High → Medium → Low → Info
2. **Identify clusters** — findings on the same endpoint/feature (flag for chain-scan)
3. **Mark high-value targets**:
   - Auth endpoints (login, password reset, token refresh)
   - Admin panels
   - File upload/download endpoints
   - Payment or PII-handling endpoints
   - API endpoints returning user lists or sensitive data
4. Create an escalation priority list — process Critical and High findings first.
5. **Tag findings by primitive type** for chain-scan:
   - Read primitives: SSRF, LFI, info disclosure, IDOR (read), exposed secrets
   - Write primitives: stored XSS, CSRF, file upload, IDOR (write)
   - Auth primitives: rate limit bypass, weak JWT, session fixation, missing CSRF token
   - Access primitives: 403 bypass, subdomain takeover, cloud bucket exposure

Print the priority list before proceeding.

---

## Step 2 — Re-Verification of Each Finding

For each finding in the priority queue, re-verify it is not a false positive.

### Mythos Automated Verification

**CRITICAL RULE: NEVER trust pre-verified status blindly.**
- **Critical and High findings**: ALWAYS re-verify regardless of `verified: true` flag.
  The previous agent may have made assumptions (e.g., 200 status ≠ accessible).
- **Medium findings**: re-verify if `verification_output` is empty or missing.
- **Low/Info findings**: may skip re-verification if `verification_output` is present and convincing.

### Authentication Barrier Detection (MANDATORY for all re-verification)

When re-verifying ANY finding, check the response for authentication barriers:
```
curl -sk --max-time 10 "$affected_url" | grep -iE \
  "password|pin.*code|enter.*pin|login.*required|sign.*in|unauthorized|forbidden|
   <input.*type=.password|WWW-Authenticate|oauth.*redirect|access.*denied"
```
If ANY auth barrier is detected → mark `verified: false`,
`verification_note: "auth barrier detected: <what was found>"`.
A 200 response with a PIN prompt is NOT a verified unauthenticated finding.

### HTTP engine selection

When `BURP_ENABLED=1` is set in the environment (see `scope.txt`), use Burp's
MCP HTTP engine instead of `curl` for all verification probes in this step:

```
mcp__burp__send_http1_request   ← preferred when BURP_ENABLED=1
curl -sk                        ← fallback when BURP_ENABLED is empty/0
```

The Burp engine handles cert pinning, sticky sessions, proxy-aware encoding,
and WAF interaction more accurately than naked `curl`. Each request also
populates Burp's site map and runs through its passive scanner — so a
re-verification request can incidentally surface NEW findings that flow back
to Phase 4.

The class-specific verification logic below stays the same regardless of
HTTP engine — only the request transport changes. If Burp is unreachable
mid-step, fall back to `curl` and continue. Do not abort verification.

For findings that pass the auth barrier check, apply class-specific verification:

- **XSS findings**: `curl -sk "<poc_url>"` (or `mcp__burp__send_http1_request`) → grep for reflected payload in response body.
  **Verified** if payload appears unencoded in an executable HTML context (inside `<script>`,
  event handler, or unquoted attribute). Check `Content-Type: text/html`.
- **SQLi findings**: send baseline request vs. payload request → compare response length.
  **Verified** if responses differ by >10% OR response contains SQL error strings
  (`syntax error`, `mysql`, `postgresql`, `ORA-`, `ODBC`).
- **CORS findings**: `curl -sI -H "Origin: https://evil.attacker.com" "$url"` →
  **Verified** if `Access-Control-Allow-Origin` echoes attacker origin AND
  `Access-Control-Allow-Credentials: true`.
- **SSRF findings**: re-send with fresh OOB host → **Verified** if callback received.
- **Header/misconfig findings**: `curl -sI "$url"` → **Verified** if header still
  missing/misconfigured in current response.
- **Secret findings**: `curl -sk "$url" | grep "$secret_pattern"` → **Verified** if
  secret still present in current response.
- **Rate limit findings**: 3 rapid POST probes → **Verified** if no 429 or rate-limit header.
- **LFI findings**: `curl -sk "$url../../etc/passwd"` → **Verified** if response contains `root:x:`.
- **Open redirect findings**: `curl -sI "$redirect_url"` → **Verified** if Location header
  points to attacker-controlled domain.
- **Subdomain takeover**: `dig CNAME "$subdomain"` → **Verified** if CNAME points to
  unclaimed service AND target returns error/default page.

Mark each finding:
- `verified: true/false`
- `verification_method: "automated" | "manual" | "pre-verified"`
- Save verification output to `assets/verify_<finding_id>_<timestamp>.txt`

**Rate limit on re-verification**: max 2 requests per finding, 1 second between requests.

### Step 2f — Horizontal Privilege Escalation Re-Verification

For every finding with `vuln_class` of `idor`, `bola`, or `access_control`:

1. Check if `CREDENTIAL_SETS` is configured with ≥ 2 accounts:
   ```bash
   source skills/stress-scan/script/build_sessions.sh
   ```

2. If `SESSION_B` is available:
   a. Extract `affected_url` and the resource ID parameter from the finding JSON.
   b. Fetch with Account A and Account B:
      ```bash
      A_RESP=$(curl -sk -H "Authorization: $SESSION_A" "$AFFECTED_URL")
      B_RESP=$(curl -sk -H "Authorization: $SESSION_B" "$AFFECTED_URL")
      ```
   c. Compare responses with `diff`. Confirmed horizontal priv esc if:
      - `B_STATUS = 200` AND
      - `B_RESP` contains user-specific data from Account A (not just public content)
   d. If confirmed: set `verified: true`, upgrade severity to minimum **High**.
   e. Set `evidence_type: exploitation` and update `verification_output` with the
      actual Account B response excerpt.

3. If `SESSION_B` is NOT available:
   - Append note: "Horizontal privilege escalation untested — configure CREDENTIAL_SETS
     with two accounts for complete BOLA/IDOR validation"
   - Do not change `verified` status.

---

## Step 3 — Business Impact Assessment

For each verified finding, assess:

1. **Confidentiality impact**: Can attacker access data they shouldn't?
   - None / Low (non-sensitive) / Medium (PII, personal data) / High (credentials, payment, full DB)
2. **Integrity impact**: Can attacker modify data?
   - None / Low / Medium / High
   - (Even if we can't write, can XSS/CSRF allow user actions?)
3. **Availability impact**: Can service be disrupted?
   - None / Low / High
4. **Attacker prerequisites**: Unauthenticated / Authenticated user / Admin / Physical access
5. **Attack complexity**: Low (reproducible) / High (requires specific conditions)
6. **Business scenario narrative**: Write a plain-English attack story:
   - "An unauthenticated attacker who visits the application can..."
   - "A malicious authenticated user can..."

---

## Step 3b — Reportability Gate

After business impact assessment, run every verified finding through the **reportability gate**.
All 5 questions must pass for a finding to be marked `reportable: true`. Findings that fail
are kept in the report but marked `reportable: false` with the reason.

### The 5 Reportability Questions

For each verified finding, answer YES or NO:

**Q1 — Is the impact real and demonstrable?**
- Can you show actual data exposure, not just a theoretical risk?
- Does the POC produce concrete evidence (leaked data, modified state, callback received)?
- A missing header alone is NOT real impact unless it enables a demonstrated attack
- `NO` → mark `reportable: false`, reason: `"theoretical_only"`

**Q2 — Is it exploitable without unrealistic conditions?**
- Can an attacker exploit this without physical access, insider knowledge, or MITM on TLS?
- Does it require victim interaction? (acceptable for XSS/CSRF, not for "attacker needs admin access")
- Would it work against a real user, not just a security tester's contrived setup?
- `NO` → mark `reportable: false`, reason: `"unrealistic_prerequisites"`

**Q3 — Is it novel (not a known limitation or by-design behavior)?**
- Is this documented as a known issue or accepted risk in the target's security policy?
- Is this a standard framework behavior (e.g., Django debug mode = known in development)?
- Would the target's security team already know about this?
- Check: error messages, version numbers, and missing optional headers are often accepted risks
- `NO` → mark `reportable: false`, reason: `"known_limitation"`

**Q4 — Is the affected asset in scope and owned by the target?**
- Is the vulnerable URL on a domain the target owns (not a third-party CDN, analytics, or widget)?
- Is it on a production asset (not a staging/dev/test environment unless explicitly in scope)?
- Would the target's security team have authority to fix this?
- `NO` → mark `reportable: false`, reason: `"out_of_scope_asset"`

**Q5 — Does it meet the severity bar?**
- Critical/High: always reportable if Q1-Q4 pass
- Medium: reportable if impact is clearly articulated
- Low: reportable only if it contributes to a chain or has clear security relevance
- Info: NOT reportable as a standalone finding — keep for chain analysis only
- `NO` → mark `reportable: false`, reason: `"below_severity_bar"`

### Common False Reportability Patterns (auto-reject)

These are frequently reported but rarely accepted — auto-mark `reportable: false`:

| Pattern | Why It Fails | Gate |
|---|---|---|
| Missing `X-Frame-Options` on API endpoint returning JSON | JSON can't be framed meaningfully | Q1 |
| Missing `CSP` on static marketing page with no user input | No injection surface | Q1 |
| `Server: nginx/1.x` version disclosure | Version alone is not exploitable | Q1 |
| Self-XSS (only exploitable by the victim on their own session) | No attacker path | Q2 |
| Clickjacking on logout page | No impact from framing a logout | Q1 |
| Missing `Secure` flag on non-session cookie | No sensitive data in cookie | Q1 |
| Rate limiting absent on non-auth endpoint | No credential stuffing risk | Q1 |
| CORS allowing `null` origin without credentials | Cannot steal data | Q1 |
| Open redirect on non-auth domain (no OAuth) | No token theft path | Q1 |
| `X-Powered-By: Express` header | Framework disclosure, not exploitable | Q5 |
| Exposed endpoint requiring PIN/password/MFA | Not actually unauthenticated | Q2 |
| Debug console with authentication enabled (PIN-protected Werkzeug) | Requires PIN to execute code | Q2 |
| Admin panel returning 200 but showing login form | Not an exposed admin panel | Q2 |
| API endpoint returning 200 but with `"error": "unauthorized"` in body | Not accessible | Q2 |
| "Exposed" page that only shows public/marketing content | No sensitive data | Q1 |
| Finding with `evidence_type: code_analysis` reported as verified | Code pattern found but never triggered via HTTP — needs manual testing | Q1 |
| Finding with `evidence_type: inferred` at High/Critical severity | Technology assumption without exploitation evidence — cap at Medium | Q1 |
| Finding referencing URLs/endpoints never observed in scan data | Attack surface assumed, not confirmed — no crawled evidence | Q1 |

### Evidence Type Enforcement (MANDATORY)

**Every finding MUST have `evidence_type` classified.** If missing from the input
report, classify it during escalate-scan:
- `"exploitation"` — curl/tool output proves the vuln (HTTP response captured)
- `"code_analysis"` — vulnerable code pattern found in JS/source but NOT triggered
- `"inferred"` — assumed based on library version, tech stack, or config

**Rules**:
- Only `evidence_type: "exploitation"` findings can remain `verified: true`
- `code_analysis` findings → force `verified: false`, add note: "code pattern found,
  not exploitable via HTTP probe — requires authenticated/manual testing"
- `inferred` findings → force `verified: false`, cap severity at Medium

### Enforcement Rule (MANDATORY)

**Every finding in the final output MUST have a populated `reportability_gate` object.**
If `reportability_gate` is missing or empty → the finding was not properly assessed and
must be re-evaluated before inclusion. A finding with `reportability_gate: null` is a
**skill bug** — it means the gate was skipped.

### Output

Add to each finding in the JSON:
```json
{
  "reportable": true,
  "reportability_gate": {
    "q1_real_impact": true,
    "q2_exploitable": true,
    "q3_novel": true,
    "q4_in_scope": true,
    "q5_severity_bar": true
  }
}
```

Or for rejected findings:
```json
{
  "reportable": false,
  "reportability_gate": {
    "q1_real_impact": false,
    "rejection_reason": "theoretical_only",
    "rejection_detail": "Missing X-Frame-Options on JSON API — no frameable content"
  }
}
```

Print gate summary:
```
Reportability Gate:
  Passed: N findings (reportable)
  Failed: N findings (kept for chain analysis)
    - theoretical_only:          N
    - unrealistic_prerequisites: N
    - known_limitation:          N
    - out_of_scope_asset:        N
    - below_severity_bar:        N
```

---

## Step 4 — CVSS 3.1 Scoring

For each finding, assign a CVSS 3.1 score.

Base score components:
- **AV** (Attack Vector): Network(N) / Adjacent(A) / Local(L) / Physical(P)
- **AC** (Attack Complexity): Low(L) / High(H)
- **PR** (Privileges Required): None(N) / Low(L) / High(H)
- **UI** (User Interaction): None(N) / Required(R)
- **S** (Scope): Unchanged(U) / Changed(C)
- **C/I/A** (Impact): None(N) / Low(L) / High(H)

Provide the CVSS vector string: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N`
And calculate the numeric score (use standard CVSS 3.1 formula or estimate).

See `references/escalation_techniques.md` for common CVSS patterns.

---

## Step 5 — Output Verified Findings Report

Generate `reports/report_escalated_<YYYYMMDD_HHMMSS>.json` + `.md`.

### JSON structure

```json
{
  "scan_type": "escalated",
  "target": "<target>",
  "timestamp": "YYYYMMDD_HHMMSS",
  "source_reports": ["report_stress_*.json", "report_frontend_*.json"],
  "stats": {
    "total_loaded": 0,
    "duplicates_removed": 0,
    "verified": 0,
    "unverified": 0,
    "false_positives": 0,
    "by_severity": {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Info": 0}
  },
  "findings": [
    {
      "id": "ESC-001",
      "title": "...",
      "severity": "Critical",
      "cvss_score": 9.8,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
      "affected_url": "...",
      "evidence": "...",
      "verified": true,
      "verification_method": "automated",
      "original_scan": "stress-scan",
      "original_id": "ST-003",
      "primitive_type": "read|write|auth|access",
      "business_impact": {
        "confidentiality": "High",
        "integrity": "None",
        "availability": "None",
        "prerequisites": "Unauthenticated",
        "complexity": "Low",
        "narrative": "An unauthenticated attacker can..."
      },
    }
  ]
}
```

### Markdown summary

Include: findings table (ID, title, severity, CVSS, verified status, URL),
business impact summary, false positives appendix, verification stats.

### Handoff

Print:
```
=== escalate-scan complete ===
  Findings: N total (X verified, Y false positives)
  Critical: N   High: N   Medium: N   Low: N   Info: N
  Report:   reports/report_escalated_<timestamp>.json

  Next step: run chain-scan --report reports/report_escalated_<timestamp>.json
======
```

---

## Safety Rules (Non-negotiable)

- **NO new attack probes** beyond re-verification (max 2 requests per finding)
- **NO execution of exploit code** — verification is read-only observation
- **NO submission of payloads** to the target during verification
- **NO requests to URLs outside the original target scope**
- All verification evidence saved to `assets/` only
