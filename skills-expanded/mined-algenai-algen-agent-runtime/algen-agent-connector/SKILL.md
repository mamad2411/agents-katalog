---
name: algen-agent-connector
description: Connect an Algen Runtime agent or workflow to typed tools, MCP, HTTP APIs, databases, retrieval stores, model providers, memory, persistence, or telemetry without bypassing governance.
---

# Connect an Algen agent

Identify the requested systems, data direction, side effects, credentials, network boundary,
tenancy, and expected failure behavior. Read the matching parts of `references/connectors.md` and
combine connectors only when the use case needs them.

Expose external actions as typed Runtime tools or workflow resources. Do not call a connector
directly from orchestration code to bypass policy, approvals, idempotency, audit events, budgets, or
telemetry. Use secret references in configuration and resolve values only at execution time.
When a tool acts as the signed-in user, forward the caller's credentials from
`ToolContext.credentials`; the host supplies them on every run and resume, and they are never
persisted. Remote MCP servers that need per-user sign-in use the Runtime's MCP OAuth, not a token
in an environment variable.

For each connection, declare least-privilege permissions, read/write behavior, idempotency, strict
schemas (mark id fields `"format": "identifier"` so the `pii` guardrail does not mask them), timeout, retry policy, concurrency, result-size limit, and allowed destinations. Mark it on
the consuming workflow node with a `WorkflowResourceReference` so Studio can display the actual
topology.

Test with a deterministic fake or local fixture. Live credentials and paid services belong only in
explicit live tests. Document the required Runtime extra and environment variable names without
including secret values.

