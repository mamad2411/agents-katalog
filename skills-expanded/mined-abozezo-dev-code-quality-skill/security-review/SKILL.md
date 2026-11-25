---
name: security-review
description: |
  Reviews application changes for input validation, authentication and authorization, injection, secret exposure,
  browser storage, uploads, redirects, and unsafe defaults. Use for security-sensitive code or a focused security pass.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Security Review

Use this skill to identify and remediate exploitable behavior, unauthorized access, and sensitive-data exposure.

## Workflow

1. Define the changed trust boundaries: inputs, identities, protected resources, storage, external services, and client/server transitions.
2. Review validation, authentication, authorization and ownership enforcement, injection defenses, secret handling, browser storage, files, redirects, and configuration defaults.
3. Classify each finding by severity, explain its impact, fix it where possible, and re-verify the affected path.
4. Report both confirmed findings and checks performed with no issue found; do not claim a full audit beyond the reviewed scope.

## Rules

- Treat every external value as untrusted until validated server-side.
- Authentication does not imply authorization; enforce permissions for every protected action.
- Never expose secrets or privileged tokens in client bundles, logs, or responses.
- Prefer explicit secure defaults for cookies, sessions, headers, CORS, file access, redirects, and caching.

## Reference

Read [the security verification guide](reference/security-verification.md) for the required review checklist, red flags, and severity guidance.
