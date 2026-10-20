---
name: backend-validation
description: Validate backend input thoroughly. Use when implementing input
  validation on servers.
metadata:
  tags: backend, validation
---

# Backend Validation

## Use this skill when
- Validating request payloads and query params
- Defining validation schemas server-side
- Returning structured validation errors

## Do not use this skill when
- Client-side validation only
- Validating internal trusted data

## Instructions
1. Validate all external input: body, query, path, headers, files.
2. Use a schema library (Zod, Joi, class-validator, Pydantic).
3. Sanitize and coerce types at the boundary.
4. Return structured field-level errors (field, message, code).
5. Distinguish validation errors (4xx) from logic errors (5xx).
6. Set explicit limits: length, ranges, allowed values.
7. Validate at the API boundary, not only in services.

## Checklist
- Every endpoint validates input
- Errors are structured, not free text

## Output Format
- Endpoint | schema | limits | error codes

## Common Mistakes
- Trusting client-side validation
- Only validating happy-path fields
- 500 on malformed input instead of 400
