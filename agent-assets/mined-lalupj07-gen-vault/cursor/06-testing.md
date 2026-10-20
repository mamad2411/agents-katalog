---
description: Testing rules focused on meaningful behavior and negative security cases
globs: "**/*.{ts,tsx,js,jsx,mjs,vue,svelte,dart,py,go,rs}"
alwaysApply: false
---

# Testing

## Use what the project has
- Detect the existing test setup (Vitest, Jest, Playwright, Cypress, `flutter_test`, pytest, `go test`, `cargo test`) and follow its conventions.
- If none exists, leave one small assert-based self-check for non-trivial logic. Ask before adding a test framework.

## Rules
- Test meaningful behavior, not coverage numbers. No snapshot dumps, no testing implementation details.
- Every bug fix gets a regression test that fails before the fix.
- Non-trivial logic leaves at least one runnable check behind.

## Choose the right level
- **Unit**: pure logic (pricing, validation, formatting, state reducers).
- **Integration / API**: handlers with real routing and validation, stubbed external providers.
- **Component / widget**: user-visible behavior and states (loading, empty, error).
- **End-to-end**: critical journeys only (signup, checkout, core task).

## Security-sensitive code needs negative tests
For auth, payments, admin and data-access code, verify:
- unauthorized access is rejected (no token, wrong role, another user's object)
- invalid input and malformed requests return a generic 4xx
- expired or revoked sessions and tokens are refused
- permission violations and privilege escalation attempts fail
- rate limits trigger after the threshold
- tampered signatures or client-supplied prices are rejected
- error handling returns safe messages with no internal details

## Before finishing
Run lint, type-check, build and relevant tests. Report what passed and what was not verified.
