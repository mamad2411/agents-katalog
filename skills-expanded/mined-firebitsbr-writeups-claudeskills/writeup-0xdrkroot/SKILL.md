<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0xdrkroot
description: CTF writeups and security challenges by 0xDrkRoot.
---

# Writeups by 0xDrkRoot

Source repository: `/repos/0xDrkRoot`

## Repository Index

- pentest-reports/README.md
- pentest-reports/reports JuiceShop_Full_Writeup.md

## Writeup Content


### File: pentest-reports/README.md

# pentest-reports
 Personal penetration testing reports and OSCP practice writeups



### File: pentest-reports/reports JuiceShop_Full_Writeup.md

# Comprehensive Pentest Report — OWASP Juice Shop (Authorized Lab)
*Author:* darkroot
*Date:* 2025-11-2
*Scope:* OWASP Juice Shop — local lab (authorized practice only)

---

> *Warning / Legal:* All tests and examples in this report were performed in a local, authorized lab environment (OWASP Juice Shop). Do *not* execute these tests against systems you do not own or do not have explicit written permission to test.

---

## Executive Summary (for non-technical readers)
This document summarizes a practical security review performed against a local instance of OWASP Juice Shop. Juice Shop intentionally contains many of the common web application vulnerabilities used here for learning purposes. The report explains each discovered issue in plain language, shows how it was tested safely, and provides clear, actionable remediation recommendations prioritized by risk.

*Key findings (examples):*
- Insecure file upload that stores files under a public folder (High).  
- Stored and reflected XSS (Cross-Site Scripting) vulnerabilities (High / Medium).  
- Insecure Direct Object References (IDOR) / Broken Access Control (High).  
- SQL Injection on low security settings (Medium).  
- Security configurations and sensitive data exposure issues (Medium).

---

## Table of Contents
1. Environment & Tools  
2. Scope & Methodology  
3. Summary of Findings (snapshot)  
4. Detailed Findings & Remediation  
   - Reflected XSS  
   - Stored XSS  
   - SQL Injection  
   - Broken Authentication & Session Management  
   - Insecure Direct Object Reference (IDOR) / Access Control  
   - Insecure File Upload  
   - Security Misconfiguration  
   - Sensitive Data Exposure  
   - CSRF (Cross-Site Request Forgery)  
   - Outdated Components / Known Vulnerabilities  
5. Prioritized Remediation Plan  
6. Testing & Re-test Checklist (technical)  
7. Action Plan for Non-Technical Managers  
8. Useful Commands & Templates  
9. References & Learning Resources

---

## 1) Environment & Tools
*Test environment*
- Application: OWASP Juice Shop (local environment)  
- URL (local): http://localhost:3000

*Tools used*
- Browser (with developer tools)  
- *Burp Suite* (Community — proxy, Repeater)  
- *Nmap* (basic service discovery)  
- *ffuf / gobuster* (directory fuzzing)  
- *curl* / httpie (HTTP requests)  
- *sqlmap* (demo testing on lab)  
- Screenshot tool (for PoC screenshots)

---

## 2) Scope & Methodology
*Scope:* Public web endpoints of the local Juice Shop instance. No external systems were tested.

*Methodology:*  
1. Reconnaissance — nmap, directory fuzzing, review visible functionality.  
2. Manual testing — Burp Suite interception + targeted tests for common OWASP Top 10 vulnerabilities.  
3. Safe PoC creation — use non-malicious markers (e.g., TEST_MARKER_123) instead of executable payloads in the report when presenting to non-technical audiences.  
4. Documentation — capture screenshots and sanitized request/response snippets.  
5. Remediation recommendations and re-test checklist.

---

## 3) Snapshot — Summary of Findings
- *High*
  - Insecure File Upload — files stored under /uploads and accessible (High risk).  
  - Stored XSS in product reviews or feedback (High risk when widely exploited).  
  - IDOR — access to other users’ orders/receipts via predictable identifiers (High).
- *Medium*
  - Reflected XSS in search or query parameters (Medium).  
  - SQL Injection on low security settings (demo only) (Medium).  
  - Security misconfiguration: sensitive info visible in headers or error pages (Medium).  
- *Low*
  - Components with known vulnerabilities (depends on package versions) (Low→Medium).

---

## 4) Detailed Findings & Remediation

> Each vulnerability below follows this structure:
> - *What it is* (plain language)  
> - *Why it happens* (short technical reason)  
> - *How we tested it safely* (sanitized PoC)  
> - *Impact / Risk*  
> - *Remediation (actionable steps)*  
> - *How to verify fix (re-test)*

---

### A) Reflected XSS (Cross-Site Scripting) — Example: /search
*What it is (simple):* The application reflects user input back into the page without proper encoding, so malicious content could run in other users’ browsers.

