# multi-agent-reference-architecture — Cursor Rules

## Project Identity

`multi-agent-reference-architecture` is the NVIDIA SA capstone reference implementation demonstrating production-ready multi-agent LLM orchestration using LangGraph with fully YAML-driven graph assembly. It is 100% feature-complete and serves as the primary ISV customization surface in the NVIDIA SA portfolio. This repo is what an NVIDIA Solutions Architect shows a customer or ISV partner as the "how to build on NIM" reference. `core/graph_builder.py` reads agent YAML configs and dynamically assembles LangGraph `StateGraph` instances at startup — ISV customization happens entirely in `configs/agents/*.yaml`, with no Python changes required for new agent personas.

**This repo is the upstream reference for ISV partners.** `docs/isv-customization.md` is the critical deliverable differentiating NVIDIA's multi-agent offering. It must always be kept accurate.

## Tech Stack

| Component | Package / Version |
|---|---|
| Python | 3.11 |
| Orchestration | langgraph ≥ 0.2 |
| LLM framework | langchain-core, langchain-openai |
| Tool framework | langchain.tools.StructuredTool, pydantic |
| Config | PyYAML, python-dotenv |
| Observability | langfuse ≥ 2.x |
| Eval | pytest, pytest-asyncio |
| Linting | ruff, mypy |
| Packaging | pyproject.toml |

Never add `torch`, `transformers`, or model training dependencies. This repo is inference and orchestration only.

## Coding Conventions

### General
- All functions and methods **must** have complete type hints (arguments + return type). No bare `Any` without a justifying comment.
- All public functions, classes, and methods **must** have Google-style docstrings with `Args:`, `Returns:`, and `Raises:` sections.
- Never use `print()`. All logging through `import logging; logger = logging.getLogger(__name__)`. Use appropriate levels.
- Use `python-dotenv` (`from dotenv import load_dotenv`) at every entry point. Never hardcode secrets, API keys, or base URLs.
- Constants belong in `ALL_CAPS` module-level variables or YAML config files. No magic strings buried in functions.
- Line length: 100 characters (configured in `pyproject.toml` under `[tool.ruff]`).
- Imports: stdlib → third-party → local, separated by blank lines. `ruff --fix` before committing.

### Error Handling
- Use `tenacity.retry` with `stop=stop_after_attempt(3)` and `wait=wait_exponential(multiplier=1, min=2, max=10)` on all NIM API calls.
- Never swallow exceptions silently. Log before re-raising.
- Graph errors should update the `error` field in state and route to an error-handling terminal node, not crash the graph.

### Async
- All orchestrator, executor, and planner functions must be `async def`.
- Entry point scripts (`examples/`) use `asyncio.run()` as the sole sync boundary.

## LangGraph Patterns

### YAML-Driven Graph Assembly — Core Pattern

The defining pattern of this repo is `core/graph_builder.py` reading a YAML agent config and dynamically wiring a `StateGraph`. This is the ISV customization surface.

**YAML config shape** (`configs/agents/my_agent.yaml`):
```yaml
name: my_agent
model: meta/llama-3.1-70b-instruct
system_prompt: |
  You are a specialized agent that...
tools:
  - query_database
  - call_api
max_iterations: 5
nodes:
  - planner
  - executor
  - reviewer
edges:
  - from: planner
    to: executor
  - from: executor
    to: reviewer
  - from: reviewer
    to: planner
    condition: should_continue
  - from: reviewer
    to: END
    condition: is_complete
```

**Graph builder pattern**:
```python
from langgraph.graph import StateGraph, END
from configs.agents import AgentConfig
from state.schema import AgentState

def build_graph(config: AgentConfig) -> StateGraph:
    """Build a LangGraph StateGraph from an agent YAML config.

    Args:
        config: Parsed agent configuration from YAML.

    Returns:
        StateGraph: Compiled LangGraph graph ready for invocation.
    """
    graph = StateGraph(AgentState)

    node_map = get_node_map()  # maps string names → async node functions
    for node_name in config.nodes:
        graph.add_node(node_name, node_map[node_name])

    for edge in config.edges:
        if edge.get("condition"):
            graph.add_conditional_edges(
                edge["from"],
                get_router(edge["condition"]),
                {True: edge["to"], False: END},
            )
        else:
            graph.add_edge(edge["from"], edge["to"])

    graph.set_entry_point(config.nodes[0])
    return graph.compile()
```

**Never hardcode graph topology in Python.** All node lists and edge definitions live in YAML.

### State
- All graph state **must** be a `TypedDict` defined in `state/schema.py`. Never use plain `dict`.
- Canonical state shape:
  ```python
  from typing import Annotated, TypedDict
  import operator

  class AgentState(TypedDict):
      messages: Annotated[list[BaseMessage], operator.add]
      plan: str
      tool_results: Annotated[list[dict], operator.add]
      final_answer: str
      iteration: int
      error: str | None
      agent_name: str  # which YAML config is active
  ```
