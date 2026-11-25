---
name: adk-reference
description: Using the Agent Develpment Kit for AI Agent Development. Use when
  ADK is referenced in coding or reviewing an AI agent.
---
# Agent Development Kit (ADK) Reference Skill

Expert guidance for building, evaluating, and deploying AI agents using the Google Agent Development Kit (ADK). This skill provides access to fragmented, task-specific documentation to ensure context efficiency while maintaining high-fidelity code generation.

## Reference Index

| Topic | File Path | Key Contents |
| :--- | :--- | :--- |
| **Core & Setup** | `core.md` | Core concepts, Capabilities, Installation (all languages). |
| **Python** | `python.md` | Python Quickstart, Streaming, Coding with AI, Agent Config, Multi-Model support. |
| **Java** | `java.md` | Java Quickstart, Streaming with Java. |
| **TypeScript** | `typescript.md` | TypeScript Quickstart. |
| **Go** | `go.md` | Go Quickstart. |
| **Tutorials** | `tutorials.md` | Progressive Weather Bot (Multi-agent team), Multi-tool agent. |
| **Agents & Workflows** | `agents.md` | Custom agents, LLM Agent, Planner, Workflow Agents (Loop, Parallel, Sequential), Multi-agent Systems. |
| **Built-in Tools** | `tools_integrations.md` | BigQuery, Spanner, GitHub, Stripe, and other platform integrations. |
| **Custom Tools** | `custom_tools.md` | Toolsets, Function tools, Auth, Human Confirmation, REST/OpenAPI integration. |
| **MCP & A2A** | `mcp_a2a.md` | Model Context Protocol, Agent-to-Agent protocol, Remote agents. |
| **Runtime & Deploy** | `runtime_deployment.md` | Runner, API Server, CLI, Web UI, Cloud Run, GKE. |
| **Observability** | `observability_evaluation.md`| Tracing, Logging, Metrics, Trajectory Evaluation. |
| **Architecture** | `safety_context_callbacks.md`| Safety, Callbacks, Context, State, Session, Memory. |
| **System** | `events_artifacts_apps.md`| Events, Artifacts, Apps, Plugins. |
| **Gemini Live** | `streaming_toolkit.md` | Comprehensive Gemini Live API Toolkit (Audio/Video). |
| **Grounding** | `grounding_reference.md` | Google Search Grounding. |

## Instructions for Agents

### 1. Documentation Retrieval Protocol
- **NEVER** read a full reference file unless it is very small (< 100 lines).
- Use `grep_search` on the specific fragment file (e.g., `python.md`) to find the symbol or concept you need.
- Once located, use `read_file` with `start_line` and `end_line` to retrieve only the relevant example or instruction.
- **Goal:** Keep the turn context lean by only importing the "Active Knowledge" required for the current implementation step.

### 2. Code Generation Standards
- **Mock first:** When building new tools, follow the patterns in `tutorials.md` to create mock implementations first to verify agent logic before integrating real APIs.
- **Type Safety:** Always use the language-specific schema definitions (e.g., Zod in TypeScript, Pydantic/Docstrings in Python).
- **Asynchronous Design:** ADK is fundamentally asynchronous. Ensure all Runner interactions use `async/await` and handle event streams properly.

### 3. Debugging Strategy
- If an agent fails to use a tool, check `custom_tools.md` for proper `FunctionTool` registration and docstring requirements.
- If state is not persisting, refer to `safety_context_callbacks.md` for `SessionService` and `State` management rules.
- For streaming issues, consult `streaming_toolkit.md` for `LiveRequestQueue` and `BIDI` configuration.

## Available Resources
- `adk-reference/core.md`
- `adk-reference/python.md`
- `adk-reference/java.md`
- `adk-reference/typescript.md`
- `adk-reference/go.md`
- `adk-reference/tutorials.md`
- `adk-reference/agents.md`
- `adk-reference/tools_integrations.md`
- `adk-reference/custom_tools.md`
- `adk-reference/mcp_a2a.md`
- `adk-reference/runtime_deployment.md`
- `adk-reference/observability_evaluation.md`
- `adk-reference/safety_context_callbacks.md`
- `adk-reference/events_artifacts_apps.md`
- `adk-reference/streaming_toolkit.md`
- `adk-reference/grounding_reference.md`
