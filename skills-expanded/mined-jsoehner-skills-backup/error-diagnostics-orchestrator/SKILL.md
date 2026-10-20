---
name: "error-diagnostics-orchestrator"
description: "Orchestrates comprehensive error diagnostics, including analysis, tracing, multi-agent review, and handling patterns."
version: 1
created: "2026-07-31"
updated: "2026-07-31"
---
## When to Use
Use for any task involving error diagnosis, debugging, tracing, or implementing robust error-handling patterns.

## Procedure
1. Identify the error type: Analysis, Tracing, Multi-Agent Review, or Pattern Implementation.
2. For Error Analysis: Use `error-debugging-error-analysis` and `error-diagnostics-error-analysis` to identify the root cause.
3. For Error Tracing: Use `error-debugging-error-trace` and `error-diagnostics-error-trace` to follow the request flow.
4. For Multi-Agent Review: Use `error-debugging-multi-agent-review` for complex issues requiring multiple perspectives.
5. For Handling Patterns: Use `error-handling-patterns` to implement resilient error management.
6. Synthesize the findings into a clear incident report or fix plan.

## Pitfalls
- Do not rely solely on logs; always correlate with traces and metrics where available.
- Ensure the root cause is identified before proposing a fix.
- Use multi-agent review for complex, distributed system failures.

## Verification
1. Root cause is clearly identified and documented.
2. Trace information is correlated with the error.
3. Fix plan is comprehensive and addresses the underlying issue.


