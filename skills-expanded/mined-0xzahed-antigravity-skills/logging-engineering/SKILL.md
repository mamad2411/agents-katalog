---
name: logging-engineering
description: Design structured logging for systems. Use when building or
  reviewing application log pipelines.
metadata:
  tags: logging, engineering
---

# Logging Engineering

## Use this skill when
- Designing log structure and levels
- Correlating distributed logs
- Routing logs to a pipeline with retention
- Avoiding secrets/PII in logs

## Do not use this skill when
- Metrics or traces (use their own skills)
- Frontend logging

## Instructions
1. Log structured JSON with fixed fields.
2. Include traceId/requestId context on every entry.
3. Use levels deliberately and consistently across services.
4. Log business events for auditability (who/what/when).
5. Ship via collector to a central store with retention policy.
6. Scrub sensitive fields at the source, not only at query time.
7. Index what you query; avoid querying on exploded fields.

## Checklist
- PII/secrets scrubbed at source
- Correlation IDs everywhere
- Retention documented

## Output Format
- Log schema | levels | correlation | pipeline | retention

## Common Mistakes
- Free-text logs nobody can query
- Secrets leaking via request logs
- No retention / infinite growth
