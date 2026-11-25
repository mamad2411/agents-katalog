---
name: agent-adapter
description: Add Agent Adapter (the agent-adapter Python package) to a project, or write code with it. Use when the user wants agent tools defined once as Python functions and run in any agent framework (LangChain, LangGraph, CrewAI, Google ADK, OpenAI Agents SDK, Pydantic AI, LlamaIndex, MCP and more), in a backend (FastAPI, Django, Flask, Celery, Lambda, scripts) or on their own, with approvals, budgets, cost tracking and traces.
license: Apache-2.0
---

# Agent Adapter

Agent Adapter turns plain Python functions into agent tools and runs every call through one
executor that applies approvals, budgets, guards, caching, cost and traces. It works with
no framework, inside any backend, or attached to 20+ agent frameworks.

## Before you write code

1. Read the API guide. In a project with the package installed, run `agent-adapter guide`
   (or `python -m agent_adapter guide`). Otherwise fetch
   https://agent-adapter.veloceai.in/llms-full.txt. Use only names that appear there.
2. Look at the project and write down:
   - the Python version (3.11+ is required) and the package manager;
   - the agent framework, if any;
   - the backend or runtime (FastAPI, Django, Flask, Celery, AWS Lambda, scripts, notebooks);
   - the LLM providers it calls;
   - the functions that should become tools, and which of them write, pay, send or delete.
3. Show the user a short plan and wait for a yes before changing files.

## The plan

- **Install:** `pip install agent-adapter`, plus one extra per framework or provider, for
  example `pip install "agent-adapter[langchain]"`. The guide's Install table lists every extra
  and the frameworks that need their own environment.
- **Tools:** decorate with `@registry.tool`. Add `confirm=True` to every tool with a side effect.
- **Executor:** build one `Executor(registry, approval=...)` with an approval port
  (`CallbackApproval`, `DeferredApproval`, or `AutoDeny`) and limits (`RunLimits`, `BudgetHook`).
- **Connect:**
  - a framework: `tools = attach("<framework>", registry, executor=executor)`;
  - async code (FastAPI, async Django): `await executor.run("tool_name", {...})`;
  - sync code (Celery, Flask, scripts): `executor.run_sync("tool_name", {...})`;
  - other languages and agents: the MCP server, the HTTP tool server or A2A, each with
    `executor=executor` and auth.

## Rules

- Never call a tool function directly in production code: that skips validation, approval,
  limits and the cost ledger. Go through the executor or `attach(..., executor=executor)`.
- Never pass an approval to `attach()`; approval belongs to the executor.
- Never log, print or return secrets. Bind secrets with `fixed=` or read them from
  `ToolContext`; never make them model-visible arguments.
- Never use `AutoApprove` for side-effect tools outside tests.
- Never set `retries=` on a side-effect tool unless it is idempotent.
- Import everyday names from `agent_adapter`, errors from `agent_adapter.errors`, and never
  from `agent_adapter.core` or a `_private` module.
- Require auth on every server you expose.

## Moving existing code

- `agent-adapter migrate src/ --diff` lists framework tool definitions and prints a suggested
  patch. It is read-only; review the patch with the user.
- `registry.wrap(obj.method)` turns code you cannot edit into a tool.

## Check your work

- Run the project's tests, then call one tool through the executor and confirm a
  `confirm=True` tool is denied without an approval.
- `agent-adapter doctor` reports which extras are installed and what is missing.

Docs: https://agent-adapter.veloceai.in/ · Source: https://github.com/VeloceAI/agent-adapter
