---
name: openai-agents-sdk
description: This skill builds AI agents with the official OpenAI Agents SDK for Python (`pip install openai-agents`), from hello world to professional production systems. Use whenever the user is writing agent code with the `agents` package — Agent, Runner.run/run_sync/run_streamed, @tool / function_tool, handoffs, agents-as-tools, input/output/tool guardrails, structured outputs (output_type), sessions & memory, RunConfig, ModelSettings, tracing, MCP servers, or multi-agent orchestration. Also use for questions about how the SDK works, its current API surface, or converting an idea into an agentic app. Provides the correct, docs-grounded API (no guessed imports).
---

# OpenAI Agents SDK (Python)

## Overview

The OpenAI Agents SDK is a lightweight, Python-first package for building agentic AI apps with very few abstractions: **Agents** (LLMs with instructions and tools), **Agents as tools / Handoffs** (delegation), **Guardrails** (input/output validation), **Sessions** (memory across turns), and **Tracing** (observability). `Runner` executes agents with a built-in loop that manages turns, tool calls, handoffs, guardrails, and sessions.

Ground all code in the official docs. This skill's reference files reproduce the documented API — never invent imports or parameters.

## Core workflow (hello world)

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```

Setup: `pip install openai-agents`, then set `OPENAI_API_KEY`. The SDK is async-first: use `await Runner.run(...)` inside an `async def main()` (or `asyncio.run(main())`); `Runner.run_sync()` for scripts.

## How to use this skill

1. Identify what the user is building (single agent → tools → multi-agent → production).
2. Read the matching reference file(s) below **before writing agent code**.
3. Use the example scripts in `assets/examples/` as starting points; adapt them to the user's needs.
4. For anything beyond these guides, consult the official docs (`https://openai.github.io/openai-agents-python/`); model IDs change and docs examples lag — prefer configurable model selection.

## Before implementing

Gather context before writing agent code:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing Python project layout, framework (FastAPI/Flask/CLI), dependency manager, where the agent will be invoked |
| **Conversation** | The agent's purpose, who calls it, single-turn vs multi-turn, required model/provider, streaming needs |
| **Skill references** | The reference file for the feature being built (see decision guide below) |
| **User guidelines** | Available API keys/secrets, deployment environment, existing DB/Redis for sessions |

## Clarify when ambiguous

Ask only what the code cannot tell you — never ask the user to recall SDK API details (this skill embeds them). Limit to 1–2 questions up front.

- **Required** (ask before building if unknown)
  - What does the agent do end-to-end, and who/what invokes it (CLI, web endpoint, background job)?
  - Is the interaction multi-turn (needs sessions/memory) or single-turn?
- **Optional** (only if relevant)
  - Custom model/provider vs the default, and is an API key already configured?
  - Streaming UX (`run_streamed`) vs a full `RunResult`?
  - Is a persistence backend already available (Postgres/Redis/SQLite) for sessions?

## Learning path: hello world → production

| Stage | What the user learns to build | Read first |
|---|---|---|
| 1. Hello world | Install, first agent, `Runner.run/run_sync`, the agent loop | `references/getting-started.md` |
| 2. Agents & tools | `@tool` functions, hosted tools, `output_type` structured output, context | `references/agents.md`, `references/tools.md` |
| 3. Multi-agent | Handoffs, agents-as-tools, manager pattern, code-driven orchestration | `references/orchestration.md` |
| 4. Safety | Input/output/tool guardrails, tripwires | `references/guardrails.md` |
| 5. State | Multi-turn memory: `to_input_list()`, sessions, session backends | `references/state-and-sessions.md` |
| 6. Models | Model selection, providers, `ModelSettings`, env config | `references/models-and-config.md` |
| 7. Observability | Tracing, `group_id`, trace dashboard | `references/observability.md` |
| 8. Production | Error handlers, approvals, RunConfig hardening, durable execution, checklist | `references/production.md` |
| Extras | MCP servers as tools | `references/mcp.md` |

