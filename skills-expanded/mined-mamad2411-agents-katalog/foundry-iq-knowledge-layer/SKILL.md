---
name: foundry-iq-knowledge-layer
description: This skill should be used when designing Microsoft Foundry IQ knowledge bases, reusable enterprise grounding, federated knowledge APIs, permission-aware retrieval, knowledge source governance, and shared context layers for agents.
---

# Foundry IQ Knowledge Layer

Foundry IQ is the Microsoft-native answer for reusable, governed enterprise knowledge. Use it when multiple agents need a shared, permission-aware knowledge layer instead of each agent owning separate RAG plumbing, indexes, source connectors, and retrieval policies.

## When to Activate

Activate this skill when:

- Designing Foundry IQ knowledge bases for agents or copilots.
- Reusing the same enterprise knowledge across multiple agents, apps, or workflows.
- Grounding agents over mixed sources such as SharePoint, OneLake, Azure data stores, web content, or customer-managed indexes.
- Preserving ACLs, sensitivity labels, tenant boundaries, and user permissions during grounding.
- Deciding whether to use Foundry IQ, Azure AI Search, SharePoint grounding, File Search, or Fabric Data Agent.
- Standardizing a knowledge API or knowledge-base catalog for an enterprise agent platform.

Do not activate this skill for adjacent work owned by other skills:

- Direct custom index design, chunking, scoring, and retrieval traces: `azure-agentic-retrieval`.
- Structured business metrics and semantic models: `fabric-data-agent`.
- Managed identities, OBO, RBAC, and tenant boundaries: `azure-identity-for-agents`.
- Tool catalog and action governance: `foundry-tool-governance`.

## Core Concepts

Knowledge bases are a product boundary, not just a prompt trick. The goal is to make enterprise knowledge reusable, governed, and consistent across agents while keeping the user's effective permissions intact.

Use Foundry IQ as the default when:

| Need | Why Foundry IQ fits |
| --- | --- |
| Shared knowledge across agents | One knowledge base can serve many agents and applications |
| Permission-aware grounding | Enterprise ACLs, labels, and tenant controls remain central |
| Mixed source estates | Federated and indexed sources can be presented through one knowledge API |
| Reduced RAG duplication | Teams avoid rebuilding ingestion, vectorization, query planning, and governance per agent |
| Enterprise control plane | Knowledge ownership, refresh, and reuse become platform concerns |

Foundry IQ complements lower-level retrieval. Azure AI Search remains the right choice when the team needs direct index control, custom ranking, enrichment pipelines, or domain-specific retrieval tuning.

## Practical Guidance

1. Define knowledge bases by durable business domain, not by single agent.
2. Treat each knowledge base as a governed product with owners, source lists, permission semantics, refresh expectations, and citation requirements.
3. Put reusable enterprise grounding in Foundry IQ before building per-agent RAG pipelines.
4. Use Azure AI Search behind or beside Foundry IQ when custom indexing and retrieval tuning are required.
5. Route analytical questions to Fabric Data Agent or Fabric semantic models when the answer requires computation over governed measures.
6. Keep identity decisions explicit: service identity for platform operations, OBO or user context for permissioned answers.
7. Evaluate retrieval quality, groundedness, permission filtering, and citation accuracy before promoting a knowledge base to production agents.

## Examples

**Example: enterprise support platform**

```text
Knowledge base: "Product Support"
Sources: SharePoint troubleshooting guides, public docs, known-issue database, escalation playbooks
Users: support agents, customer-facing copilots, engineering triage agents

Use Foundry IQ as the shared knowledge layer.
Use Azure AI Search only for the known-issue database if it needs custom indexing or ranking.
Use Entra OBO when the answer depends on the user's support role or customer assignment.
```

**Example: choosing the grounding path**

```text
One uploaded PDF for one agent: Foundry File Search.
Shared enterprise policy knowledge: Foundry IQ.
Custom document index with tuned scoring: Azure AI Search.
Power BI-aligned sales metrics: Fabric Data Agent.
Microsoft 365 documents with user permissions: SharePoint grounding or Foundry IQ, depending on availability and reuse needs.
```

## Guidelines

1. Prefer Foundry IQ for reusable enterprise knowledge bases.
2. Keep knowledge-base ownership separate from agent ownership.
3. Preserve permissions before optimizing relevance.
4. Require citations and source identifiers for answers grounded in enterprise knowledge.
5. Version and test knowledge-base changes before attaching them to production agents.
6. Document when a knowledge base federates sources versus indexes copied content.
7. Keep volatile product setup steps in deployment docs so the skill remains stable as Foundry IQ evolves.

## Gotchas

1. **Reusable does not mean universal**: Broad knowledge bases can leak intent and reduce relevance. Scope by business domain and permission boundary.
2. **Permissions are retrieval behavior**: If the user cannot access the source, the knowledge layer must not retrieve it for that user.
3. **Foundry IQ does not remove evaluation**: You still need groundedness, citation accuracy, freshness, and access-control tests.
4. **Product surfaces may move**: Foundry IQ is an evolving product surface. Verify current APIs, connector coverage, and preview status before hard-coding architecture.
5. **Fabric IQ and Foundry IQ are different layers**: Use Fabric for governed analytical semantics; use Foundry IQ for reusable enterprise knowledge grounding.

## Integration

- azure-agentic-retrieval - Provides lower-level Azure AI Search and retrieval-design patterns when Foundry IQ needs custom indexes or tuning.
- fabric-data-agent - Owns governed analytical answers and semantic-model grounding.
- azure-identity-for-agents - Owns OBO, managed identity, RBAC, and tenant-boundary design.
- responsible-ai-guardrails - Evaluates groundedness, prompt injection risks, and policy adherence.
- core memory-systems - Owns the generic retrieval and memory architecture.
- core context-optimization - Owns context selection, compression, and token budget tradeoffs.

## References

- Foundry IQ overview and announcements: https://aka.ms/iq-series
- Microsoft Foundry overview: https://learn.microsoft.com/azure/ai-foundry/what-is-azure-ai-foundry
- Azure AI Search RAG overview: https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview
- SharePoint grounding for Foundry agents: https://learn.microsoft.com/azure/foundry/agents/how-to/tools/sharepoint
- Microsoft Fabric documentation: https://learn.microsoft.com/fabric/

---

## Skill Metadata

**Created**: 2026-05-24
**Last Updated**: 2026-05-24
**Author**: Agent Skills for Context Engineering Contributors
**Version**: azure-0.1.0

