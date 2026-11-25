---
name: google-adk-python
description: >
  Build production-ready AI agents in Python using Google Agent Development Kit (ADK).
  Use when creating agentic Python applications with LlmAgent, workflow agents
  (SequentialAgent, ParallelAgent, LoopAgent), multi-agent orchestration,
  tool development (function tools, MCP, OpenAPI), session and state management,
  callbacks and guardrails, testing and evaluation, Python backend integrations
  (FastAPI, Flask, Streamlit, Slack), streaming, A2A protocol,
  or deploying to Vertex AI, Cloud Run, or GKE.
  Triggers on "build an agent", "ADK", "ADK Python", "multi-agent system",
  "agentic application", "agent orchestration", "Gemini agent".
---

# Google Agent Development Kit (ADK) - Python

ADK is Google's open-source, code-first Python framework for building, evaluating, and deploying AI agents. Optimized for Gemini but model-agnostic. Requires Python 3.10+.

## Quick Start

```bash
pip install google-adk
```

**Project structure:**
```
my_agent/
├── __init__.py
├── agent.py
└── .env          # GOOGLE_API_KEY=xxx or GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

**.env configuration:**
```bash
# Option A: Google AI (simple)
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_api_key

# Option B: Vertex AI (enterprise)
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
```

**Minimal agent (agent.py):**
```python
from google.adk.agents import Agent

root_agent = Agent(
    name="assistant",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant.",
    tools=[]
)
```

**Run:** `adk web` (dev UI), `adk run my_agent` (CLI), or `adk api_server` (HTTP)

## Agent Types

| Type | Purpose | Use When |
|------|---------|----------|
| `LlmAgent` / `Agent` | LLM-powered reasoning | Flexible, language-centric tasks |
| `SequentialAgent` | Execute sub-agents in order | Multi-step pipelines |
| `ParallelAgent` | Execute sub-agents concurrently | Independent parallel tasks |
| `LoopAgent` | Repeat until condition | Iterative refinement |
| Custom (`BaseAgent`) | Specialized logic | Unique requirements |

See [references/agents.md](references/agents.md) for detailed patterns and code examples.

## Tools

Three categories:

1. **Function Tools** - Custom Python functions with docstrings as schema
2. **Built-in Tools** - Google Search, Code Execution, Vertex AI services
3. **External Tools** - MCP servers, OpenAPI specs, third-party integrations

```python
def get_weather(city: str) -> dict:
    """Get weather for a city.

    Args:
        city: City name (e.g., "New York", "London")

    Returns:
        Weather data with temperature and condition
    """
    return {"city": city, "temp": "72F", "condition": "sunny"}

agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    instruction="Help users check weather.",
    tools=[get_weather]
)
```

See [references/tools.md](references/tools.md) for MCP, OpenAPI, and advanced tool patterns.

## Multi-Agent Orchestration

**Six core patterns:**

1. **Coordinator/Dispatcher** - Central agent routes to specialists
2. **Sequential Pipeline** - Linear workflow with state passing
3. **Parallel Fan-Out** - Concurrent execution, then aggregate
4. **Hierarchical Decomposition** - Tree of delegating agents
5. **Generator-Critic** - Create then review
6. **Iterative Refinement** - Loop until quality threshold

See [references/multi-agent.md](references/multi-agent.md) for implementation details.

## Session & State

```python
# Write state in tools via ToolContext
def save_data(ctx: ToolContext, key: str, value: str) -> str:
    ctx.session.state[key] = value
    return f"Saved {key}"

# Read state in instructions via templating
instruction = "User prefers {user_preference} theme."

# State flows through sub-agents automatically
# Use output_key to capture agent output in state
agent = Agent(name="writer", output_key="draft", ...)
```

**SessionService** manages conversation threads. **MemoryService** enables cross-session knowledge. Use in-memory implementations for development, Firestore/database-backed services for production.

## Callbacks & Guardrails

Hook into execution at six checkpoints:

```python
def safety_check(callback_context, llm_request):
    if contains_pii(llm_request):
        return LlmResponse(content="Cannot process PII")
    return None  # Continue normally

