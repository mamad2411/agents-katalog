---
name: blazing-agents
description: Blazing Agents integration work for BA Agents, Providers, Prompts, Sessions, Turns, runtime Skills, Tools, MCP Connections, Memory, Workspaces, Artifacts, Tasks, usage, CLI, and SDK clients. Use when Blazing Agents or BA context is explicit. Do not use for generic AI-agent, Vercel AI SDK, sandbox, or task questions without BA context.
metadata:
  author: Blazing Agents
  version: "0.1.0"
---

# Blazing Agents

Blazing Agents (BA) supplies hosted infrastructure for production agents:
configuration, execution, Tools, secure Workspaces, automation, and usage
tracking. This coding-agent Skill guides development against BA; a runtime
Skill is an Agent-owned resource loaded by the BA runtime.

Keep credentials on a backend. Tenant context comes from the credential, never
from caller-selected input. Attribution is data for filtering and reporting,
not authentication or authorization. Use public APIs instead of internal
storage.

1. Understand the outcome, stack, and trust boundary. This is complete when
   every BA concept in the request maps directly to a reference below.
2. Inspect the selected public docs and current contracts. This is complete
   when every signature, schema, limit, error, and behavior the change depends
   on has a canonical source; report any missing source instead of guessing.
3. Implement against the public surface, then verify proportionally. This is
   complete after focused checks for a narrow change or the consuming
   project's full required gate for an integration change passes.

## Agents

- [Agents](references/agents/agents.md): choose and configure the hosted behavior boundary.
- [Providers and models](references/agents/providers-and-models.md): connect Tenant credentials and select a model.
- [Prompts](references/agents/prompts.md): manage reusable parameterized input.
- [Versions and lifecycle](references/agents/versions-and-lifecycle.md): pin, inspect, restore, enable, or disable Agent configuration.
- [Runtime Skills](references/agents/skills.md): package progressively loaded Agent guidance and resources.
- [Memory](references/agents/memory.md): store and retrieve durable Agent context.
- [Workspaces](references/agents/workspaces.md): attach durable file state used by Workspace Tools.
- [Artifacts](references/agents/artifacts.md): deliberately publish files as durable deliverables.
- [Generation and streaming](references/agents/output/generation-and-streaming.md): choose stateful chat or stateless text generation and relay output.
- [Structured output](references/agents/output/structured-output.md): generate schema-constrained data in a stateless Turn.
- [Built-in Tools](references/agents/tools/built-in-tools.md): select BA-hosted Tool groups and understand execution boundaries.
- [MCP Tools](references/agents/tools/mcp-tools.md): attach an MCP Connection to expose remote Tools to an Agent.
- [Tool approvals](references/agents/tools/tool-approvals.md): continue an exact sensitive Tool call after a durable human decision.

## Platform

- [Sessions and Turns](references/platform/sessions-and-turns.md): persist interactive history and reason about one metered execution.
- [Tenancy and Attribution](references/platform/tenancy-and-attribution.md): preserve credential-derived Tenant isolation and optional end-user data.
- [Security and credentials](references/platform/security-and-credentials.md): place API and Provider credentials at trusted boundaries.
- [Usage and quotas](references/platform/usage-and-quotas.md): query metering and handle quota outcomes.
- [Limits and reliability](references/platform/limits-and-reliability.md): look up current limits and design retries, idempotency, and recovery.

## Automation

- [Tasks](references/automation/tasks.md): define asynchronous Agent work and optional scheduling.
- [Task runs](references/automation/task-runs.md): start, observe, cancel, and troubleshoot one Task execution.
- [Schedules](references/automation/schedules.md): choose one-time, interval, or cron timing for a Task.

## CLI

- [Setup and authentication](references/cli/setup-and-authentication.md): install the current CLI and authenticate a trusted terminal.
- [`ba chat`](references/cli/chat.md): start or resume an interactive terminal Session.
- [`ba run`](references/cli/run.md): execute one script-friendly prompt.
- [`ba assist`](references/cli/assist.md): work with the Tenant's Admin Agent.
- [Scripting and CI](references/cli/scripting-and-ci.md): automate supported CLI workflows safely.

## SDK

Python uses synchronous `BlazingAgents` and asynchronous `AsyncBlazingAgents`;
their resource coverage is identical.

- [Python client](references/sdk/python/client.md): construct and own the root clients, request options, lifecycle, and generation methods.
- [Python Agents](references/sdk/python/agents.md): `agents` resource.
- [Python Artifacts](references/sdk/python/artifacts.md): `artifacts` resource.
- [Python Providers](references/sdk/python/providers.md): `providers` resource.
- [Python MCP Connections](references/sdk/python/mcp-connections.md): `mcp_connections` resource.
- [Python Memories](references/sdk/python/memories.md): `memories` resource.
- [Python Prompts](references/sdk/python/prompts.md): `prompts` resource.
- [Python Sessions](references/sdk/python/sessions.md): `sessions` resource.
- [Python Skills](references/sdk/python/skills.md): `agent(agent_id).skills` resource.
- [Python Tasks](references/sdk/python/tasks.md): `tasks` resource, including Task runs.
- [Python Workspaces](references/sdk/python/workspaces.md): `workspaces` resource.
- [Python Tenant](references/sdk/python/tenant.md): `tenant` resource.
- [Python Usage](references/sdk/python/usage.md): `usage` resource.
- [TypeScript client](references/sdk/typescript/client.md): construct the root client, request options, and direct generation methods.
- [TypeScript Agents](references/sdk/typescript/agents.md): `agents` resource.
- [TypeScript Artifacts](references/sdk/typescript/artifacts.md): `artifacts` resource.
- [TypeScript Providers](references/sdk/typescript/providers.md): `providers` resource.
- [TypeScript MCP Connections](references/sdk/typescript/mcp-connections.md): `mcpConnections` resource.
- [TypeScript Memories](references/sdk/typescript/memories.md): `memories` resource.
- [TypeScript Prompts](references/sdk/typescript/prompts.md): `prompts` resource.
- [TypeScript Sessions](references/sdk/typescript/sessions.md): `sessions` resource.
- [TypeScript Skills](references/sdk/typescript/skills.md): `agent(agentId).skills` resource.
- [TypeScript Tasks](references/sdk/typescript/tasks.md): `tasks` resource, including Task runs.
- [TypeScript Workspaces](references/sdk/typescript/workspaces.md): `workspaces` resource.
- [TypeScript Tenant](references/sdk/typescript/tenant.md): `tenant` resource.
- [TypeScript Usage](references/sdk/typescript/usage.md): `usage` resource.
