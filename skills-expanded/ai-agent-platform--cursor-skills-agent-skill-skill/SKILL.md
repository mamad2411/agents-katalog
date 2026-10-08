---
name: agent-skill
description: Generate agents, agent configurations, system prompts, and agent registry entries. Use when creating agents, modifying agent behavior, or when the user mentions research agent, coding agent, chat agent, or multi-agent coordination.
---

# Agent Skill -- AI Agent Platform

## When this skill applies

Use this skill when generating:

- new agents or modifying existing agents
- system prompts for agents
- agent registry entries
- agent-to-tool bindings
- multi-agent coordination logic

---

# Agent Technology

**Sub-agents** (research, analysis, generator, code, monitor) use **CrewAI crews** as sub-agents inside LangGraph. Each is implemented as a single-agent CrewAI crew with role, goal, and backstory. Tools are LangChain `@tool` wrappers converted to CrewAI via `Tool.from_langchain()` in `services/agents/crewai_agents.py`.

**Special agents** (chat, plan_execute, scheduler) use their original implementations:
- **chat** — simple LLM chat (no tools)
- **plan_execute** — planner LLM + CrewAI analysis crew as executor
- **scheduler** — scheduler-specific logic (no CrewAI)

All LLM calls use the shared factory in `shared/llm.py` (OpenAI default `gpt-4o-mini`).

---

# Agent Design Philosophy

Agents are **specialized** components -- each agent is expert in a particular domain (research, analysis, code, generation, monitoring, chat).

Agents must:

- solve a specific problem
- be modular and stateless
- produce string output
- access external systems only through MCP tools

Agents must never contain API logic, infrastructure code, or database access.

---

# Agent-to-User Communication

**Agents never talk to the user directly.** All agent-to-user communication goes through the Supervisor (LangGraph StateGraph).

- Agents return results to the Supervisor via the execute node
- The Supervisor evaluates results and decides whether to replan or deliver
- The Delivery Service formats the final output for the user

---

# Agent Implementation Standard

**CrewAI sub-agents** (research, analysis, generator, code, monitor): Add a new entry to `_CREW_DEFS` in `services/agents/crewai_agents.py` with role, goal, backstory. The registry maps agent types to `run_research`, `run_analysis`, etc. Tools come from `TOOL_REGISTRY` and are converted via `Tool.from_langchain()`.

```python
# services/agents/crewai_agents.py
_CREW_DEFS = {
    "my_agent": (
        "Role Name",
        "Goal: what the agent achieves. Mention tools: web_search, execute_python, etc.",
        "Backstory: expert context and behavior.",
    ),
}
# Add run_my_agent() and register in AGENT_REGISTRY
```

**Non-CrewAI agents** (chat, scheduler): Use their existing patterns (chat_agent.py, scheduler_agent.py).

After adding a CrewAI agent:

1. Add to `_CREW_DEFS` and create `run_<type>` in `crewai_agents.py`
2. Register in `services/agents/registry.py` `AGENT_REGISTRY`
3. Assign tools in `shared/mcp/server.py` `TOOL_REGISTRY` (and `get_tools_for_agent`)

Agents with `tool_execute_python` in their tool set are automatically treated as code-approval agents when `require_code_approval` is true (derived from `TOOL_REGISTRY`, not hardcoded).

---

# Current Agent Pool

| Agent | Implementation | Tools | Purpose |
|-------|----------------|-------|---------|
| research | CrewAI (`crewai_agents.py`) | web_search, scrape_url | Web search and data gathering |
| analysis | CrewAI (`crewai_agents.py`) | web_search, execute_python, read_file | Summarization, comparison |
| generator | CrewAI (`crewai_agents.py`) | web_search, write_file, read_file, execute_python | Report/document creation |
| code | CrewAI (`crewai_agents.py`) | execute_python, read_file, write_file, list_files | Calculations, data processing |
| monitor | CrewAI (`crewai_agents.py`) | web_search, scrape_url | Long-running observation |
| chat | `chat_agent.py` | (none) | Casual conversation |
| plan_execute | `plan_execute_agent.py` | planner + CrewAI analysis executor | Complex multi-step tasks |
| scheduler | `scheduler_agent.py` | scheduler tools | Recurring task scheduling |

---

# Agent State

The Supervisor manages workflow state via `WorkflowState` (TypedDict). Individual agents are stateless -- they receive a message string and return a result string.

```python
class WorkflowState(TypedDict, total=False):
    goal: str
    output_format: str
    format_hint: str         # Agent-inferred planner instruction (from preference_inference)
    is_clarification_resume: bool  # Skip classify when resuming after clarification
    intent: str              # casual | simple | complex | monitor (agent-decided)
    next_node: str          # chat_respond | ask_user | plan (agent-decided routing)
    plan: Optional[ExecutionPlan]
    step_results: list[StepResult]
    iteration_count: int
    goal_achieved: bool
    final_result: Optional[str]
```

**Agent-driven decisions:** The classify node returns `next_node` directly (no hardcoded intent→node mapping). Code-approval agent types are derived from `TOOL_REGISTRY` (agents that have `tool_execute_python`), not hardcoded.

---

# Key Files

- `services/agents/crewai_agents.py` -- CrewAI crews for research, analysis, generator, code, monitor; `Tool.from_langchain()` converts MCP tools
- `services/agents/registry.py` -- Agent type → runner mapping (CrewAI runners for sub-agents)
- `services/agents/chat_agent.py`, `scheduler_agent.py`, `plan_execute_agent.py` -- Non-CrewAI agents
- `shared/mcp/server.py` -- Tool registry (agent type → LangChain tools)
- `services/orchestrator/supervisor/nodes/execute.py` -- Agent execution; code-approval agents derived from `TOOL_REGISTRY`
- `shared/preference_inference.py` -- LLM infers output_format, require_code_approval, clean_message, format_hint
