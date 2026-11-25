---
name: ai-agents-category-pointer
description: "Pointer to a library of 20 specialized Ai Agents skills. Use when working on ai-agents-related tasks."
risk: none
---

# Ai Agents Capability Library 🎯

This is a **pointer skill**. The 20 specialized Ai Agents skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **agent-evaluation** — Evaluate agent behavior with versioned cases and explicit verifiers. Use when comparing agent or prompt changes, reproducing failures, or running agent regression tests.
- **agent-manager-skill** — Manage multiple local CLI agents via tmux sessions (start/stop/monitor/assign) with cron-friendly scheduling.
- **ai-agents-architect** — Expert in designing and building autonomous AI agents. Masters tool use, memory systems, planning strategies, and multi-agent orchestration.
- **dispatching-parallel-agents** — Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
- **hosted-agents** — Build background agents in sandboxed environments. Use for hosted coding agents, sandboxed VMs, Modal sandboxes, and remote coding environments.
- **hosted-agents-v2-py** — Build hosted agents using Azure AI Projects SDK with ImageBasedHostedAgentDefinition. Use when creating container-based agents in Azure AI Foundry.
- **lambda-lang** — Native agent-to-agent language for compact multi-agent messaging. A shared tongue agents speak directly, not a translation layer. 340+ atoms across 7 domains; 3x smaller than natural language.
- **langgraph** — Expert in LangGraph - the production-grade framework for building stateful, multi-actor AI applications. Covers graph construction, state management, cycles and branches, persistence with checkpointers, human-in-the-loop patterns, and the ReAct agent pattern.
- **llm-council** — Run Fireworks-hosted open-weight model councils that compare responses and synthesize a final answer.
- **loop-library** — Find, compare, adapt, and design bounded AI-agent feedback loops with explicit checks, stop rules, guardrails, and handoffs.
- **m365-agents-dotnet** — Microsoft 365 Agents SDK for .NET. Build multichannel agents for Teams/M365/Copilot Studio with ASP.NET Core hosting, AgentApplication routing, and MSAL-based auth.
- **m365-agents-ts** — Microsoft 365 Agents SDK for TypeScript/Node.js.
- **mcp-builder** — Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.
- **mcp-builder-ms** — Use this skill when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
- **multi-advisor** — Conselho de especialistas — consulta multiplos agentes do ecossistema em paralelo para analise multi-perspectiva de qualquer topico. Ativa personas, especialistas e agentes tecnicos simultaneamente, cada um pela sua otica unica, e consolida em sintese decisoria final.
- **multi-agent-patterns** — This skill should be used when the user asks to "design multi-agent system", "implement supervisor pattern", "create swarm architecture", "coordinate multiple agents", or mentions multi-agent patterns, context isolation, agent handoffs, sub-agents, or parallel agent execution.
- **open-dynamic-workflows** — Plan, orchestrate, and adversarially verify parallel AI coding agents with a dynamic multi-agent workflow engine.
- **parallel-agents** — Multi-agent orchestration patterns. Use when multiple independent tasks can run with different domain expertise or when comprehensive analysis requires multiple perspectives.
- **pilot-protocol** — Give an AI agent a permanent network address, encrypted P2P messaging, and an installable app store via Pilot Protocol
- **pydantic-ai** — Build production-ready AI agents with PydanticAI — type-safe tool use, structured outputs, dependency injection, and multi-model support.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/ai-agents/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/ai-agents`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
