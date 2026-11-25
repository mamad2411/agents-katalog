---
name: foundry-tool-governance
description: This skill should be used when designing Microsoft Foundry tool surfaces: Foundry Toolbox, tool catalog configuration, MCP servers, Azure Functions, OpenAPI tools, API Management AI Gateway policy, tool versioning, and allowed-tool scoping.
---

# Foundry Tool Governance

Tool governance is the Microsoft-native implementation of the core tool-design principle: keep the agent's callable surface small, unambiguous, permissioned, observable, and versioned. Foundry Toolbox is the preferred abstraction when a team needs a curated tool set rather than a loose pile of MCP servers and OpenAPI definitions.

## When to Activate

Activate this skill when:

- Packaging several tools into a Foundry Toolbox.
- Choosing between built-in Foundry tools, Azure Functions, OpenAPI, MCP, or API Management AI Gateway.
- Scoping which MCP tools an agent may call.
- Versioning and promoting a tool catalog.
- Adding policy, authentication, logging, or throttling around agent tools.

Do not activate this skill for adjacent work owned by other skills:

- Writing generic tool descriptions, schemas, or error payloads: core `tool-design`.
- Designing identity flows for tool calls: `azure-identity-for-agents`.
- Designing retrieval quality or knowledge-source chunking: `azure-agentic-retrieval`.
- Designing human approval boundaries around autonomous action: core `harness-engineering`.

## Core Concepts

Foundry Toolbox should be treated as the curated boundary between the non-deterministic agent and deterministic systems. The toolbox is not just a convenience wrapper. It is where tool selection, versioning, authentication, and governance become explicit.

Use this hierarchy:

| Need | Microsoft-native default |
| --- | --- |
| Built-in knowledge or action | Foundry tool catalog |
| Curated cross-agent tool set | Foundry Toolbox |
| Custom synchronous action | Azure Functions MCP or OpenAPI |
| Existing REST estate | API Management AI Gateway or OpenAPI tool |
| Central policy and throttling | API Management AI Gateway |
| Long-running action | Queue-backed function or workflow with status polling |

## Practical Guidance

Design a toolbox in this order:

1. List the workflows the agent must perform, not the APIs available.
2. Remove overlapping tools before exposing them to the model.
3. Group tools by stable domain boundaries such as `crm`, `devops`, `search`, or `billing`.
4. Put authentication and authorization in Foundry connections, managed identity, OBO, or APIM policy.
5. Give every tool an actionable error response that tells the agent whether to retry, ask, or stop.
6. Create a new Toolbox version for meaningful changes, test it, then promote it.
7. Review traces to confirm the agent calls the intended tool for representative tasks.

## Examples

**Example: toolbox boundary**

```text
Avoid: agent sees twenty raw CRM endpoints.
Prefer: toolbox exposes search_customer, summarize_customer_context, create_follow_up_task.
```

**Example: APIM governance**

```text
Agent -> Toolbox MCP endpoint -> API Management policy -> internal API

The gateway can enforce token limits, route versions, redact headers, and centralize logs without changing the agent prompt.
```

## Guidelines

1. Prefer Foundry built-in tools before custom tools when the capability matches.
2. Prefer Toolbox when multiple agents should share the same curated tool set.
3. Prefer APIM AI Gateway when policy, throttling, or existing REST API exposure matters.
4. Expose workflow-level tools, not raw backend implementation details.
5. Version tool catalogs deliberately and promote only after trace-based validation.

## Gotchas

1. **Toolbox does not fix bad tool descriptions**: A curated endpoint still fails if descriptions overlap or omit recovery guidance.
2. **Raw MCP expansion creates routing noise**: Importing every MCP tool is convenient but can degrade selection. Scope tools before exposing them.
3. **Policy outside the prompt still shapes behavior**: Rate limits, auth failures, and blocked calls must return agent-actionable errors or the model will retry blindly.

## Integration

- core tool-design - Owns the generic tool contract and consolidation principle.
- azure-identity-for-agents - Owns managed identity, OBO, and RBAC choices.
- responsible-ai-guardrails - Adds safety checks and prompt-injection controls around tool use.
- core evaluation - Measures tool call accuracy and task completion.

## References

- Foundry Agent Service overview: https://learn.microsoft.com/azure/foundry/agents/overview
- Foundry tool catalog: https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog
- Tool best practices: https://learn.microsoft.com/azure/foundry/agents/concepts/tool-best-practice
- Azure Functions tools: https://learn.microsoft.com/azure/foundry/agents/how-to/tools/azure-functions
- API Management AI Gateway: https://learn.microsoft.com/azure/api-management/genai-gateway-capabilities

---

## Skill Metadata

**Created**: 2026-05-24
**Last Updated**: 2026-05-24
**Author**: Agent Skills for Context Engineering Contributors
**Version**: azure-0.1.0