*Why it happens (technical):* Input is included in HTML output without proper HTML encoding or filtering.

*Safe test (PoC):*  
- Enter a safe marker string in the search field like TEST_MARKER_XSS_001.  
- If the exact string appears unescaped in the HTML response body (visible in Browser DevTools > Response or in Burp), this indicates reflection.

*Impact:*  
- An attacker could trick a user into visiting a crafted URL that executes JavaScript in that user’s browser — possible session theft, account actions, or content spoofing.

*Remediation:*  
1. On output, apply HTML encoding for any user-supplied data (e.g., use framework templating functions that escape output).  
2. Implement a Content Security Policy (CSP) that restricts script sources.  
3. Set session cookies with HttpOnly and Secure flags.  
4. Validate input server-side as a defense-in-depth measure.

*Re-test:* Use the same safe marker; the marker should appear escaped (e.g., &lt; instead of <) and not as executable content. Confirm CSP header presence and proper cookie flags.

---

### B) Stored XSS — Example: product reviews / feedback
*What it is:* User-supplied content is stored on the server (e.g., a product review) and later rendered to other users, enabling execution of scripts for every visitor of that content.

*Why it happens:* Server stores user content and renders it later without encoding or sanitization.

*Safe test (PoC):*  
- Submit a harmless marker in a review field: STORED_MARKER_001.  
- Visit the page displaying reviews and verify whether the marker appears as HTML (unescaped).

*Impact:* Persistent cross-user attacks — more severe than reflected XSS, as it can affect many users.

*Remediation:*  
1. Sanitize and encode stored content on output.  
2. Apply input validation and canonicalization.  
3. Use a sanitizer library (e.g., DOMPurify for HTML allowed sub-sets).  
4. Content Security Policy (CSP) as additional mitigation.

*Re-test:* Post a sanitized test review and verify output is encoded/escaped and not executable.

---

### C) SQL Injection — Example: demo endpoints (low security)
*What it is:* Untrusted input is used to build database queries, allowing attackers to modify queries and retrieve or manipulate data.

*Why it happens:* Queries constructed by concatenating strings from user input without parameterization.

*Safe test (PoC):* In lab/demo mode, use a harmless test input that reveals behavior, or test only in low-security lab settings. Example marker: INJECTION_TEST_001 and verify no unexpected data returned.

*Impact:* Data disclosure, data modification, login bypass, or worst-case full DB compromise.

*Remediation:*  
1. Use parameterized queries/prepared statements (avoid string concatenation).  
2. Use ORM methods that automatically parameterize queries.  
3. Use least-privileged database accounts.  
4. Input validation and escaping as needed.

*Re-test:* Submit test input and verify no data is returned other than expected. Run dependency scanning for known vulnerable database drivers.

---

### D) Broken Authentication & Session Management
*What it is:* Weak password policies, missing HttpOnly/Secure flags, predictable password reset tokens, or missing rate limiting.

*Why it happens:* Poor authentication controls and session handling.

*Safe test (PoC):* Verify whether:
- Cookies have HttpOnly and Secure flags.  
- Password reset flows use unpredictable tokens and expire.  
- Account lockout or rate limiting exists after several failed attempts.

*Impact:* Account takeover, credential stuffing success, session hijacking.

*Remediation:*  
1. Use secure password hashing (bcrypt/Argon2).  
2. Enforce strong password policies and consider MFA.  
3. Implement rate limiting and account lockout for failed logins.  
4. Ensure password reset tokens are random and expire quickly.  
5. Set secure session cookie attributes.

*Re-test:* Validate cookie flags, try brute-force mitigation tests in a controlled lab, and validate token behavior.

---

### E) Insecure Direct Object Reference (IDOR) / Broken Access Control
*What it is:* The app allows access to objects (orders, invoices, user data) via predictable identifiers without verifying requester authorization.

*Why it happens:* No server-side authorization checks for each object access.

*Safe test (PoC):*  
- Create two test accounts (A and B).  
- Note an object ID for account B (e.g., order=2002).  
- While authenticated as A, request order=2002. If A can see B’s data, IDOR exists.

*Impact:* Data disclosure and unauthorized access to other users’ data.

*Remediation:*  
1. Enforce server-side authorization checks on every object access.  
2. Use indirect references (UUIDs or mapping tokens) where feasible.  
3. Implement access control rules and validate them in code reviews and tests.

*Re-test:* Attempt the same IDOR request after fixes; an unauthorized request should be denied (HTTP 403/404).

---

### F) Insecure File Upload
*What it is:* Uploaded files are stored under a public folder and may be accessible/executable.

*Why it happens:* No server-side validation of file type, poor storage location (webroot), and no checks for dangerous file types.

