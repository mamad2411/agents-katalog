---
name: foundry-hosted-agents
description: This skill should be used when designing Microsoft Foundry Hosted Agents and managed agent runtimes: production endpoints, runtime boundaries, sandboxing, scaling, tool execution, runtime state, deployment environments, and operational controls.
---

# Foundry Hosted Agents

Foundry Hosted Agents are the Microsoft-native managed runtime for production agent execution. Use them when the agent should run as a governed service with managed endpoints, tool access, identity, observability, and release controls instead of as a local script or ungoverned orchestration process.

## When to Activate

Activate this skill when:

- Designing a production runtime for a Foundry agent.
- Choosing between Foundry Hosted Agents, Azure Container Apps, Azure Functions, App Service, local orchestration, or a custom agent framework deployment.
- Defining stable agent endpoints, runtime environments, sandbox filesystem behavior, and execution boundaries.
- Deciding where tools execute and how agent runtime identity reaches those tools.
- Planning scale, latency, quotas, timeout behavior, or production operational controls.
- Separating playground experiments from hosted staging and production agents.

Do not activate this skill for adjacent work owned by other skills:

- Channel publishing, version promotion, Teams, or Microsoft 365 Copilot distribution: `agent-publishing`.
- Tool catalog, Toolbox, MCP, OpenAPI, and function governance: `foundry-tool-governance`.
- Entra identity, managed identity, OBO, and RBAC: `azure-identity-for-agents`.
- Generic runtime architecture independent of Azure: core `hosted-agents`.

## Core Concepts

A hosted agent is a runtime boundary. It owns where the agent executes, how requests enter, how tools are reached, what state survives, and which operational controls apply.

Use the shallowest runtime that satisfies control requirements:

| Runtime need | Default |
| --- | --- |
| Managed Foundry agent with platform tools and stable endpoint | Foundry Hosted Agent |
| Custom code-first orchestration with more runtime control | Azure Container Apps or App Service |
| Event-driven tool or narrow action surface | Azure Functions |
| Declarative multi-step process and approvals | Foundry Workflow Agent when preview risk is acceptable |
| Local experimentation | Foundry playground or local framework before promotion |

The runtime choice should follow the agent's operational contract: identity, network access, tool execution, state, observability, latency, scale, and rollback.

## Practical Guidance

1. Start by writing the production contract: endpoint, users, channels, data sources, tools, permissions, latency target, and failure behavior.
2. Use Foundry Hosted Agents when managed runtime, platform tooling, and operational consistency matter more than custom host control.
3. Keep tool execution boundaries explicit: which actions run inside Foundry tools, which call Azure Functions or APIs, and which require external services.
4. Store durable state outside the runtime in Cosmos DB, Blob, ADLS, Azure AI Search, Foundry IQ, or Fabric as appropriate.
5. Attach monitoring, traces, and evaluation evidence before broad rollout.
6. Treat environment configuration as a release artifact: instructions, model deployment, tools, identities, retrieval sources, network access, and runtime settings.

## Examples

**Example: internal knowledge assistant**

```text
Runtime: Foundry Hosted Agent.
Knowledge: Foundry IQ knowledge base plus Azure AI Search for one custom index.
Tools: Curated through Foundry Toolbox.
Identity: Managed identity for platform operations, OBO for user-permissioned data.
State: Cosmos DB for session metadata and durable user preferences.
Release: staging hosted agent, evaluation gate, then production endpoint.
```

**Example: when not to use hosted runtime first**

```text
Need: bespoke long-running workflow with custom scheduler, complex external workers, and advanced queue control.

Prefer: code-first orchestration on Azure Container Apps, with Foundry Agent Service for model and tool surfaces where useful.
Still use: agent-publishing for release governance and responsible-ai-guardrails for safety gates.
```

## Guidelines

1. Prefer Foundry Hosted Agents for Microsoft-native managed production execution.
2. Keep durable memory and audit logs outside the hosted runtime.
3. Make runtime identity and tool identity explicit; do not let tools inherit broad permissions accidentally.
4. Separate development, staging, and production hosted agents.
5. Monitor model calls, tool calls, latency, failures, safety events, and retrieval traces from day one.
6. Keep a rollback path to the previous agent version, tool version, and model deployment.
7. Document preview dependencies and product limits before using hosted features as hard architecture boundaries.

## Gotchas

1. **Hosted does not mean stateful by default**: Persist session state, memories, and handoff artifacts in explicit Azure stores.
2. **Tool execution is part of the runtime boundary**: A hosted agent calling an over-permissioned API is still over-permissioned.
3. **Playground success is not production readiness**: Channel identity, tool latency, private networking, quotas, and monitoring can change behavior.
4. **Preview surfaces can move**: Validate current Hosted Agent capabilities, limits, and SDK/API names before encoding them in deployment automation.
5. **Custom hosts still matter**: Use Container Apps, App Service, or Functions when runtime control is more important than managed agent hosting.

## Integration

- agent-publishing - Owns version promotion, channel distribution, rollout, and rollback.
- foundry-tool-governance - Owns tool catalog, Toolbox, MCP, OpenAPI, and Azure Functions boundaries.
- azure-identity-for-agents - Owns runtime identity, OBO, RBAC, and tenant boundaries.
- azure-memory-state - Owns durable state outside the hosted runtime.
- responsible-ai-guardrails - Owns evaluation gates, safety monitoring, and red-team evidence.
- core hosted-agents - Owns the generic hosted-agent architecture.

## References

- Microsoft Foundry Agent Service overview: https://learn.microsoft.com/azure/foundry/agents/overview
- Foundry Agent Service concepts: https://learn.microsoft.com/azure/foundry/agents/concepts/agents
- Foundry tools overview: https://learn.microsoft.com/azure/foundry/agents/concepts/tools
- Publish agents to Microsoft 365 Copilot and Teams: https://learn.microsoft.com/azure/foundry/agents/how-to/publish-copilot
- Azure Container Apps documentation: https://learn.microsoft.com/azure/container-apps/
- Azure Functions documentation: https://learn.microsoft.com/azure/azure-functions/

---

## Skill Metadata

**Created**: 2026-05-24
**Last Updated**: 2026-05-24
**Author**: Agent Skills for Context Engineering Contributors
**Version**: azure-0.1.0

