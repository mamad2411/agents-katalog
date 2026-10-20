---
name: repo-logging-and-privacy-review
description: Reviews logs and telemetry for usefulness, privacy, redaction, structured context, correlation IDs, and sensitive-data safety. Use when adding, changing, or reviewing logging, telemetry, error handling, audit events, request tracing, or debug output.
---

# Repository Logging and Privacy Review

Use this skill when adding or reviewing logs, telemetry, debug output, or error reporting.

## When to Use This Skill

Use this skill for:

- new log statements
- error logging changes
- request/response logging
- audit events
- telemetry payloads
- tracing spans and attributes
- crash or exception reporting
- debug flags and verbose output

## Review Process

1. Identify what operational question each log answers.
2. Check severity, event name, structure, and correlation fields.
3. Check whether data is sensitive using `resources/logging-redaction-checklist.md`.
4. Prefer sanitized identifiers over raw values.
5. Avoid full body, header, cookie, token, and credential logging.
6. Ensure logs are useful without leaking private data.
7. Confirm that debug logs cannot be accidentally enabled in production without controls.

## Workflow

Use `workflows/logging-and-privacy-review-workflow.md` for structured review.

## Scripts

This skill owns:

```text
scripts/logging-risk-scan.py
```

Run the script with `--help` before manual use.
