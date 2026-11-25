---
name: google-adk
description: This skill builds reliable AI agents with the official Google ADK for Python (`pip install google-adk`), from hello world to professional production systems. Use whenever the user is writing agent code with the `google.adk` package — Agent/LlmAgent, Runner/InMemoryRunner, InMemorySessionService, @function tools & ToolContext, sub_agents, SequentialAgent/Workflow graphs, modes (single_turn/task/chat), output_schema structured output, output_key & session state, callbacks, google_search, McpToolset/MCP tools, Gemini model config (gemini-flash-latest, GOOGLE_API_KEY, GOOGLE_GENAI_USE_ENTERPRISE), adk run/web/api_server CLI, streaming, or multi-agent orchestration. Also use for questions about how the SDK works, its current API surface, or converting an idea into a Gemini agentic app. Provides the correct, docs-grounded API (no guessed imports).
---

# Google ADK (Python)

## Overview

The Google Agent Development Kit (ADK) is a code-first, Python-first toolkit for building agents with Gemini and other models. Core concepts: **Agents** (`LlmAgent`, aliased `Agent`) with instructions and tools, **sub-agents / workflows** (hierarchical delegation and deterministic orchestration), **sessions & state** (per-conversation memory), **events** (the execution stream), and **callbacks** (interception hooks). `Runner` executes agents; `InMemorySessionService` stores sessions.

Ground all code in the official docs. This skill's reference files reproduce the documented API — never invent imports or parameters. Current ADK is v2.x (latest v2.6.2, 2026-08).

## Core workflow (hello world)

```python
from google.adk.agents.llm_agent import Agent

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = Agent(
    model='gemini-flash-latest',
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)
```

Setup: `pip install google-adk` (Python 3.10+), then put `GOOGLE_API_KEY` in `.env`. Run with `adk run my_agent`, `adk web` (dev UI), or programmatically with `Runner` + `InMemorySessionService`.

## How to use this skill

1. Identify what the user is building (single agent → tools → multi-agent → production).
2. Read the matching reference file(s) below **before writing agent code**.
3. Use the example scripts in `assets/examples/` as starting points; adapt them to the user's needs.
4. For anything beyond these guides, consult the official docs (`https://adk.dev/`); model IDs change and docs examples lag — prefer configurable model selection.

## Before implementing

Gather context before writing agent code:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing Python project layout, framework (FastAPI/CLI), dependency manager, where the agent will be invoked |
| **Conversation** | The agent's purpose, who calls it, single-turn vs multi-turn, required model/provider, streaming needs |
| **Skill references** | The reference file for the feature being built (see decision guide below) |
| **User guidelines** | Available API keys/secrets (`GOOGLE_API_KEY` vs Vertex env vars), deployment environment, existing DB for sessions |

## Clarify when ambiguous

Ask only what the code cannot tell you — never ask the user to recall SDK API details (this skill embeds them). Limit to 1–2 questions up front.

- **Required** (ask before building if unknown)
  - What does the agent do end-to-end, and who/what invokes it (CLI, web endpoint, background job)?
  - Is the interaction multi-turn (needs sessions/state) or single-turn?
- **Optional** (only if relevant)
  - Google AI Studio (`GOOGLE_API_KEY`) vs Vertex (`GOOGLE_GENAI_USE_ENTERPRISE=TRUE` + project/location)?
  - Is a persistence backend available (Postgres/Firestore) for sessions, or is in-memory fine?

## Learning path: hello world → production

| Stage | What the user learns to build | Read first |
|---|---|---|
| 1. Hello world | Install, project structure, first agent, Runner, run commands | `references/getting-started.md` |
| 2. Agents & config | LlmAgent params, instructions, `output_schema`, generation config, modes | `references/agents.md` |
| 3. Tools | Function tools, ToolContext, google_search, AgentTool, code execution | `references/tools.md` |
| 4. Multi-agent | sub_agents, single_turn/task/chat modes, SequentialAgent, Workflow graphs | `references/orchestration.md` |
| 5. State | Sessions, state scopes, `output_key`, state_delta, memory | `references/sessions-and-state.md` |
| 6. Events & callbacks | Event stream, `is_final_response`, interception hooks | `references/events.md`, `references/callbacks.md` |
| 7. Models | Gemini config, auth, retries, Interactions API | `references/models-and-config.md` |
| 8. Integrations | MCP servers as tools | `references/mcp.md` |
| 9. Production | Observability, evals, deployment, CLI reference | `references/observability-and-production.md` |

## Decision guide (jump straight to the right file)

