---
name: azure-identity-for-agents
description: This skill should be used when binding agent access to Microsoft Entra identity: managed identities, RBAC scopes, on-behalf-of access, tenant boundaries, credential-free SDK use, and per-user authorization for tools and grounding sources.
---

# Azure Identity for Agents

Identity is the control plane for enterprise agents. In Microsoft-native systems, an agent should not carry broad static credentials in prompts, tool definitions, or code. It should operate through Entra identity, scoped permissions, and explicit user delegation when the answer depends on a user's private data.

## When to Activate

Activate this skill when:

- Designing agent access to Azure resources, Microsoft 365 data, SharePoint, Fabric, Azure DevOps, or custom APIs.
- Choosing between system-assigned managed identity, user-assigned managed identity, service principal, or on-behalf-of user access.
- Preventing an agent from seeing data beyond the invoking user's permissions.
- Configuring RBAC for Foundry projects, tool connections, or hosted agent infrastructure.
- Removing API keys or secrets from prompts, config files, and tool payloads.

Do not activate this skill for adjacent work owned by other skills:

- Designing the tool schema or description after identity is chosen: `foundry-tool-governance` or core `tool-design`.
- Choosing retrieval architecture without identity-specific access semantics: `azure-agentic-retrieval`.
- Designing autonomous approval and merge boundaries: core `harness-engineering`.

## Core Concepts

Treat identity as part of context engineering because access decisions shape what information enters the model. A retrieval result obtained with a broad service credential can poison context by exposing documents the user could not access. A tool call made with the wrong identity can also produce an action that is technically valid but unauthorized from the user's perspective.

Use three access modes deliberately:

| Mode | Use when | Risk |
| --- | --- | --- |
| Managed identity | The agent or tool acts as a workload against Azure resources | Can become over-broad if RBAC is assigned at subscription or resource-group scope |
| On-behalf-of access | The agent must respect the user's Microsoft 365 or API permissions | Requires tenant alignment and token-flow support |
| Service principal or key | Legacy APIs or bootstrap automation require non-user credentials | Secrets and over-permissioning need stricter governance |

The default should be managed identity for workload access and on-behalf-of for user-private data.

## Practical Guidance

1. Start by classifying each tool as workload-scoped or user-scoped.
2. Assign managed identity only to resources the agent needs for its job.
3. Use on-behalf-of access for SharePoint, Microsoft 365, and APIs where user permissions must be preserved.
4. Keep tool credentials in Foundry connections, managed identity, Key Vault, or API Management policy, not in prompts.
5. Test with a low-privilege user and a high-privilege user to confirm retrieval and actions differ correctly.
6. Log which identity was used for each sensitive tool call without logging tokens or secrets.

## Examples

**Example: identity selection**

Input: A support agent reads public product docs, private customer contracts in SharePoint, and opens internal tickets.

Output:

```text
Product docs: managed identity against Azure AI Search.
Customer contracts: on-behalf-of SharePoint grounding so user permissions apply.
Ticket creation: managed identity or app registration with scoped API permission, plus audit fields for invoking user.
```

**Example: bad binding**

```text
Avoid: one service principal with broad SharePoint access for all retrieval.
Prefer: OBO retrieval so the model never receives documents the user cannot open.
```

## Guidelines

1. Prefer credential-free SDK flows such as managed identity where the platform supports them.
2. Scope RBAC at the narrowest resource boundary that still supports the workflow.
3. Use OBO for user-private knowledge sources.
4. Treat tool outputs as permissioned context, not neutral text.
5. Never put secrets, tokens, or connection strings into agent instructions.

## Gotchas

1. **Service identity is not user identity**: A service credential can retrieve correct-looking data that violates user access semantics. Use OBO when the data source is user-private.
2. **RBAC scope creep is silent**: A managed identity assigned at broad scope can work in testing and become a production data exposure. Review effective permissions, not just role names.
3. **Cross-tenant assumptions break grounding**: Microsoft 365 and SharePoint grounding often depend on same-tenant identity flows. Validate tenant boundaries before designing the agent workflow.

## Integration

- foundry-tool-governance - Applies identity choices to Toolbox, MCP, OpenAPI, and Azure Functions tools.
- azure-agentic-retrieval - Applies per-user and workload access to knowledge sources.
- responsible-ai-guardrails - Combines access control with content safety and prompt-injection defenses.
- core tool-design - Keeps identity requirements visible in tool contracts.

## References

- Microsoft Foundry Agent Service: https://learn.microsoft.com/azure/foundry/agents/overview
- Tool best practices for Foundry Agent Service: https://learn.microsoft.com/azure/foundry/agents/concepts/tool-best-practice
- Managed identities for Azure resources: https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview
- SharePoint grounding tool: https://learn.microsoft.com/azure/foundry/agents/how-to/tools/sharepoint

---

## Skill Metadata

**Created**: 2026-05-24
**Last Updated**: 2026-05-24
**Author**: Agent Skills for Context Engineering Contributors
**Version**: azure-0.1.0

