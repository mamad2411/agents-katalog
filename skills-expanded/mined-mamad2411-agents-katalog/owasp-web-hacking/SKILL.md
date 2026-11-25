---
name: owasp-web-hacking
description: Use when performing web application security testing, bug bounty hunting, penetration testing, or researching web vulnerabilities. Covers all OWASP WSTG v4.2 categories: information gathering, configuration, identity, authentication, authorization, session management, input validation (XSS, SQLi, SSRF, SSTI, XXE, LFI, RFI, command injection, etc.), error handling, cryptography, business logic, client-side attacks, and API testing.
---

# OWASP Web Application Security Testing (WSTG v4.2)

## Overview

Comprehensive reference for web application security testing based on the OWASP Web Security Testing Guide v4.2. Covers all 12 test categories with techniques, payloads, tools, and methodologies.

**Test ID Format:** `WSTG-<CATEGORY>-<NN>` (e.g., `WSTG-INPV-05` = SQL Injection)

**Core methodology phases:**
1. Reconnaissance → 2. Enumeration → 3. Vulnerability Identification → 4. Validation → 5. Exploitation (if authorized) → 6. Reporting

## How to Use This Skill

This skill is split across category files. Load the file matching the test you are performing:

| Category | File | Coverage |
|----------|------|----------|
| 4.1 Information Gathering (INFO) | [info-information-gathering.md](info-information-gathering.md) | Search engine recon, fingerprinting servers/frameworks, metafiles, app enumeration, entry-point mapping, architecture mapping |
| 4.2 Configuration & Deployment (CONF) | [conf-configuration-deployment.md](conf-configuration-deployment.md) | Network/platform config, file extensions, backup files, admin interfaces, HTTP methods, HSTS, RIA policies, subdomain takeover, cloud storage |
| 4.3 Identity Management (IDNT) | [idnt-identity-management.md](idnt-identity-management.md) | Role definitions, account enumeration |
| 4.4 Authentication (ATHN) | [athn-authentication.md](athn-authentication.md) | Credential transport, default creds, lockout, auth bypass, remember-me, browser cache, password policy, security questions, password reset |
| 4.5 Authorization (ATHZ) | [athz-authorization.md](athz-authorization.md) | Directory traversal/LFI wrappers, authz bypass, privilege escalation, IDOR |
| 4.6 Session Management (SESS) | [sess-session-management.md](sess-session-management.md) | Token schema, cookie attributes, fixation, exposed variables, CSRF, logout, timeout, session puzzling, hijacking |
| 4.7 Input Validation (INPV) | [inpv-input-validation.md](inpv-input-validation.md) | Reflected/Stored XSS, verb tampering, HPP, SQLi (MySQL/MSSQL/PostgreSQL/Oracle/MS Access/NoSQL/ORM), LDAP, XXE, SSI, XPath, IMAP/SMTP, Code injection/LFI/RFI, Command injection, Format string, Incubated, HTTP splitting/smuggling, Host header, SSTI, SSRF |
| 4.8 Error Handling (ERRH) | [errh-error-handling.md](errh-error-handling.md) | Improper error handling |
| 4.9 Cryptography (CRYP) | [cryp-cryptography.md](cryp-cryptography.md) | Weak TLS, padding oracle, weak encryption |
| 4.10 Business Logic (BUSL) | [busl-business-logic.md](busl-business-logic.md) | Data validation, forged requests, process timing, workflow circumvention, file upload (unexpected/malicious) |
| 4.11 Client-Side (CLNT) | [clnt-client-side.md](clnt-client-side.md) | DOM XSS, CSS injection, CORS, clickjacking, WebSockets, postMessage, browser storage, XSSI |
| 4.12 API Testing (APIT) | [apit-api-testing.md](apit-api-testing.md) | GraphQL |
| Cross-cutting reference | [reference.md](reference.md) | Payload encoding cheat sheet, full tools reference, complete WSTG test ID lookup |

## Decision Flow

```
What are you testing?
├─ Mapping the target (passive/active recon)   → info-information-gathering.md
├─ Server/platform configuration weaknesses    → conf-configuration-deployment.md
├─ User identification / enumeration           → idnt-identity-management.md
├─ Login / credential security                 → athn-authentication.md
├─ Access control / permissions / IDOR         → athz-authorization.md
├─ Cookies / sessions / CSRF                   → sess-session-management.md
├─ Any injection / payload-based input attack  → inpv-input-validation.md
├─ Error messages / stack traces               → errh-error-handling.md
├─ TLS / crypto / hashing                      → cryp-cryptography.md
├─ Race conditions / workflow / file upload    → busl-business-logic.md
├─ Browser-side attacks / DOM / CORS / iframe  → clnt-client-side.md
└─ GraphQL / API-specific                      → apit-api-testing.md
```

For tool selection, payload encoding bypasses, or test ID lookup, always consult [reference.md](reference.md).

## Reporting Each Finding

For every confirmed vulnerability, document:
- Summary
- Affected asset
- Severity (CVSS or qualitative)
- CWE (if known)
- Reproduction steps
- Proof of concept
- Impact / attack path / prerequisites / likelihood
- Remediation
- References

## OPSEC

- Prefer passive enumeration first; avoid noisy scans unless requested.
- Warn before destructive, irreversible, or DoS-prone actions.
- Distinguish lab-safe vs. production-safe behavior.
- Do not perform exploitation without explicit written authorization.
- Stay strictly within scope.
