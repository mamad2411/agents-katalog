---
name: root-path-exposure-assessment
description: >
  Use for authorized pentest/bug-bounty recon to assess whether a target
  exposes or permits unauthenticated discovery of its filesystem/document
  root (path disclosure via errors, directory listing, misconfig). Stops
  immediately once root-path exposure is proven; never accesses private
  files/data/credentials. Requires written authorization/bug-bounty scope.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  category: engineering
  domain: security-audit
  updated: 2026-09-13
  tags: [security, pentest, bug-bounty, information-disclosure, responsible-disclosure]
---
# Root Path Exposure Assessment

## Objective

Assess whether an authorized security-testing target exposes or permits unauthenticated discovery of its filesystem/document-root path.

**IMPORTANT:** This assessment must STOP after proving root-path exposure. Do not download, copy, dump, enumerate, or inspect private application data.

**Prerequisite:** Confirm written authorization / bug-bounty scope for the target before testing. If none exists, stop and tell the user to obtain it first.

---

## Test For

1. Publicly exposed filesystem paths
2. Directory listing
3. Error messages revealing absolute paths
4. Debug/stack-trace path disclosure
5. Web-server misconfiguration
6. Backup/configuration path disclosure
7. Predictable document-root exposure
8. Path disclosure through publicly accessible application responses

If a path such as:

```text
/home/username/public_html
/var/www/html
/srv/www/example
/opt/application
```

can be reliably identified without authentication, record:

* Target
* Discovered path
* Discovery method
* HTTP response/status if applicable
* Minimal non-sensitive evidence
* Security impact
* Severity
* Recommended remediation

---

## DO NOT

* Access private files
* Download source code
* Access databases
* Read credentials/secrets
* Dump environment variables
* Read `.env` files
* Access private backups
* Modify files
* Escalate privileges
* Bypass authentication
* Brute-force credentials
* Continue deeper after root exposure is proven

---

## Stop Condition

Once the filesystem/document root is reliably identified, **STOP TESTING THAT VECTOR.**

---

## Report Format

Generate a finding titled **"Potential Filesystem Path Disclosure"** with:

```text
Finding:
Evidence:
Impact:
Severity:
Remediation:
Responsible Disclosure Recommendation:
```

The purpose is to demonstrate:

> "If an unauthorized user can discover the application's filesystem root, the organization should investigate whether additional sensitive resources could subsequently become exposed."

Never claim that source code or company data is compromised unless it was actually and legitimately accessed under explicit authorization.

---

## Important Distinction

Discovering a root path is not full server compromise. But an unauthenticated leak of the filesystem root is itself an information-disclosure vulnerability, and the report may recommend the organization investigate whether further exposure exists beyond it.

Always verify bug-bounty scope / written authorization for the target before testing, so the resulting report is a genuinely defensible white-hat assessment.

---

## Boundary on URL-Only Input

Given only a target URL, this skill does NOT run automated cPanel/root-path guessing against a company that hasn't confirmed authorization — that operationalizes unauthorized reconnaissance. Confirm scope/authorization first (see Prerequisite above).

Once authorization is confirmed, the test stays **passive/non-invasive** — reading what the target already publicly returns, not probing or guessing:

```text
INPUT
https://target.example
        ↓
Passive / non-invasive analysis
        ↓
Can publicly available responses reveal:
- hosting provider
- web server
- document-root indicators
- absolute filesystem paths
- cPanel-related exposure
- error/debug path disclosure
- directory listing
- accidental configuration exposure
        ↓
YES → record minimal evidence
NO  → report "No root-path disclosure detected"
        ↓
STOP
```

If no path is directly confirmed by a response (only inferred from indirect signals), report it as **"inferred/potential root path"**, never as a confirmed one.

## Evidence-Based Report Template

Use this for the finding once real evidence exists (an actual response/error/header/screenshot that itself reveals the path):

```text
Finding:
Filesystem / Document Root Disclosure

Target:
https://example.com

Exposed Path:
[exact path discovered during authorized testing]

Evidence:
[the exact URL/request/response or screenshot that revealed the path]

Impact:
An unauthorized user may be able to infer the server's filesystem structure.
Further investigation is recommended to determine whether sensitive resources
are exposed.

Severity:
[Low/Medium/High — based on actual exposure]

Recommended Fix:
Disable verbose error messages/debug output, prevent directory listing,
remove path-disclosing responses, and review web-server/document-root
configuration.

Proof:
The following evidence demonstrates the path disclosure without accessing,
downloading, or modifying private application data.
```
