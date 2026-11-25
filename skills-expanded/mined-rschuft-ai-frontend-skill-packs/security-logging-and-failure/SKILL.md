---
name: security-logging-and-failure
description: "Assess and remediate security event logging, audit signals and resilient error handling in frontend and associated web services. Use for security event, log injection, stack trace, audit, exception, incident, error leakage."
---

# Logging, auditing and exceptional-condition risks

## Scope

Use when the task concerns **security event logging, audit signals and resilient error handling**. Common triggers include security event, log injection, stack trace, audit, exception, incident, error leakage. Do not classify unrelated symptoms as this category or expand the authorized scope. A client-side implementation may not reveal server-side enforcement.

ASVS 5.0.0 chapters: **V16**. For exact requirement wording and levels consult `../security-diagnose/references/asvs/5.0.0/index.json` and the version-pinned official ASVS source. Do not treat the index as the full standard. The local reference is `references/playbook.md`.

## Procedure

1. Establish the user action, attacker/actor, sensitive asset, trust boundary, affected runtime, and actual observed evidence.
2. Read `references/playbook.md` and the relevant ASVS chapter entries. Resolve baseline using `../security-diagnose/references/standard-selection.md` (explicit task > project policy > planning fallback).
3. Differentiate the underlying cause from superficial symptoms; select a specific applicable requirement only after checking the authoritative source text.
4. Implement or recommend the smallest verified control with the project’s existing security architecture. Prefer server-side enforcement when the failure crosses the browser trust boundary.
5. Test normal and denied paths with synthetic or approved fixtures, documenting exact methods and evidence. Record residual unknowns; route broad assessments to `security-review`, implementation to `security-build` and retesting to `security-validate`.

## Failure discipline

- Not every exception is an attack and not every 200 status means success.
- Avoid leaking PII or session tokens into monitoring systems.
- Logs alone do not enforce an authorization decision.

No active probing of live systems, aggressive scanning, credential handling or cross-tenant requests without explicit authorization. Never report security certification from this skill alone.
