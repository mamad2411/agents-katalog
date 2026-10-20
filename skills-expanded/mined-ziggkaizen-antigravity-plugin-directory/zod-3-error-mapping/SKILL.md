---
name: zod-3-error-mapping
description: Creates and reviews safe Zod 3 validation error mapping for APIs, forms, logs, and user-facing messages. Use when handling ZodError, safeParse failures, validation responses, form errors, redaction, or sensitive input leakage.
license: MIT
compatibility: Requires Node.js for bundled helper scripts. Intended for TypeScript or JavaScript projects using Zod 3.
---

# Zod 3 Error Mapping Skill

## When to Use

Use this skill when mapping `ZodError` issues to API responses, form errors, logs, telemetry, or support diagnostics.

## First Checks

1. Identify whether errors are user-facing, developer-facing, log-only, or metrics-only.
2. Identify sensitive fields and sensitive boundaries.
3. Run helper scripts with `--help` before using them:
   - `scripts/scan-sensitive-error-echo.mjs --help`
   - `scripts/zod-3-sensitive-error-check.mjs --help`

## Error Mapping Principles

- Use `.safeParse()` at recoverable boundaries.
- Return stable error objects with path, code, and safe message.
- Do not echo raw input values.
- Redact sensitive values in logs and diagnostics.
- Keep redaction behavior covered by tests.
- Prefer allow-listed error fields over block-listed payload redaction.

## Workflow References

- `workflows/error-mapping-workflow.md`: Use when creating public validation error mapping.
- `workflows/sensitive-error-review-workflow.md`: Use when reviewing code for sensitive input leakage.

## Resources and Examples

- `resources/error-mapping-checklist.md`: Safe error mapping checklist.
- `resources/sensitive-fields.md`: Common sensitive field patterns.
- `examples/safe-error-mapping.example.ts`: Safe mapper example.
- `examples/unsafe-error-echo.example.ts`: Anti-pattern examples.
