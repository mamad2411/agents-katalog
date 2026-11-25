---
name: p0-agent-harness
description: Use when implementing or reviewing TeaAgent P0 harness behavior, tool governance, budgets, audit logs, and destructive-tool approval.
---

# P0 Agent Harness

Use this skill when changing the first production-readiness layer of TeaAgent.

## Workflow

1. Keep the harness model-agnostic.
2. Register tools only through `ToolRegistry`.
3. Enforce schema validation before and after tool execution.
4. Enforce `RunBudget` limits on every run.
5. Require `ApprovalPolicy` for destructive tools.
6. Record lifecycle and tool events through `AuditLogger`.

## References

- Read `REFERENCE.md` for implementation details and extension rules.
