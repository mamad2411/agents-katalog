---
name: "security-audit-lite"
description: "Perform a practical security review focused on auth, secrets, insecure defaults, injection risks, trust boundaries, privilege escalation, token handling, and sensitive data exposure. Use when a user asks for a lightweight security audit, AppSec review, auth or secret handling review, or as part of $full-test-suite."
---

# Security Audit Lite

Run a practical appsec pass that finds confirmed security issues without expanding into a full threat model unless the user asks.

## Workflow

1. Identify sensitive surfaces: auth, payments, webhooks, admin paths, secrets, PII, file or network access, and config.
2. Trace trust boundaries and privilege assumptions end to end.
3. Inspect for concrete failures such as missing authorization, unsafe secret handling, injection opportunities, insecure defaults, weak validation, and sensitive logging.
4. Promote only confirmed security findings into `project-audit-findings.md`.
5. If fixes are in scope, validate with targeted checks and record evidence before resolution.

## Focus Areas

- authentication and authorization mismatches
- secret leakage in code, logs, configs, or sample files
- injection or unsafe interpolation
- insecure transport, token storage, or replay handling
- overbroad permissions or privilege escalation paths
- unsafe defaults or missing environment guards

## Rules

- Use `blocked` or `needs-context` when exploitability depends on missing runtime context.
- Keep findings concrete and avoid broad fear-based language.
- If the request becomes a full threat model, prefer `$security-threat-model` separately.

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- Severity rubric: `../_shared-project-ops/references/severity-rubric.md`
- Verification template: `../_shared-project-ops/references/verification-template.md`