- State checkpointing is handled by `state/checkpointer.py`. Never implement custom persistence logic elsewhere.

### Node Naming
- Node names in Python must exactly match node name strings in YAML.
- Naming convention: snake_case verbs — `plan_task`, `execute_tools`, `review_output`, `route_decision`.
- Routers (conditional edge functions) use `should_` prefix: `should_continue`, `should_escalate`.

### Nodes
- All nodes are `async def node_name(state: AgentState) -> dict:`.
- Nodes return only keys they modify (partial state dict).
- `core/planner.py`, `core/executor.py`, `core/reviewer.py` define the canonical Planner→Executor→Reviewer nodes.
- Node implementations must not contain graph wiring logic — that belongs exclusively in `core/graph_builder.py`.

## NIM / LangChain Patterns

### LLM Construction
Always construct `ChatOpenAI` with the Langfuse callback:

```python
from langchain_openai import ChatOpenAI
from core.observability import get_langfuse_handler

def build_llm(model: str) -> ChatOpenAI:
    """Build a ChatOpenAI instance pointed at NIM with Langfuse tracing.

    Args:
        model: NIM model name, e.g. "meta/llama-3.1-70b-instruct".

    Returns:
        ChatOpenAI: Configured LLM instance with tracing enabled.
    """
    return ChatOpenAI(
        model=model,
        base_url=os.environ["NIM_BASE_URL"],
        api_key=os.environ["NIM_API_KEY"],
        temperature=0,
        callbacks=[get_langfuse_handler()],
    )
```

The model name comes from the agent YAML config — never hardcoded.

### StructuredTool Wrappers
- All tools in `tools/` are `langchain.tools.StructuredTool` instances.
- Tool input schemas use `pydantic.BaseModel`. Never use bare `dict`.
- `tools/registry.py` is the single source of truth for available tools. `graph_builder.py` looks up tools by name from the registry.
- Tool names must match exactly between `tools/registry.py` and YAML `tools:` lists.
- Naming convention: `verb_noun` — `query_database`, `call_api`, `read_file`, `write_file`.

## Observability Standard

**Every LLM call in `core/planner.py`, `core/executor.py`, `core/orchestrator.py`, and all example scripts must have Langfuse tracing.**

Create `core/observability.py` as the canonical observability module:

```python
"""Observability utilities for multi-agent-reference-architecture.

All LLM-touching modules import from here — never duplicate handler creation.
"""

import logging
import os

from langfuse.callback import CallbackHandler

logger = logging.getLogger(__name__)


def get_langfuse_handler() -> CallbackHandler:
    """Return a configured Langfuse CallbackHandler.

    Reads LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST from env.
    Logs a warning and operates in no-op mode if credentials are absent.

    Returns:
        CallbackHandler: Configured Langfuse handler.
    """
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY", "")
    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")

    if not public_key or not secret_key:
        logger.warning(
            "Langfuse credentials missing (LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY). "
            "Tracing disabled."
        )

    return CallbackHandler(
        public_key=public_key,
        secret_key=secret_key,
        host=host,
    )


def get_callbacks() -> list[CallbackHandler]:
    """Return the list of all active callback handlers.

    Returns:
        list[CallbackHandler]: List containing the Langfuse handler.
    """
    return [get_langfuse_handler()]
```

- Import `get_callbacks` from `core.observability` in every file that constructs an LLM.
- Add `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` to `.env.template`.

## ISV Customization Surface

**This is the most important section of these rules.** Preserve and protect the ISV customization pattern.

### The Contract
- ISVs customize this architecture by **only editing YAML files** in `configs/agents/`.
- No Python changes should be required to add a new agent persona or pipeline variant.
- `docs/isv-customization.md` documents this contract in full. Keep it up to date after every structural change.

### YAML Agent Config Fields (Required)
| Field | Type | Description |
|---|---|---|
| `name` | string | Agent identifier (snake_case) |
| `model` | string | NIM model name |
| `system_prompt` | string (multiline) | Agent persona and instructions |
| `tools` | list[string] | Tool names from `tools/registry.py` |
| `max_iterations` | int | Loop cap |
| `nodes` | list[string] | Ordered node names to wire |
| `edges` | list[dict] | Edge definitions with optional conditions |

### Existing Agent Configs
- `configs/agents/sales_pipeline.yaml` — Sales prospecting and outreach pipeline.
- `configs/agents/support_triage.yaml` — Customer support triage and routing pipeline.
- `configs/agents/data_analyst.yaml` — Data analysis and reporting pipeline.

When adding a new agent config, always run the corresponding example in `examples/` to verify the graph compiles and runs end-to-end.

