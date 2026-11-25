---
name: security-browser-and-origin
description: "Review browser security boundaries, CSP, cookies, CORS, CSRF, framing, and third-party scripts. Use when browser origin protections are implicated."
---

# Browser trust boundary and origin risks

## Scope

Use when the task concerns **browser security, dom sinks, csp, cookies, origin separation and third-party scripts**. Common triggers include CSP, CORS, CSRF, clickjacking, iframe, browser storage, third-party script, XSS DOM. Do not classify unrelated symptoms as this category or expand the authorized scope. A client-side implementation may not reveal server-side enforcement.

ASVS 5.0.0 chapters: **V3**. For exact requirement wording and levels consult `../security-diagnose/references/asvs/5.0.0/index.json` and the version-pinned official ASVS source. Do not treat the index as the full standard. The local reference is `references/playbook.md`.

## Procedure

1. Establish the user action, attacker/actor, sensitive asset, trust boundary, affected runtime, and actual observed evidence.
2. Read `references/playbook.md` and the relevant ASVS chapter entries. Resolve baseline using `../security-diagnose/references/standard-selection.md` (explicit task > project policy > planning fallback).
3. Differentiate the underlying cause from superficial symptoms; select a specific applicable requirement only after checking the authoritative source text.
4. Implement or recommend the smallest verified control with the project’s existing security architecture. Prefer server-side enforcement when the failure crosses the browser trust boundary.
5. Test normal and denied paths with synthetic or approved fixtures, documenting exact methods and evidence. Record residual unknowns; route broad assessments to `security-review`, implementation to `security-build` and retesting to `security-validate`.

## Failure discipline

- CORS is not authentication or CSRF prevention by itself.
- Security headers require examination of actual HTTP responses.
- Do not claim complete XSS protection solely from a CSP header.

No active probing of live systems, aggressive scanning, credential handling or cross-tenant requests without explicit authorization. Never report security certification from this skill alone.
