---
name: claude-api-apps
description: Build, scaffold, refactor, and troubleshoot Claude-powered applications that combine an MCP server and/or the Anthropic API. Use when Claude Code needs to design tools, register MCP resources, wire the Anthropic SDK or Claude API, apply MCP metadata or security settings, or produce a docs-aligned project scaffold. Prefer a docs-first workflow by consulting Anthropic developer docs before generating code.
---

# Claude API Apps

## Overview

Scaffold Claude-powered application implementations with a docs-first, example-first workflow, then generate code that follows current Anthropic SDK and MCP patterns.

Use this skill to produce:

- A primary app-archetype classification and repo-shape decision
- A tool plan (names, schemas, annotations, outputs)
- An MCP server scaffold (resource registration, tool handlers, metadata)
- A client scaffold using the Anthropic SDK (`@anthropic-ai/sdk` or `anthropic` Python package)
- A reusable Node or Python starter scaffold for common integration patterns
- A validation report against the minimum working repo contract
- Local dev and testing setup steps
- A short stakeholder summary of what the app does (when requested)

## Mandatory Docs-First Workflow

Consult the Anthropic developer docs first whenever building or changing a Claude-powered app.

1. Use the `anthropic-docs` skill (preferred) or fetch docs from `docs.anthropic.com` directly.
2. Fetch current SDK and API docs before writing code, especially:
   - `api/messages`
   - `api/tool-use`
   - `sdk/overview`
   - `mcp/overview`
   - `claude-code/sdk`
3. Fetch deployment/integration docs when the task includes production hosting or agent orchestration.
4. Cite the doc URLs you used when explaining design choices or generated scaffolds.
5. Prefer current docs guidance over older patterns when they differ.

## Prompt Guidance

Use prompts that pair this skill with `$anthropic-docs` so the resulting scaffold is grounded in current docs.

Preferred prompt patterns:

- `Use $claude-api-apps with $anthropic-docs to scaffold a Claude app for <use case> with a <TS/Python> backend.`
- `Use $claude-api-apps with $anthropic-docs to build an MCP server that exposes <tools> to Claude.`
- `Use $claude-api-apps and $anthropic-docs to refactor this Anthropic SDK integration to use tool use and streaming.`
- `Use $claude-api-apps with $anthropic-docs to plan tools first, then generate the MCP server and client code.`

When responding, ask for or infer these inputs before coding:

- Use case and primary user flows
- Read-only vs mutating tools
- Demo vs production target
- Backend language (TypeScript/Python)
- Auth requirements
- External API domains
- Hosting target and local dev approach
- Streaming requirements

## Classify The App Before Choosing Code

Before choosing examples, repo shape, or scaffolds, classify the request into one primary archetype:

- `api-only` — direct Anthropic API calls, no MCP server
- `mcp-server` — MCP server exposing tools/resources to Claude
- `mcp-client` — Claude Code extension or client that connects to MCP servers
- `agent` — multi-step autonomous agent using tool use loops
- `streaming` — real-time streaming responses with partial output handling

## Default Starting-Point Order

For greenfield apps, prefer these starting points in order:

1. **Official Anthropic SDK examples** when a close example already matches the requested stack.
2. **MCP SDK examples** (`@modelcontextprotocol/sdk`) when the user needs MCP server/client wiring.
3. **Local scaffold** only when no close example fits or network access is undesirable.

## Build Workflow

### 1. Plan Tools Before Code

Define the tool surface area from user intents.

- Use one job per tool.
- Write tool descriptions that start with "Use this when..." behavior cues.
- Make inputs explicit and machine-friendly (enums, required fields, bounds).
- Set `input_schema` accurately with JSON Schema.
- Decide whether each tool is read-only or mutating.

### 2. Choose an App Architecture

Choose the simplest structure that fits the goal.

- Use **API-only** for direct Claude integrations without tool servers.
- Use **MCP server** when exposing tools or data sources to Claude Code or other MCP clients.
- Use **agent loop** for multi-step autonomous work with tool use.

### 3. Scaffold the MCP Server (if needed)

Generate a server that:

- Registers tools with clear names, schemas, and descriptions
- Returns structured results that Claude can parse
- Keeps handlers idempotent or documents non-idempotent behavior explicitly
- Uses the `@modelcontextprotocol/sdk` (Node) or `mcp` (Python) package

### 4. Scaffold the Anthropic API Client

Generate a client that:

- Uses the official `@anthropic-ai/sdk` (Node) or `anthropic` (Python) package
- Includes prompt caching where applicable (`cache_control` on large context blocks)
- Handles streaming with `stream()` or `messages.stream()` when real-time output is needed
- Implements the tool use loop correctly: send tools, handle `tool_use` blocks, return `tool_result`

### 5. Add Security and Configuration

- Store API keys in environment variables, never hardcoded
- Use `ANTHROPIC_API_KEY` as the standard env var name
- Validate tool inputs before executing side effects
- Add rate limiting and error handling for API calls

### 6. Validate the Local Loop

- Run the lowest-cost checks first: static review, syntax/compile checks
- Test tool calls end-to-end with real Claude responses
- Verify streaming output if used
- Check tool error handling with intentionally bad inputs

### 7. Plan Production Hosting

When the user asks to deploy, generate hosting guidance:

- Host behind a stable HTTPS endpoint
- Configure secrets outside the repo (environment variables / secret manager)
- Add logging and request latency tracking for API calls
- Add basic observability and a troubleshooting path

## Output Expectations

When using this skill to scaffold code, produce output in this order:

1. Primary app archetype chosen and why
2. Tool plan and architecture choice
3. Starting point chosen (official example or local scaffold) and why
4. Doc pages/URLs used
5. File tree to create or modify
6. Implementation (server + client)
7. Validation performed
8. Local run/test instructions
9. Deployment/hosting guidance (if requested)
10. Risks, gaps, and follow-up improvements

## References

- `references/app-archetypes.md` for classifying requests into supported app shapes
- `scripts/scaffold_node_ext_apps.mjs` for a minimal Node fallback starter scaffold
