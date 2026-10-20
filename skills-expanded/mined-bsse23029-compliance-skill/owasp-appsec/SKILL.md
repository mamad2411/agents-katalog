---
name: owasp-appsec
description: OWASP application security requirements for this product — ASVS 5.0 as the verifiable requirement source, Top 10:2025 for risk framing, and the API Security Top 10 for the multi-tenant CRUD API. Use for secure code review, appsec gap analysis, or when choosing which security requirements to hold a module to.
---

# OWASP application security

Registry: `OWASP-ASVS`, `OWASP-TOP10`, `OWASP-API-TOP10`.

Division of labour:

- **ASVS 5.0** — the *requirements* source. Testable, numbered, gradeable. This is what the grid
  cites for application security.
- **Top 10:2025** — risk *awareness*. Good for prioritising and for communicating with
  non-engineers. Never cite it as a requirement; "we comply with the Top 10" is not a statement.
- **API Security Top 10 (2023)** — the risk list that actually predicts how this system breaks.

## ASVS 5.0 — mind the renumbering

Released **30 May 2025**. ~350 requirements across 17 chapters; the largest revision in ASVS
history, restructured for cloud-native architectures and automation. **The numbering changed
substantially from 4.0.3 — old V-numbers are not portable.** If you find a 4.x reference in older
project docs, re-map it rather than carrying it forward.

Pick a level and state it: L1 (baseline), L2 (most applications handling sensitive data — the right
target for this product), L3 (highest assurance). Grading against an unstated level is meaningless.

Chapters that carry the most weight here: authentication, session management, authorization,
validation/sanitisation, cryptography, secure communication, data protection, files and resources,
configuration, and the API chapter.

## API Security Top 10 — the decisive list for this codebase

This product exposes generated CRUD (`Src/Apis/GeneratedApis/`) plus ~40 project-specific API
modules, multi-tenant, permission-driven. That is precisely the shape the API list was written for:

| Risk | Why it matters here |
|---|---|
| API1 Broken Object Level Authorization (BOLA) | Any endpoint taking an id must check tenant *and* role ownership. The single highest-likelihood serious bug in this system |
| API2 Broken Authentication | JWT lifetime/renewal, OTP flows, session revocation |
| API3 Broken Object Property Level Authorization | Mass assignment and over-exposure — generated CRUD returning whole rows including `passport_number` |
| API4 Unrestricted Resource Consumption | `express-rate-limit` present; confirm it is actually applied to guest and auth endpoints |
| API5 Broken Function Level Authorization | Admin functions reachable by non-admin roles; UI-only permission hiding |
| API6 Unrestricted Access to Sensitive Business Flows | Booking, refund and cancellation abuse |
| API7 SSRF | Any URL fetched from user input, including webhooks and file imports |
| API8 Security Misconfiguration | Headers, CORS, verbose errors |
| API9 Improper Inventory Management | Undocumented, deprecated and test endpoints — `Src/Apis/TestApis/` deserves a look |
| API10 Unsafe Consumption of APIs | Trusting OTA, gateway and AI responses without validation |

## Top 10:2025 — what changed

Final version released January 2026 after the November 2025 announcement. Two new categories:

- **A03:2025 Software Supply Chain Failures** — broader than the old "vulnerable components"; covers
  the build pipeline itself. Route to `secure-sdlc-supply-chain` and `cicd-compliance`.
- **A10:2025 Mishandling of Exceptional Conditions** — error handling as a security property:
  fail-open paths, swallowed exceptions, information leakage in errors. Worth a specific pass over
  the payment, fiscalisation and Shomoos transmission paths, where a swallowed error is both a
  security and a legal failure.

## How to use in the grid

Cite `OWASP-ASVS` plus the chapter and requirement for anything testable; cite `OWASP-API-TOP10`
plus the API-n code for the tenancy and authorisation rows. Use `OWASP-TOP10` only in the summary
narrative. Frontend and backend get separate rows with the same requirement where both apply.
