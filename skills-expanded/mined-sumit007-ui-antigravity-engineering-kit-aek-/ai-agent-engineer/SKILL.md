---
name: ai-agent-engineer
description: Architect production AI agents, Model Context Protocol (MCP) servers, tool-calling pipelines, RAG systems, and deterministic evaluation suites. Enforces safe sandboxing and least-privilege tool execution.
---

# AI Agent Engineer Skill

## Purpose
Directs the architecture of production AI coding agents, tool-calling loops, context engineering, and MCP servers.

## When to Use
- Implementing or extending MCP servers and agent tool dispatchers.
- Building multi-agent collaboration pipelines and autonomous workflows.
- Auditing agent permissions, filesystem boundaries, and prompt safety.

## Engineering Workflow
1. **Tool Interface Design**: Define typed schemas for every tool with explicit argument validation.
2. **Context Engineering**: Curate minimal, high-density context windows; avoid dumping raw unindexed data.
3. **Verification**:
   - Validate MCP JSON-RPC protocol compliance across stdio and streamable HTTP transports.
   - Run prompt regression test suites with Promptfoo.

