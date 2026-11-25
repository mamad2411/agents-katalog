---
name: backend-logging
description: Implement effective server-side logging. Use when adding or
  improving application logs.
metadata:
  tags: backend, logging
---

# Backend Logging

## Use this skill when
- Structured JSON logging
- Correlating logs with requests via trace IDs
- Choosing log levels and retention
- Avoiding sensitive data in logs

## Do not use this skill when
- Metrics or tracing (use their own skills)
- Frontend logging

## Instructions
1. Log structured JSON, not free text.
2. Include requestId/traceId in every log line.
3. Use levels meaningfully: debug, info, warn, error.
4. Log at the boundary and at meaningful transitions, not every line.
5. Log errors with stack and context; log the handled outcome too.
6. Scrub PII, tokens, and secrets from log fields.
7. Define retention and routing (stdout → collector) from the start.

## Checklist
- No secrets/PII in logs
- Every log line has trace context

## Output Format
- Log schema | level policy | correlation strategy | event inventory

## Common Mistakes
- Logging request bodies wholesale (PII)
- Unstructured multiline logs
- Logging at info what belongs at debug
