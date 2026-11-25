---
name: ac-http
version: 1.0.0
description: Agent Coordinator HTTP API client
uses: []
requires:
  tools: [curl]
  services: [AgentCoordinator]
security:
  risk_level: write
  capabilities:
    - coordinator:read
    - coordinator:write
  requires_approval: false
---

# Agent Coordinator (HTTP)

Interact with the Agent Coordinator server via its HTTP API. This skill provides access to agent registration, task management, and system health monitoring through the coordinator's REST endpoints.

## Execution Model

This is an **HTTP skill** (`handler: type: http`). When `ac_request` is invoked, the executor makes an HTTP request to the Agent Coordinator server at the configured base URL. The tool schema in tool.yaml defines the external contract; the executor handles the HTTP communication directly.

**Prerequisite**: The Agent Coordinator server must be running at the configured URL.

## When to Use

- Registering an agent with the coordinator on session start
- Claiming a task to prevent other agents from working on the same thing
- Completing or releasing a task
- Sending heartbeats to indicate the agent is alive
- Checking system health, agent status, or task status
- Deregistering on session end

## Methodology

### 1. Health Check

Before any operation, verify the coordinator is running:
- Call `GET /health`
- If unreachable, wait and retry (up to configured retry attempts)
- If still unreachable, report the error — don't proceed without coordination

### 2. Agent Registration

On session start:
- **If running inside the agent wrapper** (you'll see `[wrapper]` in your system prompt):
  registration is handled automatically — **do NOT register again**.
- **If running standalone** (no wrapper): call `POST /agents/register` with agent ID,
  workspace, and capabilities. Capabilities are the **category prefixes** of your skills
  (the part before `/`). For example, skill `review/pr-review` → capability `review`.
- **Standalone only**: Store the registration confirmation and begin sending periodic heartbeats

### 3. Task Operations

| Operation | Endpoint | Method | When |
|-----------|----------|--------|------|
| Claim | `/tasks/claim` | POST | Before starting work on a task |
| Complete | `/tasks/{id}/complete` | POST | After task is done and verified |
| Release | `/tasks/{id}/release` | POST | When abandoning or handing off a task |
| List | `/tasks` | GET | Checking available or in-progress tasks |

### 4. Heartbeat

- **If running inside the agent wrapper** (`[wrapper]` in system prompt):
  heartbeats are handled automatically — do NOT send them yourself.
- **Standalone only**: send periodic heartbeats:
  - Call `POST /agents/{id}/heartbeat` with current status and task
  - Frequency: every 60 seconds while active
  - Include status (`working`, `idle`, `reviewing`) and current task ID

### 5. Deregistration

- **If running inside the agent wrapper** (`[wrapper]` in system prompt):
  session cleanup is handled automatically — do NOT deregister yourself.
- **Standalone only**: call `DELETE /agents/{id}` to deregister on session end

## Output Format

```
## Coordinator Request

- Endpoint: [path]
- Method: [GET/POST/PUT/DELETE]
- Status: [HTTP status code]
- Response: [response body summary]
```

## Quality Criteria

- Health check is performed before first operation
- Agent is registered on session start and deregistered on session end
- Tasks are claimed before work begins (prevents duplicate work)
- Tasks are completed or released when work finishes (doesn't leave tasks stuck)
- Heartbeats are sent regularly while active
- HTTP errors are handled gracefully with retries

## Common Mistakes

- **Not checking health first**: Making API calls to a coordinator that isn't running. Always check `/health` before proceeding.
- **Forgetting to claim tasks**: Starting work without claiming leads to multiple agents working on the same task.
- **Not releasing abandoned tasks**: If you can't finish a task, release it so another agent can pick it up. Don't leave it claimed.
- **Missing heartbeats**: Not sending heartbeats makes the coordinator think the agent is dead, potentially reassigning its tasks.
- **Not deregistering**: Leaving a stale agent registration means the coordinator tracks a ghost agent.
- **Hardcoding the URL**: Use the configured `base_url` from config defaults, not a hardcoded address. This enables deployment flexibility.

## Completion

A coordinator interaction is complete when:
- The HTTP request succeeded (2xx status code)
- The response is parsed and understood
- State changes are confirmed (registration, task claim, etc.)
- Errors are handled with appropriate retries
