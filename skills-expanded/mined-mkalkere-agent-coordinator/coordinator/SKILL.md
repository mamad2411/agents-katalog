---
name: coordinator
version: 1.0.0
description: Coordinate and monitor other agents — spawn, observe, fix issues
uses:
  - core/bus
  - core/memory
  - core/session
requires:
  tools: [curl]
  services: [AgentCoordinator]
security:
  risk_level: admin
  capabilities:
    - agent:spawn
    - agent:monitor
    - agent:terminate
    - bus:read
    - bus:write
    - memory:read
    - memory:write
  requires_approval: true
---

# Coordinator

Manage and monitor the agent ecosystem. The coordinator spawns agents, observes their work, fixes infrastructure issues, and ensures the multi-agent workflow operates smoothly. The coordinator orchestrates — it does not do the work itself.

## Execution Model

This is an **HTTP skill** (`handler: type: http`). When `coordinator_request` is invoked, the executor makes an HTTP request to the Agent Coordinator server. The tool schema in tool.yaml defines the external contract; the executor handles the HTTP communication directly.

**Role distinction**: This skill is for the coordinator agent — the one managing the ecosystem. Regular agents use `coordination/ac-http` for their own registration and task management.

## When to Use

- Setting up a multi-agent workflow (spawning developer + reviewer)
- Monitoring ongoing work across agents
- Debugging agent infrastructure issues
- Restarting or recovering stuck agents
- Improving the agent OS framework

## Methodology

### 1. Spawn Agents

When work needs to be done:
1. Determine which agent roles are needed (developer, reviewer, etc.)
2. Check if agents of those roles are already running
3. If not, spawn new agent sessions with appropriate identity and skills
4. Verify agents register with the coordinator
5. Assign initial tasks

### 2. Monitor Agents

While agents are working, check periodically:
- **Dashboard status**: Are all expected agents online?
- **Heartbeats**: Has any agent missed heartbeats (stale)?
- **Bus traffic**: Are messages flowing between agents?
- **Task progress**: Are claimed tasks making progress?

Check at the configured monitoring interval (default: every 5 minutes).

### 3. Detect and Fix Issues

When something is wrong:

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Agent offline | Crash or session timeout | Restore from checkpoint |
| No heartbeats | Agent hung or crashed | Check session, restart if needed |
| Messages not processed | Agent not polling bus | Verify `listens_to` in identity, send nudge |
| Task stuck (no progress) | Agent blocked or confused | Check memory/logs, send clarification |

### 4. Intervene When Necessary

Escalation levels:
1. **Nudge**: Send a message asking the agent to check its bus
2. **Restart**: Restore the agent from its last checkpoint
3. **Reassign**: Release the task and assign to a different agent
4. **Escalate**: Report the issue to the human supervisor

### 5. Orchestrate Workflows

The typical development workflow:
1. Receive task from user
2. Publish task to the `work` channel for developer agent
3. Monitor developer's progress
4. When PR is created, ensure reviewer picks it up
5. Monitor review cycle (review → address → re-review)
6. When approved, verify developer merges
7. Confirm task completion in coordinator

## Output Format

```
## Coordinator Status

### Agents
| Agent | Status | Current Task | Last Heartbeat |
|-------|--------|-------------|----------------|
| [name] | [active/idle/offline] | [task or none] | [timestamp] |

### Tasks
| Task | Assigned To | Status | Age |
|------|------------|--------|-----|
| [description] | [agent] | [claimed/in-progress/done] | [duration] |

### Issues
- [issue description] — [action taken]
```

## Quality Criteria

- All expected agents are running and registered
- Stale agents are detected within the threshold period
- Bus messages are flowing between agents correctly
- Tasks progress from claimed to completed
- Infrastructure issues are detected and fixed promptly
- Interventions follow the escalation levels (nudge before restart)
- The coordinator does not do the agents' work

## Common Mistakes

- **Doing the work yourself**: The coordinator orchestrates — it doesn't write code, review PRs, or merge. Delegate to the appropriate agent.
- **Intervening too early**: Agents need time to work. Don't nudge after 30 seconds of inactivity. Wait for the monitoring interval.
- **Not checking before spawning**: Spawning a duplicate agent when one is already running creates conflicts. Check existing agents first.
- **Ignoring stale agents**: An agent that hasn't sent a heartbeat is probably stuck. Investigate rather than ignoring.
- **Missing the feedback loop**: After a reviewer posts feedback, ensure the developer picks up the `review_completed` message. If the bus message is the wrong type, the developer never sees it.
- **Hardcoding infrastructure details**: Use the configured `base_url`, not a hardcoded URL. Keep infrastructure details in config defaults.

## Completion

Coordinator work is complete when:
- All required agents are spawned and registered
- Workflow is set up (tasks assigned, bus channels active)
- Monitoring is active (periodic checks configured)
- Issues are detected and resolved
- Tasks progress to completion
