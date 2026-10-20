---
name: agent-publishing
description: This skill should be used when publishing Microsoft-native agents: Foundry agent versions, stable endpoints, Teams and Microsoft 365 Copilot distribution, Entra Agent Registry, environment promotion, rollout, and rollback.
---

# Agent Publishing

Publishing turns an agent from a development artifact into a managed product surface. In Microsoft-native systems, publishing must preserve versioning, identity, permissions, evaluation evidence, monitoring, and rollback.

## When to Activate

Activate this skill when:

- Promoting a Foundry agent from playground or development into a stable endpoint.
- Publishing an agent to Teams, Microsoft 365 Copilot, or another Microsoft channel.
- Designing version promotion, rollback, and release gates.
- Registering agents for enterprise discovery and governance.
- Separating development, test, and production agent configurations.

Do not activate this skill for adjacent work owned by other skills:

- Hosted runtime architecture before publishing: `foundry-hosted-agents`.
- Human approval, PR, and locked evaluator design: core `harness-engineering`.
- Identity and tenant access: `azure-identity-for-agents`.
- Tool catalog versioning before the agent release: `foundry-tool-governance`.

## Core Concepts

Publishing is a governance boundary. The published agent should be a versioned, monitored, permissioned endpoint whose behavior can be traced back to instructions, model selection, tools, evaluations, and release approval.

Separate three surfaces:

| Surface | Purpose |
| --- | --- |
| Development | Fast iteration in Foundry playground, local framework, or hosted agent code |
| Staging | Evaluation, red teaming, identity testing, and channel-specific validation |
| Production | Stable endpoint, monitored distribution, rollback plan |

## Practical Guidance

1. Freeze instructions, model deployment, tool versions, and identity configuration before evaluation.
2. Run deterministic and Foundry evaluations against representative prompts.
3. Confirm tool traces and user-permission behavior in the target channel.
4. Publish a stable endpoint or channel integration only after approval.
5. Monitor quality, safety, latency, token use, and tool failures after release.
6. Keep rollback simple: previous agent version, previous toolbox version, and previous model deployment should remain available.

## Examples

**Example: internal Teams agent**

```text
Dev: prompt agent in Foundry playground.
Staging: same tools, staging Search index, test users with different permissions.
Production: published to Teams with monitored endpoint and rollback to prior version.
```

**Example: release artifact**

```text
Release record:
- Agent version
- Model deployment
- Toolbox version
- Retrieval sources
- Evaluation result link
- Approver
- Rollback target
```

## Guidelines

1. Publish versions, not mutable experiments.
2. Validate in the channel where users will invoke the agent.
3. Treat tool and retrieval configuration as part of the release.
4. Keep production monitoring attached from day one.
5. Require human approval for broad enterprise distribution.

## Gotchas

1. **The channel changes behavior**: Teams or Microsoft 365 Copilot distribution can alter identity, file access, and user expectations. Test in-channel.
2. **Tool drift breaks reproducibility**: If a toolbox changes after publishing, the agent version is not the whole release artifact.
3. **Discovery is governance**: Registering an agent broadly without clear ownership creates support and compliance ambiguity.

## Integration

- foundry-hosted-agents - Owns Microsoft-native runtime architecture.
- core hosted-agents - Owns platform-agnostic runtime architecture.
- core harness-engineering - Owns approval, rollback, and locked evaluation surfaces.
- azure-identity-for-agents - Owns production identity and permission boundaries.
- responsible-ai-guardrails - Owns safety gates and production monitoring signals.

## References

- Foundry Agent Service overview: https://learn.microsoft.com/azure/foundry/agents/overview
- Publish agents to Microsoft 365 Copilot and Teams: https://learn.microsoft.com/azure/foundry/agents/how-to/publish-copilot
- Microsoft Foundry evaluations: https://learn.microsoft.com/azure/ai-foundry/concepts/evaluation-approach-gen-ai
- Microsoft 365 Copilot agent builder: https://learn.microsoft.com/microsoft-365-copilot/extensibility/copilot-studio-agent-builder

---

## Skill Metadata

**Created**: 2026-05-24
**Last Updated**: 2026-05-24
**Author**: Agent Skills for Context Engineering Contributors
**Version**: azure-0.1.0
