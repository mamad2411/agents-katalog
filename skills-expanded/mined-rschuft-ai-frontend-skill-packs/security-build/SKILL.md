---
name: security-build
description: "Implement secure web application, browser and API changes using OWASP ASVS 5.0.0 requirements and specialist remediation patterns. Use during frontend or connected service coding and targeted vulnerability fixes."
---

# Implement a focused application security improvement

## Scope

Use only for security improvements requested or needed in the authorized coding task. Preserve the existing architecture, release constraints and identity/security ownership. Changes to authentication, authorization or cryptography require corresponding server-side enforcement and tests.

## Procedure

1. Determine the protected asset, threat model, actual trust boundary, affected ASVS requirement and relevant owned code paths; distinguish user-requested scope from proposed methods.
2. Read matching specialist `references/playbook.md` and selected ASVS identifier metadata from `../security-diagnose/references/asvs/5.0.0/index.json`; consult exact upstream ASVS requirement text before claiming satisfaction.
3. Prefer established project mechanisms, secure defaults, native platform protections, maintained dependencies and minimal change surface; do not introduce homegrown cryptography or authentication.
4. Implement functional and negative cases for authorized/unauthorized roles, malformed input, stale sessions, errors and data exposure as appropriate. Ensure browser-only controls are not substituted for server/API enforcement.
5. Run focused relevant tests/scans or mark them untested; record source diff, independent tool evidence, residual risk and rollback information. Use `security-validate` for verification.

## Safe execution

Do not launch active scans against external or production targets without explicit authorization. Do not disable checks, suppress alerts, publish secrets, or broaden privileges to make tests pass. Report changes that require security-owner approval.
