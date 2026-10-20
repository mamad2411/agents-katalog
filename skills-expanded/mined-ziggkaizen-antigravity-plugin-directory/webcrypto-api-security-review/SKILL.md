---
name: webcrypto-api-security-review
description: Reviews WebCrypto API usage for security issues, weak primitives, key leaks, IV or nonce misuse, runtime assumptions, XSS exposure, storage risks, URL leakage, console logging, and incomplete tests. Use before merging or releasing cryptographic code.
license: MIT
---

# WebCrypto API Security Review

Use this skill to review WebCrypto usage and produce actionable security feedback. It is not a replacement for qualified cryptographic or application-security review when real security claims depend on the code.

## Review Priorities

1. Confirm the security goal and threat model.
2. Reject new primitives or protocols.
3. Check secure-context and runtime assumptions.
4. Check algorithms, IVs/nonces, authentication, and key usages.
5. Check key extractability, lifecycle, storage, and logging.
6. Check XSS, CSP, dependency trust, and script injection paths.
7. Check URLs, browser storage, analytics, telemetry, console logging, and error reporting.
8. Check tests, vectors, cross-runtime evidence, and review documentation.

## Workflows

- `workflows/webcrypto-security-review-workflow.md`
- `workflows/key-lifecycle-review-workflow.md`

## Resources

- `resources/security-review-checklist.md`
- `resources/threat-model-template.md`

## Examples

- `examples/anti-patterns.md`

## Scripts

- `scripts/webcrypto-command-guard.sh`
