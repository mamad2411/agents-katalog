---
name: test-mcp
description: Guide end-to-end testing of platform changes via the local MCP server (aflow-local). Covers prerequisites, testing patterns per change type, result interpretation, and feedback collection.
argument-hint: [what-to-test]
---

# /test-mcp — Test via Local MCP Server

Test your changes end-to-end through the local Aflow MCP server, seeing exactly what agents and users see.

## Prerequisites

Before testing, verify the local stack is running:

1. **Stack**: `yarn start` (Postgres, Redis, server, orchestrator, executors, web)
2. **Or engine only**: `yarn dev:core` (server + orchestrator + mock executor)
3. **MCP server**: served by `yarn start` on port 3100 (`yarn dev:mcp` beside `yarn dev:core`)
4. **Auth**: `mcp.local.json` in the project root holds its API key and the session token a client presents for it — `yarn mcp:setup` writes both and prints the line that sets `AFLOW_MCP_LOCAL_TOKEN`, which `.mcp.json` sends; a session without it is refused with a `401`. `auth_status` reports `api_key`

Quick health check:

```bash
curl -s http://localhost:3000/v1/health | head -1   # API server
curl -s http://localhost:3100/health | head -1       # MCP server
```

## Testing patterns by change type

### After operation schema changes

1. **Verify catalog listing**: `mcp__aflow-local__catalog` — check the operation appears with correct params
2. **Run the operation**: `mcp__aflow-local__run_operation` with `operationId` and test input
3. **Inspect the run**: `mcp__aflow-local__inspect_run` with the returned `runId` — check step traces and output
4. **Check for validation errors**: If input is rejected, the error should be clear and actionable

### After flow definition changes

1. **Run the flow**: `mcp__aflow-local__run_flow` with `flowId` or inline flow config
2. **Inspect traces**: `mcp__aflow-local__inspect_run` — verify all steps executed in expected order
3. **Check state variables**: Inspect run output for correct state variable values

### After agent behavior changes

1. **Run an agent flow**: `mcp__aflow-local__run_flow` with an agent flow (e.g., seed flows)
2. **Observe decision cycle**: Check `inspect_run` for agent turn decisions, tool calls, and results
3. **Test edge cases**: Request input, parallel tool calls, completion with `finalOutputSchema`

### After executor changes

1. **Run relevant operation**: `mcp__aflow-local__run_operation` targeting the modified executor
2. **Check error handling**: Intentionally provide invalid input — verify error messages are clear
3. **Check output format**: Verify output matches `outputZod` schema

### After MCP server changes

1. **Important**: After changes to `apps/aflow-mcp/`, the MCP server auto-restarts via `scripts/watch-service.mjs`
2. **Session reset required**: The user must close and resume the Claude Code session for the coding agent to pick up updated tool schemas
3. **Re-test**: Run `mcp__aflow-local__auth_status` to confirm reconnection, then test your changes

## Interpreting inspect_run output

The `inspect_run` tool returns a structured debug summary:

- **Step traces**: Each step's status, duration, input/output refs, error details
- **Token usage**: Per-step and total token consumption
- **Decision chain**: For agent flows, the sequence of agent decisions and tool calls
- **Error details**: Stack traces, error codes, classification (user/internal/transient)

**What to look for:**

- Steps in `FAILED` status — read the error message and code
- Unexpected step ordering — check transitions in the flow definition
- Missing output — check if the operation produced output or if payload resolution failed
- High token usage — may indicate context engineering issues

## When MCP tools aren't enough

| Need                     | Tool                                                    |
| ------------------------ | ------------------------------------------------------- |
| Raw API response/headers | `curl http://localhost:3000/v1/...`                     |
| SSE event stream         | `curl -N http://localhost:3000/v1/runs/:runId/events`   |
| Full debug view          | `curl http://localhost:3000/v1/runs/:runId/debug`       |
| Redis hot state          | `redis-cli` commands (see CLAUDE.md Redis key patterns) |
| Postgres data            | `psql` on port 5433                                     |
| Live service logs        | Check terminal running `yarn start`                     |

## Feedback collection

When you encounter MCP issues during testing, note:

- **Confusing output**: What was unclear? What would be more helpful?
- **Missing information**: What data did you need that wasn't in the response?
- **Unhelpful errors**: Did the error message help diagnose the problem?
- **Workflow friction**: Did a common task require too many tool calls?

Save observations to `memory/feedback_mcp-<topic>.md` for cross-session accumulation.
