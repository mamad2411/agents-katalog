---
name: "managed-agents"
description: "Deploy and manage Claude agents with lifecycle management, monitoring, and scaling"
---

# Managed Agents

## When to activate
Building applications where agents need to run autonomously in the cloud, or when the user mentions Claude Managed Agents, long-running agent tasks, or building agent-powered products via the Anthropic API.

## When NOT to use
- Claude Code subagents running in a terminal session — those use the `Task` tool, not this API
- Short synchronous requests that complete in under 10 seconds — use the standard Messages API
- Workflows requiring Zero Data Retention (ZDR) or HIPAA BAA — Managed Agents are not eligible

## Instructions

### Core Concepts
- **Agent:** a configured entity with a model, system prompt, and allowed tool set
- **Environment:** a compute sandbox where the agent runs (cloud-hosted by Anthropic, or self-hosted)
- **Session:** one execution run — has a start, an end, and an event stream
- **Events:** Server-Sent Events (SSE) stream reporting what the agent is doing in real time

**Key distinction from Claude Code subagents:** Managed Agents run independently of your terminal in Anthropic's cloud. Use them for async, long-running, or API-driven agent products — not for Claude Code slash commands.

### Beta Header
All Managed Agents API calls require:
```
anthropic-beta: managed-agents-2026-04-01
```

### Tool Type
To give an agent access to all built-in tools (Bash, file operations, web search, web fetch, MCP):
```python
tools=[{"type": "agent_toolset_20260401"}]
```

### Python Pattern
```python
import anthropic

client = anthropic.Anthropic()

# 1. Create the agent (do once; reuse agent_id)
agent = client.beta.agents.create(
    model="claude-opus-4-5",
    name="research-agent",
    system="You are a research agent. When given a topic, search the web, gather facts, and produce a structured summary.",
    tools=[{"type": "agent_toolset_20260401"}],
)

# 2. Create an environment (cloud sandbox)
env = client.beta.environments.create(type="cloud")

# 3. Create a session and stream events
with client.beta.sessions.stream(
    agent_id=agent.id,
    environment_id=env.id,
    input="Research the latest developments in quantum computing and summarize in 3 bullet points.",
) as stream:
    for event in stream:
        if event.type == "agent.message":
            print(event.data.text, end="", flush=True)
        elif event.type == "agent.tool_use":
            print(f"\n[Tool: {event.data.name}]")
        elif event.type == "session.status_idle":
            print("\n[Session complete]")
            break
```

### Event Types
| Event | Meaning |
|---|---|
| `agent.message` | Agent producing output text |
| `agent.tool_use` | Agent calling a tool — `data.name` is the tool name |
| `agent.tool_result` | Result returned from a tool call |
| `session.status_idle` | Agent has finished and is waiting |
| `session.status_error` | Session ended with an error |

### Async Session (Fire and Poll)
For workloads where you don't want to hold a connection open:
```python
# Start session without streaming
session = client.beta.sessions.create(
    agent_id=agent.id,
    environment_id=env.id,
    input="Analyze these 50 documents and extract action items.",
)
session_id = session.id

# Poll status later
import time
while True:
    session = client.beta.sessions.retrieve(session_id)
    if session.status in ("idle", "error"):
        break
    time.sleep(10)

# Retrieve output
output = client.beta.sessions.retrieve(session_id)
print(output.output)
```

### Rate Limits
| Operation | Limit |
|---|---|
| Create session | 300 RPM |
| Read session / stream | 600 RPM |

### Testing with the `ant` CLI
```bash
# Install
npm install -g @anthropic-ai/ant

# Test an agent interactively
ant run --agent-id <id> --environment cloud

# Run with a specific input
ant run --agent-id <id> --input "Summarize today's AI news"
```

### Agent Lifecycle Management
- Agents are persistent configurations — create once, reuse across many sessions
- Environments are per-run compute sandboxes — create a new one per session for isolation
- Sessions are ephemeral — store the output before the session expires
- Store `agent_id` in your application config; store session output in your database

### When to Use Cloud vs Self-Hosted Environment
- **Cloud (`type: "cloud"`):** fastest to start, no infrastructure, appropriate for most use cases
- **Self-hosted:** when the agent needs access to internal network resources, private data stores, or custom tool servers not reachable from Anthropic's cloud

## Example

A product that lets users submit research tasks asynchronously via a web form:

1. User submits: "Find the top 5 competitors to our product and summarize their pricing"
2. App creates a session with `type: "cloud"` environment — stores `session_id` in the job queue
3. App returns immediately: "Your research report will be ready in ~10 minutes"
4. Background worker polls session status every 30 seconds
5. When `session.status == "idle"`, worker retrieves `session.output` and emails the user
6. User receives a structured 5-competitor analysis with pricing tables

The entire agent run — web searches, data extraction, synthesis — happens in Anthropic's cloud with no infrastructure management.

---
