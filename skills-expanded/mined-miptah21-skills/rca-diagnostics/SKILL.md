---
name: rca-diagnostics
description: |
  Cross-system incident response and post-mortem Root Cause Analysis for data platforms.
  Use when: investigating MULTI-system failures, correlating failures across infra + data + code, writing post-mortem reports, or diagnosing cascading failures.
  Do NOT use for single Airflow DAG failures — use `debugging-dags` instead.
  Do NOT use for single dbt model errors — use `debugging-dbt-errors` instead.
metadata:
  author: dataops-agent
  version: "2.0.0"
---

# Root Cause Analysis (RCA) Diagnostics

Cross-system incident response. For single Airflow DAG failures, use `debugging-dags`. For single dbt errors, use `debugging-dbt-errors`.

## When to Apply
Use this skill when:
- Multiple pipelines or systems failed simultaneously (cascading failure)
- Correlating failures with infrastructure changes (deploys, config changes)
- Correlating failures with upstream data source changes
- Writing post-mortem / incident reports
- Investigating systemic reliability issues (recurring failures, intermittent errors)
- Analyzing patterns across multiple incident occurrences

## Scope Boundaries

| Task | Correct Skill |
|------|--------------|
| "My DAG failed, fix it" | `debugging-dags` |
| "dbt build failed with error" | `debugging-dbt-errors` |
| "3 pipelines broke after deploy" | **this skill** ✅ |
| "Write a post-mortem for the outage" | **this skill** ✅ |
| "Why do these errors keep recurring?" | **this skill** ✅ |

## Best Practices
1. **Methodical Tracing**: Work backward from the point of failure to the source.
2. **Holistic View**: Look beyond the code (check infrastructure, upstream API changes, network timeouts).
3. **Blameless Culture**: Focus on systemic failures and how to prevent them in the future.
4. **Actionable Fixes**: Always provide a short-term mitigation and a long-term architectural fix.

## Execution Pattern
1. Gather all available logs, error messages, and context from all affected systems.
2. Build a timeline of events leading to the incident.
3. Perform backward tracing to isolate the root cause.
4. Provide a clear explanation of *why* it failed.
5. Propose immediate remediation and long-term preventative measures.
6. Draft a post-mortem document if requested.