agent = Agent(
    name="safe_agent",
    before_model_callback=safety_check,
    # Also: before_agent_callback, after_agent_callback,
    #       after_model_callback, before_tool_callback, after_tool_callback
)
```

Return `None` to proceed normally, return a response object to override and skip default behavior.

## Testing & Evaluation

ADK provides trajectory-based evaluation comparing actual agent behavior against expected tool call sequences and reference responses. A recommended best practice is to follow a **task-first approach**:

1. **Identify tasks/intents** - Map every user intent the agent handles, with tools involved
2. **Map trajectories** - For each task, define happy paths and failure trajectories (not found, not eligible, tool errors, ambiguous input)
3. **Select evals** - Use all 9 built-in metrics as baseline, then construct custom rubrics per task category
4. **Test in layers** - eval-file trajectory tests → integration eval sets (real LLM) → simulated scenario tests (multi-turn via `conversation_scenario`)

**Built-in metrics:** `tool_trajectory_avg_score`, `response_match_score`, `final_response_match_v2`, `rubric_based_final_response_quality_v1`, `rubric_based_tool_use_quality_v1`, `hallucinations_v1`, `safety_v1`

**Run:** `adk eval my_agent` or integrate with pytest.

See [references/testing.md](references/testing.md) for task-first strategy, rubric construction, eval trajectory tests, integration tests, and simulated scenario tests.

## Python Backend Integrations

### Streamlit

```python
import streamlit as st
from google.adk.runners import Runner

@st.cache_resource
def get_runner():
    return Runner(agent=root_agent, app_name="my_app")

runner = get_runner()
# Use runner.run() in chat interface
```

### FastAPI

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

app = FastAPI()
session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="api", session_service=session_service)

@app.post("/chat")
async def chat(request: ChatRequest):
    new_message = types.Content(
        role="user", parts=[types.Part(text=request.message)]
    )
    events = []
    async for event in runner.run_async(
        user_id=request.user_id,
        session_id=request.session_id,
        new_message=new_message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    events.append({"type": "content", "text": part.text})
    return {"events": events}
```

**Note:** `runner.run_async()` uses keyword-only arguments. The `new_message` must be a `types.Content` object from `google.genai.types`, not a plain string.

See [references/ui-integrations.md](references/ui-integrations.md) for Slack, PubSub, and frontend patterns.

## Streaming

**Server-Sent Events:**
```python
async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=new_message):
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text:
                yield part.text
```

**Bidi-streaming (Gemini Live):**
```python
from google.adk.agents import LiveRequestQueue

queue = LiveRequestQueue()
async for event in run_live(agent, queue):
    handle_event(event)
```

## A2A Protocol

Agent-to-agent communication for distributed Python systems:

```python
# Expose agent as A2A server
from google.adk.a2a import serve
serve(agent, port=8080)

# Consume remote agent as A2A client
from google.adk.a2a import A2AClient
remote = A2AClient("http://other-agent:8080")
```

## Deployment

| Platform | Best For |
|----------|----------|
| **Vertex AI Agent Engine** | Production, auto-scaling, managed |
| **Cloud Run** | Containerized, serverless |
| **GKE** | Custom configs, open-source models |
| **Docker/Podman** | Offline, air-gapped environments |

See [references/deployment.md](references/deployment.md) for Dockerfiles, K8s manifests, and production checklists.

## Best Practices

1. **Start simple** - Single agent first, add complexity as needed
2. **Use descriptive names** - Agent/tool `description` fields guide LLM routing
3. **State over message passing** - Use `session.state` and `output_key` for data flow
4. **Write clear docstrings** - LLM uses function docstrings and type hints as tool schema
5. **Test trajectories** - Verify tool call sequences, not just outputs
6. **Callbacks for guardrails** - Not for business logic
7. **Dev UI for debugging** - `adk web` shows events, state changes, latency

## Common Pitfalls

- **Circular agent references** - An agent instance can only be sub-agent once
- **Missing tool descriptions** - LLM needs docstrings to select tools
- **In-memory services in prod** - Data lost on restart; use Firestore/Redis
- **Blocking in async** - Use `run_async` for streaming endpoints
- **Over-orchestration** - A single agent is often sufficient
- **Missing type hints** - Tools without type hints produce poor schemas

## Resources

- [references/agents.md](references/agents.md) - Agent types and patterns
- [references/tools.md](references/tools.md) - Tool development guide
- [references/multi-agent.md](references/multi-agent.md) - Orchestration patterns
- [references/testing.md](references/testing.md) - Evaluation framework
- [references/ui-integrations.md](references/ui-integrations.md) - Backend and frontend integration
- [references/deployment.md](references/deployment.md) - Production deployment

## External Links

- [Official Docs](https://google.github.io/adk-docs/)
- [GitHub (google/adk-python)](https://github.com/google/adk-python)
- [ADK Training Hub](https://github.com/raphaelmansuy/adk_training)
