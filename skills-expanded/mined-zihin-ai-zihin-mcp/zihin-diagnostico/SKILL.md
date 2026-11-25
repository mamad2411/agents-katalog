---
name: zihin-diagnostico
description: Use this guide to investigate incorrect agent responses, missing tools, failed runs, high cost or latency, and conversations that no longer start new turns.
---

# Diagnose agent behavior

Start with the observed symptom and a specific agent, session or execution identifier.
Use `get_agent_metrics` for the relevant period. Check whether tool statistics represent
a truncated sample before interpreting them as totals.

For missing tools, inspect `list_agent_tools`, validate agent schemas and test external
MCP servers. Refresh the MCP cache after fixing connectivity or configuration. Compare
the loaded tool names in `get_execution_diagnostics` with the tools the agent attempted
to use. A tool cited by a persona or skill may have been removed or blocked by a policy.

Inspect a specific execution with `get_execution_diagnostics`. For multi-agent work,
use `get_execution_trace`; for a conversation spanning multiple turns, also inspect
`get_session_agent_tree`. Check child results before accepting a supervisor's summary.

For timeouts, inspect `timeout_clock` and the configured execution and tool budgets.
Do not assume a timeout switched models or that no work occurred. Investigate provider
or account-wide errors with `get_tenant_health` before changing the agent configuration.

For agents that do not start, check budgets, plan quota, session controls and the consumer
profile. A budget limit, suspended session or consumer restriction can prevent execution.
Use history and version comparison to identify regressions; use supported rollback tools
when appropriate. Reproduction with `chat_with_agent` or `test_trigger` performs real work.
