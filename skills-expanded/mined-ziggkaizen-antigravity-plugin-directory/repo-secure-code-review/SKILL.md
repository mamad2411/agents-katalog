---
name: repo-secure-code-review
description: Reviews code changes for security vulnerabilities, risky data flows, insecure defaults, missing authorization, unsafe input handling, sensitive data exposure, and missing security tests. Use for secure code review, security-sensitive diffs, and implementation review.
---

# Repo Secure Code Review

Use this skill to review code changes for security impact across languages and frameworks.

## When to Use This Skill

Use this skill when reviewing changes involving:

- authentication, authorization, sessions, tokens, roles, permissions, or identity
- user input, parsing, serialization, deserialization, file handling, redirects, or URL fetching
- database queries, shell commands, template rendering, dynamic code execution, or path handling
- secrets, credentials, private data, logs, telemetry, or test fixtures
- cryptography, hashing, signing, certificates, random values, or key material
- API boundaries, service-to-service calls, webhooks, callbacks, or external integrations
- CI/CD, deployment config, infrastructure config, or runtime security settings

## Review Approach

1. Identify trust boundaries and sensitive assets.
2. Review changed data flows from input to sink.
3. Look for missing authorization or incorrect ownership checks.
4. Look for unsafe string construction into interpreted contexts.
5. Look for secret or sensitive data exposure.
6. Check error handling and logging.
7. Check whether security tests cover negative cases.
8. Classify findings by severity and exploitability.
9. Provide actionable fixes, not vague warnings.

## Finding Quality

A good security finding includes:

- affected file and line or code path
- vulnerability class or risk
- why the current behavior is unsafe
- realistic exploit or failure scenario
- concrete remediation
- test recommendation
- severity

## Workflow

Use `workflows/repo-secure-code-review-workflow.md` for structured secure review.

## Resources

Use `resources/secure-review-checklist.md` during review.

## Examples

Use `examples/security-review-findings.md` as a finding format reference.

## Scripts

This skill owns:

```text
scripts/secure-diff-scan.py
```

Run the script with `--help` before manual use. The script is read-only and pattern-based; it does not replace human security review.
