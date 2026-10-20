---
name: repo-console-network-debugging
description: Reviews browser console and network evidence. Use when debugging JavaScript errors, failed requests, redirects, CORS-like symptoms, asset loading, storage behavior, or browser-only runtime failures.
---


# Console and Network Debugging

Use this skill when browser console or network evidence is central to the task.

## Focus Areas

- JavaScript runtime exceptions
- source-mapped stack traces
- failed fetch/XHR/document/script/style/image requests
- CORS-like failures
- redirects and mixed-content errors
- cache and service-worker confusion
- auth/session failures
- content security policy violations
- asset loading and bundling problems

## Required Behavior

- Redact tokens, cookies, authorization headers, query secrets, emails, and customer identifiers.
- Distinguish network transport errors from application errors.
- Record method, endpoint pattern, status code, and timing when useful.
- Do not paste full response bodies if they contain private data.
- Tie observations to specific reproduction steps.

## Workflow

Use `workflows/console-network-debugging-workflow.md`.