- **Install / hello world / project structure / `adk run` vs `adk web` / Runner** → `getting-started.md`
- **Agent configuration** (name, model, instruction, output_schema, generate_content_config, modes) → `agents.md`
- **Tools** (function tools, docstring schemas, ToolContext, google_search, AgentTool, code execution) → `tools.md`
- **Multi-agent orchestration** (sub_agents vs AgentTool vs workflows, mode semantics) → `orchestration.md`
- **Conversation memory / state / session backends** → `sessions-and-state.md`
- **Understanding the event stream / final responses / streaming** → `events.md`
- **Intercept or modify agent/LLM/tool behavior** → `callbacks.md`
- **Which Gemini model / auth / retries / generation config** → `models-and-config.md`
- **Connect an MCP server** (stdio, streamable HTTP, SSE) → `mcp.md`
- **Tracing, evals, deployment, production hardening** → `observability-and-production.md`

## Key rules (verified against official docs)

- **`name` is required** on every agent; `model` and `instruction` are strongly recommended. `description` is recommended for multi-agent routing.
- **`agent.py` must define a variable named `root_agent`** — ADK's tools discover the agent through it.
- **Plain Python functions in `tools=` are auto-wrapped** as function tools; the docstring + type hints generate the LLM-facing schema.
- **A parameter is required** if it has a type hint and no default; optional if it has a default or `Optional[...]`. `*args`/`**kwargs` are ignored.
- **Return dicts from tools** (prefer a `"status"` key); other types get wrapped as `{"result": ...}`.
- **`ToolContext` injection**: add a parameter typed `ToolContext` — it's auto-injected and hidden from the LLM; parameter name is flexible.
- **Python callback parameter names must match exactly** (`callback_context`, `llm_request`, `llm_response`, `tool`, `args`, `tool_context`, `tool_response`) or you get a `TypeError`.
- **`mode="task"` agents must call the built-in `finish_task` tool** to complete; `single_turn` and `task` sub-agents are exposed to parents as **tools**, not transfer targets.
- **`InMemorySessionService` loses all data on restart** — use Database/Vertex/Firestore services for production.
- **Never mutate `session.state` directly** on a retrieved session; update via `output_key`, `EventActions.state_delta`, or `context.state`.
- **State prefixes**: none = session, `user:` = per-user, `app:` = global, `temp:` = current invocation only (never persisted).
- **`google_search` tool is Gemini-2-only and must be the sole tool** in the standard path (Interactions API uses `bypass_multi_tools_limit=True` to combine with custom tools).
- **MCP toolsets must be defined synchronously in `agent.py`** for deployment; async creation only works with `adk web`.
- **`adk web` is not for production** — use `adk api_server`, Cloud Run, GKE, or Agent Runtime.
- **Model IDs change**; `gemini-flash-latest` is the common alias but regional endpoints may need a pinned version. Configure via env, don't hardcode.

## Example scripts (assets/examples/)

Copy and adapt these runnable scripts rather than writing from scratch:

- `hello_world.py` — minimal agent with a tool, programmatic Runner (hello world)
- `function_tools.py` — function tools + `ToolContext` session state
- `structured_output.py` — Pydantic `input_schema`/`output_schema` extraction
- `sub_agents.py` — hierarchical multi-agent delegation
- `sequential_workflow.py` — deterministic pipeline via `SequentialAgent` + `output_key` propagation
- `callbacks.py` — `before_tool_callback` / `before_model_callback` / `after_model_callback`
- `google_search.py` — grounding with the prebuilt search tool
- `sessions.py` — multi-turn session state persistence
- `mcp_tools.py` — connect an MCP server (stdio filesystem server) as tools

## References

- `references/getting-started.md` — install, project structure, hello world, run commands, Runner/InMemoryRunner
- `references/agents.md` — LlmAgent constructor, generation config, structured output, instruction templating, modes, planner, code execution
- `references/tools.md` — function tools, ToolContext, return values, LongRunningFunctionTool, AgentTool, google_search, code execution
- `references/orchestration.md` — sub-agents, single_turn/task/chat modes, Sequential/Parallel/Loop agents, Workflow graphs
- `references/sessions-and-state.md` — sessions, state scopes, state update methods, persistence, memory
- `references/events.md` — Event structure, final responses, control signals
- `references/callbacks.md` — callback types, parameter names, skip/continue semantics
- `references/models-and-config.md` — Gemini models, auth env vars, generation/thinking config, retries, Interactions API
- `references/mcp.md` — McpToolset, connection types, filtering, deployment patterns
- `references/observability-and-production.md` — plugins, metrics, evals, deployment targets, CLI reference
