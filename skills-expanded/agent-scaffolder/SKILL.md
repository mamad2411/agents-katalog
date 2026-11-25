---
name: agent-scaffolder
description: Generate a runnable Python project from an Agent Build Spec. Turns architecture documents into working code with a controller loop, tool stubs, session state, permission checks, and observability.
---
# Agent Scaffolder

## When To Use This Skill
Use this skill when:
- You have an Agent Build Spec (from the production agent architecture skill or written by hand).
- You want to turn that spec into a runnable Python project, not just documentation.
- You want a starting point that already has the right architecture: loop, tools, permissions, state, logging.

## Prerequisites
The input should be an Agent Build Spec with at least these sections:
- Domain and user goal
- Tools (names and descriptions)
- Session state (fields)
- Permissions and approvals (which tools are auto-allow, ask-first, deny)
- Controller loop (steps)

## Output Structure

Generate a Python project with this layout:

```
your-agent/
  src/
    __init__.py
    agent.py          # Controller loop
    tools.py          # Tool contracts and executor stubs
    state.py          # Session state dataclass
    permissions.py    # Runtime permission policy
    observability.py  # Structured JSON logging
    main.py           # CLI entry point
  requirements.txt
  README.md
```

## File-By-File Instructions

### src/state.py

Define a `SessionState` dataclass with:
- Every field from the spec's "Session state" section, typed appropriately.
- A `session_id` field (auto-generated UUID).
- A `turn_count` integer.
- A `tool_history` list for recording every tool call.
- A `completed` boolean and `failure_reason` optional string.
- Token tracking: `total_input_tokens` and `total_output_tokens`.
- A `record_tool_call()` method and a `summary()` method.

Use `dataclasses.dataclass` with `field(default_factory=...)` for mutable defaults.

### src/tools.py

For each tool in the spec:
1. Define a tool contract dict with: `name`, `description`, `input_schema` (JSON Schema), `permission` (from the spec), `timeout_seconds`, and `side_effects`.
2. Define a mock executor function `_exec_{tool_name}(inp: dict) -> dict` that returns realistic placeholder data.
3. Collect all contracts in a `TOOL_CONTRACTS` list.
4. Provide a `_anthropic_tools()` function that converts contracts to Anthropic API format.
5. Provide an `execute_tool(tool_name, raw_input) -> (json_result, latency_ms)` function.

Mark the mock executors clearly so users know where to plug in real integrations.

### src/permissions.py

Define:
- A `PermissionLevel` enum: `AUTO_ALLOW`, `ASK_FIRST`, `DENY`.
- A `check_permission(tool_name) -> PermissionLevel` function that reads from the tool contracts.
- A `request_human_approval(tool_name, tool_input) -> bool` function using CLI input (with a comment noting this should be replaced with Slack, web UI, etc. in production).

### src/observability.py

Define structured JSON logging functions:
- `log_event(event_type, data, session_id)` — base logger to stderr.
- `log_tool_call(session_id, turn, tool_name, latency_ms, success, error)`.
- `log_approval(session_id, turn, tool_name, approved)`.
- `log_turn(session_id, turn, input_tokens, output_tokens)`.
- `log_session_end(session_id, summary)`.

### src/agent.py

This is the core. Generate:

1. A `SYSTEM_PROMPT` string that:
   - Describes the agent's role from the spec's Domain section.
   - Lists rules derived from the spec's Permissions, Stop conditions, and Core workflow.
   - Includes `{tool_names}` and `{state_summary}` template variables.

2. A `_build_system_prompt(state) -> str` function.

3. A `run_agent(user_goal, **kwargs) -> SessionState` function implementing:
   - Initialize the Anthropic client and session state.
   - Loop up to `MAX_TURNS`:
     - Build the system prompt with current state.
     - Call `client.messages.create()` with system, tools, and messages.
     - Track token usage.
     - If the model returned no tool calls, print the final response and break.
     - For each tool call:
       - Check permission via `permissions.check_permission()`.
       - If DENY, return error to model.
       - If ASK_FIRST, call `request_human_approval()`. On denial, stop.
       - If allowed, call `tools.execute_tool()`.
       - Log everything via `observability`.
       - Update session state with domain-specific results.
     - Check stop conditions.
   - Return final session state.

### src/main.py

A simple CLI using `argparse`:
- Positional `goal` argument with a sensible default.
- Any domain-specific flags (e.g., `--campaign`, `--repo`, `--ticket`).
- Call `run_agent()` and print the session summary.

### requirements.txt

```
anthropic>=0.42.0
```

### README.md

Include:
- One-paragraph description of what this agent does.
- Quick start: install, set API key, run.
- Architecture overview: which file does what.
- How to adapt: replace tool executors, update system prompt, adjust permissions.
- Environment variables table.

## Style Rules

- Use type hints everywhere.
- Use `from __future__ import annotations` in every file.
- No comments that just narrate what the code does. Only explain non-obvious decisions.
- Keep the controller loop in `agent.py` clean and readable; push details into other modules.
- Mock executors should return data that looks realistic for the domain.

## What NOT To Do

- Do not generate a one-shot script. The controller loop must be a real loop.
- Do not skip the permission check. Even if all tools are auto-allow, the check function must exist.
- Do not hardcode the API key. Use `os.environ.get("ANTHROPIC_API_KEY")`.
- Do not skip observability. Every tool call and every turn must be logged.
- Do not generate empty files. Every file should have real, functional code.
