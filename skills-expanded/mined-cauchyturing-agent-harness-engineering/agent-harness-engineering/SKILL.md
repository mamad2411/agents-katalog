---
name: agent-harness-engineering
description: >
  Production-grade design patterns for building agentic CLI tools, AI harnesses,
  and LLM-powered applications. 91 patterns across 9 domains: architecture,
  agentic loops, tool systems, permissions, hooks, LLM integration, caching,
  agent orchestration, terminal UI, and infrastructure. Plus a 58-item audit checklist.
when_to_use: >
  Building an agentic CLI tool, AI coding assistant, MCP server, tool harness,
  agent orchestration system, or any LLM-powered application that executes tools.
  Also useful when designing: permission models, hook/plugin architectures,
  context management strategies, prompt caching schemes, or multi-agent systems.
  Invoke this skill before making architectural decisions in these domains.
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
user-invocable: true
version: "1.0"
source: "Extracted from 512K-line production agentic codebase analysis"
---

# Agent Harness Engineering

> 91 production-proven patterns for building agentic tools.
> By [Stephen](https://github.com/cauchyturing) / [Abel AI](https://github.com/Abel-ai-causality/). Open source under MIT.

## How to use this skill

**Do NOT load all references.** Load only the 1-2 modules relevant to your current task.

| Building... | Load reference |
|-------------|---------------|
| System architecture, entry points, state management | @./references/00-architecture.md |
| The agentic loop, context management, compaction | @./references/01-agentic-loop.md |
| LLM API integration, prompt assembly, caching | @./references/02-llm-integration.md |
| Tool interfaces, lifecycle, registry, concurrency | @./references/03-tool-system.md |
| Subagents, async agents, fork, swarm, task system | @./references/04-agent-orchestration.md |
| Permission model, safety, sandbox, enterprise | @./references/05-permission-safety.md |
| Hooks, plugins, skills, extensibility | @./references/06-hooks-extensibility.md |
| Terminal UI, rendering, infrastructure, config | @./references/07-ui-infrastructure.md |
| Core engineering principles (the "why behind why") | @./references/08-philosophy.md |

## Auditing an existing harness

Use the comprehensive checklist: @./checklists/harness-audit.md

## Key principles (always applicable)

1. **AsyncGenerator as lingua franca** — One composition primitive for loops, tools, hooks, streaming, retry.
2. **Prompt cache is sacred** — Cache bust = 12x cost. Sort tool pools, latch headers, hash paths.
3. **Fail-fast for safety, fail-open for UX** — Security? exit(1). Feature degradation? Continue.
4. **Just enough complexity** — 34-line store > Redux. Pure functions > class hierarchies.
5. **Tool interface IS the extension point** — MCP tools = built-in tools. Same pipeline, same rules.
6. **Persist before the crash boundary** — State on disk before any killable operation.
7. **Hide latency, don't reduce it** — Start I/O before you need the result.

## When reviewing harness code

Apply these diagnostic questions:
- Is there I/O happening that nothing is waiting for yet? (latency hiding)
- If this fails, is it dangerous or merely inconvenient? (fail-fast vs fail-open)
- Does this change bust the prompt cache? (cache stability)
- Can I explain this component in one sentence? (just enough complexity)
- Is external tool execution on the same pipeline as built-in? (extension parity)
- Is state on disk before the crash boundary? (persistence)
- Am I using one async pattern or five? (composition primitive)