### Adding a New Tool
1. Implement the tool function in `tools/` (new file or existing file).
2. Register it in `tools/registry.py` with its `StructuredTool` wrapper.
3. Reference it by the registered name in the YAML `tools:` list.
4. Add a unit test in `tests/test_tools.py`.
5. Document it in `docs/isv-customization.md`.

## Docker & Deployment

- `docker-compose.yml` **must** exist at the **repo root** (developer convenience).
- The root compose file uses `env_file: .env` and build context `.` with `deploy/Dockerfile`.
- `deploy/docker-compose.yml` is the production-parameterized version.
- Never commit actual `.env` files. Only `.env.template` is tracked.

## File & Module Organization

```
multi-agent-reference-architecture/
├── api/               # FastAPI server (server.py)
├── configs/
│   ├── agents/        # Per-agent YAML configs (ISV customization surface)
│   └── tools.yaml     # Global tool configuration
├── core/              # graph_builder, orchestrator, planner, executor, reviewer
│   └── observability.py  # Langfuse/callback handler factory
├── deploy/            # Dockerfile, docker-compose (prod)
├── docs/
│   ├── architecture.md
│   └── isv-customization.md  # CRITICAL — ISV onboarding doc
├── evals/             # pipeline_eval.py
├── examples/          # run_sales_pipeline.py, run_support_triage.py, run_data_analyst.py
├── state/             # schema.py (TypedDict), checkpointer.py
├── tests/             # pytest suite
├── tools/             # api_node, db_node, file_node, registry.py
├── .cursorrules       # This file
├── .env.template      # Environment variable template
├── docker-compose.yml # Root developer convenience compose
└── pyproject.toml
```

- `core/` does not import from `examples/`. Examples are entry points only.
- `tools/` does not import from `core/` (no circular dependency).
- `state/` does not import from `core/` or `tools/`.
- `core/graph_builder.py` imports from `core/`, `tools/`, `state/`, `configs/`.

## What NOT to Do

- **Do not** hardcode LangGraph node topology in Python. All graph topology lives in YAML.
- **Do not** hardcode model names, system prompts, or tool lists in Python. Load from YAML.
- **Do not** use `langchain.agents.AgentExecutor`. Use LangGraph `StateGraph` only.
- **Do not** define graph state as a plain `dict`. Always use `TypedDict` from `state/schema.py`.
- **Do not** add tools to graph builder logic directly — register in `tools/registry.py` first.
- **Do not** use `print()` for any output. Use structured logging.
- **Do not** skip Langfuse callback when constructing any LLM instance.
- **Do not** import from deprecated `langchain.` namespace. Use `langchain_core`, `langchain_openai`.
- **Do not** modify `docs/isv-customization.md` without also verifying the examples still work.
- **Do not** put `docker-compose.yml` only in `deploy/` — the root must always have a compose file.
- **Do not** create new agent configs without a corresponding entry in `examples/`.
- **Do not** use mutable default arguments in function signatures.

## Test Conventions

- Test runner: `pytest` with `pytest-asyncio`.
- All async tests: `@pytest.mark.asyncio`.
- Use `pytest.fixture` for graph and agent config setup in `tests/conftest.py`.
- Mock all NIM API calls. Never make real HTTP calls in unit tests.
- Mock Langfuse with `mocker.patch("langfuse.callback.CallbackHandler")`.
- Test YAML-driven graph assembly: for each agent config in `configs/agents/`, assert `build_graph(config)` returns a compiled graph without raising.
- Test naming: `test_<module>_<scenario>`.
- Minimum coverage: 80% for `core/`, `tools/`, `state/`.
- Integration tests in `tests/integration/` with `@pytest.mark.integration`.

## Cross-Repo Conventions

These conventions are shared across `nvidia-nim-agent-toolkit`, `enterprise-rag-pipeline`, and `multi-agent-reference-architecture`:

1. **dotenv**: Every entry point calls `load_dotenv()` before any config reads.
2. **Linting**: `ruff check . --fix && mypy .` must pass clean before merging.
3. **docker-compose at root**: All repos expose a root-level `docker-compose.yml` for `docker compose up`.
4. **TypedDict state**: LangGraph state is always a `TypedDict`, never a plain dict.
5. **Langfuse tracing**: Every LLM call includes `CallbackHandler` from `langfuse.callback`.
6. **No legacy langchain imports**: Use `langchain_core`, `langchain_openai`, `langchain_community`.
7. **No print() statements**: All output via `logging`.
8. **YAML config pattern**: All agent personas, models, and graph topology live in YAML, not Python.
9. **Google-style docstrings**: All public functions and classes document Args, Returns, Raises.
10. **StructuredTool with Pydantic**: All LangChain tools use Pydantic input models, never bare dicts.
