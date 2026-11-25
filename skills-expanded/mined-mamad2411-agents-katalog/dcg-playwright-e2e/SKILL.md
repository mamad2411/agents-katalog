---
name: dcg-playwright-e2e
description: Run safe, repeatable browser checks for DCG Smart PWA test environments using Playwright. Use when verifying login, OTP, session boundaries, navigation, loading, error states, responsive UI, accessibility, or a pre-release test flow.
---

# DCG Playwright end-to-end testing

Automate only an explicitly identified TEST or staging URL unless a human has approved production smoke testing.

1. Read the work item, `AGENTS.md`, environment ownership, and `docs/quality/playwright-standard.md`. Confirm the URL, environment marker, test account, test data, and rollback boundary.
2. Use a fresh browser context. Never record, display, commit, or hard-code real credentials, OTPs, service keys, tokens, or personal data.
3. Begin with a browser snapshot. Use role, label, Thai visible text, or test-id locators; do not use brittle CSS paths. Re-snapshot after navigation or a major state change.
4. Cover the smallest relevant flow: public landing or direct login, authentication boundary, expected success state, one denied/error path, sign-out, and session-expiry behavior where the change can affect it.
5. Check viewport widths appropriate to the screen, keyboard navigation for changed controls, Thai copy, TEST banner, loading, empty/error states, and no console/network errors caused by the change.
6. Save only non-sensitive screenshots and traces under the project's approved test-artifact path. On a failure, record the exact step, visible result, trace/screenshot location, and safe reproduction steps.
7. Treat a passing browser run as evidence, not authorization to deploy. Record results in the work item and `agent-memory/WORKLOG.md`; require human approval before production actions.

Use the existing Playwright CLI/wrapper before adding a new browser framework or dependency. Do not use the test account against production.