*Safe test (PoC):*  
- Upload a harmless text file named test_upload.txt.  
- Confirm it is retrievable under /uploads/test_upload.txt.

*Impact:* If upload of executable files is permitted, attacker can achieve remote code execution (RCE). Even non-executable uploads can expose sensitive data or be used for phishing.

*Remediation:*  
1. Validate MIME type server-side (do not rely on extension only).  
2. Store uploads outside the webroot or configure the web server not to execute uploads.  
3. Rename files on upload to random names and do not use user-supplied names.  
4. Limit allowed extensions and scan files for malware.  
5. Set safe file permissions (no execute) and use virus scanning.

*Re-test:* Upload a benign file and confirm it is stored safely; verify the server does not execute uploads and that access controls apply.

---

### G) Security Misconfiguration
*Examples:* Exposed stack traces, unnecessary services, missing security headers (CSP, X-Frame-Options, X-Content-Type-Options).

*Impact:* Provides attackers with information to craft more effective attacks.

*Remediation:*  
1. Disable detailed error messages in production.  
2. Add security headers: X-Frame-Options: DENY, X-Content-Type-Options: nosniff, CSP, etc.  
3. Close unnecessary ports/services and minimize public attack surface.

*Re-test:* Verify headers and error pages no longer leak detailed internals.

---

### H) Sensitive Data Exposure
*What it is:* Sensitive data (passwords, credit card data) stored or transmitted insecurely.

*Remediation:*  
1. Ensure TLS everywhere (HTTPS only).  
2. Encrypt sensitive data in storage and use proper key management.  
3. Avoid storing payment data unless necessary; use tokenization/third-party providers.

---

### I) CSRF (Cross-Site Request Forgery)
*What it is:* Actions can be performed by an authenticated user without their intent via a malicious site.

*Remediation:*  
1. Use anti-CSRF tokens on state-changing forms.  
2. Set cookie attribute SameSite appropriately.  
3. Require re-authentication for critical actions.

---

### J) Components with Known Vulnerabilities
*What it is:* Old libraries or packages that contain known CVEs.

*Remediation:*  
1. Implement dependency scanning (Snyk, Dependabot, npm audit).  
2. Maintain a patch/update schedule and test updates.

---

## 5) Prioritized Remediation Plan (what to fix first)
1. *Insecure File Uploads & Stored XSS* — fix within 7 days (High risk of RCE or widespread client impact).  
2. *IDOR / Broken Access Control* — fix within 7–14 days (High data exposure risk).  
3. *Authentication & Session hardening* — 7–14 days.  
4. *Reflected XSS, SQLi (where applicable)* — 14–30 days.  
5. *Security config & headers, dependency updates* — 14–30 days.  
6. *Ongoing: dependency scanning, automated tests, security training for devs.*

---

## 6) Testing & Re-test Checklist (technical)
- [ ] Run nmap to confirm only required ports are open.  
- [ ] Run ffuf / directory fuzzers and audit all discovered endpoints.  
- [ ] Validate all user inputs are encoded at output.  
- [ ] Confirm cookie flags: HttpOnly, Secure, and SameSite.  
- [ ] Attempt IDOR tests across sessions after fixes; expect 403 or 404.  
- [ ] Re-run dependency scans (Snyk / npm audit) and verify no critical CVEs remain.  
- [ ] Re-run XSS tests using safe markers — markers must be escaped.  
- [ ] Confirm file uploads cannot be executed and are stored outside webroot.

---

## 7) Action Plan for Non-Technical Managers
1. *Prioritize fixes:* Start with file upload, access control, and authentication fixes.  
2. *Request deadlines:* Ask dev team for estimated completion dates for each priority (7–14 days for criticals).  
3. *Require test evidence:* Each fix must be followed by a short re-test report showing before/after screenshots.  
4. *Implement monitoring:* Add logging and alerting for suspicious access (failed auth attempts, unexpected file uploads).  
5. *Training:* Schedule a short secure-coding workshop for devs focusing on input handling, auth best practices, and dependency hygiene.

---

## 8) Useful Commands & Templates

*Quick commands (lab only):*
```bash
# Nmap basic scan
nmap -sC -sV -p- localhost -oN nmap-basic.txt

# Directory fuzz (ffuf)
ffuf -u http://localhost:3000/FUZZ -w /usr/share/wordlists/dirb/common.txt -t 50 -o ffuf-results.txt

# HTTP headers
curl -s -I http://localhost:3000 | sed -n '1,20p'


##9) References & Learning Resources

OWASP Top Ten — https://owasp.org/www-project-top-ten/

PortSwigger Web Security Academy — https://portswigger.net/web-security

OWASP Juice Shop — https://owasp.org/www-project-juice-shop/

Burp Suite documentation — https://portswigger.net/burp/documentation 


