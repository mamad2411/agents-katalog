---
name: datadog-analyze-log-pipeline
description: Analyze Datadog log pipelines, processors, parsing, remappers, facets, sensitive-data handling, exclusion behavior, and structured logging quality. Use for missing fields, broken parsing, inconsistent service tags, PII concerns, or log-processing problems.
---

# Analyze Log Pipeline

1. Identify relevant log source, pipeline, service, and environment.
2. Inspect parsing and processor behavior for representative events.
3. Verify critical fields such as service, env, version, status, trace ID, request ID, and error attributes.
4. Check masking/redaction requirements for sensitive fields.
5. Identify parsing failures, field collisions, routing mistakes, and unintended exclusion.
6. Never reproduce sensitive values in output.

## Output
- Pipeline Scope
- Parsing/Field Findings
- Correlation Impact
- Sensitive-Data Findings
- Recommended Changes