## Decision guide (jump straight to the right file)

- **"Hello world" / first run / how does Runner work?** → `getting-started.md`
- **Agent configuration** (name, instructions, output_type, hooks, context types, tool_use_behavior) → `agents.md`
- **Tools** (@tool, schemas, hosted tools, timeouts, error handling) → `tools.md`
- **Agent orchestration** (handoffs vs agents-as-tools, which to pick) → `orchestration.md`
- **Validate input/output/tool calls** → `guardrails.md`
- **Conversation memory / sessions / backends** → `state-and-sessions.md`
- **Which model / provider / temperature** → `models-and-config.md`
- **Traces, group_id, disabling tracing, custom processors** → `observability.md`
- **Connect an MCP server** (stdio, HTTP, hosted) → `mcp.md`
- **Robustness, evals, deployment, human-in-the-loop** → `production.md`

## Key rules (verified against official docs)

- **Import `@tool` from `agents.decorators`** — the documented decorator. The legacy `function_tool` is still exported from `agents` and behaves identically.
- **Guardrail decorators** live in `agents.decorators`: `input_guardrail`, `output_guardrail`, `tool_input_guardrail`, `tool_output_guardrail`.
- **`Agent` + `Runner`** = the SDK manages turns, tools, guardrails, handoffs, sessions for you. Use the Responses API directly only when you want to own the loop yourself.
- **`name` is required** on every Agent; `instructions` is strongly recommended.
- **Final output rule:** an agent's output is final only when it produces text with the desired type and there are no tool calls.
- **Sessions cannot combine** with `conversation_id`, `previous_response_id`, or `auto_previous_response_id` in the same run.
- **Input guardrails** run only on the first agent; **output guardrails** only on the final agent; **tool guardrails** wrap every custom `@tool` call.
- **`tool_choice` auto-resets to `auto`** after a tool call (`reset_tool_choice=True`) to prevent infinite loops.
- **Hosted tools** (`WebSearchTool`, `FileSearchTool`, `ToolSearchTool`, etc.) require `OpenAIResponsesModel`.
- **Tracing is on by default.** Disable via `OPENAI_AGENTS_DISABLE_TRACING=1`, `set_tracing_disabled(True)`, or `RunConfig(tracing_disabled=True)`.
- **Default model** is `gpt-5.4-mini` (overridable via `OPENAI_DEFAULT_MODEL` or `RunConfig(model=...)`). Model IDs in docs examples lag reality — configure via env/config, don't hardcode.

## Example scripts (assets/examples/)

Copy and adapt these runnable scripts rather than writing from scratch:

- `hello_world.py` — minimal sync agent (hello world)
- `function_tools.py` — agents with `@tool` functions (async + context)
- `structured_output.py` — Pydantic `output_type` extraction
- `handoffs.py` — triage agent routing to specialists
- `multi_agent.py` — orchestrator calling specialists via `as_tool()`
- `guardrails.py` — input + output guardrail with tripwires
- `sessions.py` — multi-turn conversation with `SQLiteSession`

## References

- `references/getting-started.md` — install, hello world, Runner API, agent loop, RunResult, streaming, exceptions
- `references/agents.md` — Agent constructor, structured output, context types, dynamic instructions, hooks
- `references/tools.md` — @tool, hosted tools, timeouts, errors, agents-as-tools, tool search
- `references/orchestration.md` — handoffs, handoff customization, manager pattern, code-driven patterns
- `references/guardrails.md` — input/output/tool guardrails, tripwires
- `references/state-and-sessions.md` — memory strategies, session backends, session operations
- `references/models-and-config.md` — model selection, providers, ModelSettings, env vars, RunConfig
- `references/observability.md` — tracing, group_id, sensitive data, custom processors
- `references/mcp.md` — HostedMCPTool, MCPServerStdio/StreamableHttp/Sse, server manager, filtering
- `references/production.md` — error handlers, approvals, RunConfig hardening, durable execution, checklist
