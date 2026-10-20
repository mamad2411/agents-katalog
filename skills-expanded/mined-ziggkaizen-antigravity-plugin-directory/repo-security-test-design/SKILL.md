---
name: repo-security-test-design
description: Designs security-focused tests for authorization, validation, injection resistance, tenant isolation, replay safety, sensitive data exposure, and error handling. Use when implementing or reviewing security-sensitive changes.
---

# Repo Security Test Design

Use this skill to create test plans for security-sensitive work.

## When to Use This Skill

Use this skill when changes affect:

- authentication or authorization
- input validation or parsing
- query, command, path, template, or expression construction
- multi-tenant access or object ownership
- secrets, logs, telemetry, or private data
- webhooks, callbacks, tokens, signatures, replay windows, or idempotency
- uploads, downloads, redirects, or external URL fetches

## Test Design Principles

- Include negative tests, not only happy paths.
- Test unauthorized, malformed, boundary, encoded, oversized, replayed, and cross-tenant cases.
- Verify sensitive data is not exposed in responses, logs, errors, or fixtures.
- Prefer tests that fail before the fix and pass after the fix.
- Keep tests deterministic and isolated.
- Avoid real secrets and production data.

## Workflow

Use `workflows/repo-security-test-plan-workflow.md` for structured test planning.

## Resources

Use `resources/security-test-case-catalog.md` for test ideas.
