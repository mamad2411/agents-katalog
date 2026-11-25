---
name: azure-agentic-retrieval
description: This skill should be used when implementing private grounded retrieval on Azure: Azure AI Search, agentic retrieval, knowledge sources, File Search, SharePoint grounding, citations, access-controlled indexes, and retrieval traces.
---

# Azure Agentic Retrieval

Agentic retrieval is the Microsoft-native path for giving agents private, high-signal context without stuffing entire corpora into prompts. Use Foundry IQ when the agent needs a reusable managed enterprise knowledge layer; use Azure AI Search and Foundry retrieval tools when the implementation needs direct index control, custom pipelines, or lower-level retrieval tuning.

## When to Activate

Activate this skill when:

- Building RAG or grounded agents on Azure AI Search.
- Deciding between File Search, Azure AI Search, SharePoint grounding, Fabric Data Agent, or custom retrieval.
- Designing knowledge sources, indexes, chunks, citations, and retrieval traces.
- Preserving document permissions while grounding responses.
- Comparing simple vector search with hybrid, semantic, or agentic retrieval.

Do not activate this skill for adjacent work owned by other skills:

- Generic memory architecture and retrieval-shape decisions: core `memory-systems`.
- Token budgeting, masking, and context partitioning independent of Azure Search: core `context-optimization`.
- Identity and OBO design for retrieval: `azure-identity-for-agents`.
- Reusable Foundry IQ knowledge bases and enterprise knowledge APIs: `foundry-iq-knowledge-layer`.
- Structured data in Fabric semantic models or lakehouses: `fabric-data-agent`.

## Core Concepts

Retrieval is a context filter. The objective is not to retrieve the most text; it is to retrieve the smallest set of permission-valid evidence that can answer the question with citations.

Use the shallowest Azure retrieval path that satisfies the data shape:

| Data shape | Default |
| --- | --- |
| Uploaded documents for one agent | Foundry File Search |
| Reusable managed enterprise knowledge base | Foundry IQ |
| Enterprise search index | Azure AI Search |
| Microsoft 365 documents with user permissions | SharePoint grounding |
| Analytical data and semantic models | Fabric Data Agent |
| Mixed private sources with custom pipeline | Azure AI Search knowledge sources and custom indexing |

## Practical Guidance

1. Start with the user's answer contract: citation requirements, freshness, permission semantics, and latency tolerance.
2. Choose the retrieval surface based on data ownership and access control before choosing chunking.
3. Use hybrid retrieval when exact terms and semantic meaning both matter.
4. Keep chunks evidence-sized, with stable source identifiers and citation metadata.
5. Return retrieval activity in traces so failures can be debugged without replaying the whole conversation.
6. Evaluate groundedness, relevance, and citation accuracy separately.

## Examples

**Example: internal policy assistant**

```text
Private HR policies in SharePoint: use SharePoint grounding with OBO.
Published product docs in Blob: index into Azure AI Search.
Final answer: cite both sources separately and do not merge permission domains.
```

**Example: retrieval escalation**

```text
Start: File Search for a small uploaded corpus.
Scale: Azure AI Search when multiple agents share the corpus or need custom indexing.
Escalate: agentic retrieval when query planning over multiple knowledge sources improves answer quality.
```

## Guidelines

1. Design retrieval around evidence and permissions before model prompts.
2. Prefer private grounding sources over public web grounding for regulated workloads.
3. Store source IDs, timestamps, and access scope with every retrieved chunk.
4. Evaluate retrieval separately from generation.
5. Surface "not enough evidence" as a valid answer.

## Gotchas

1. **Search relevance is not answer groundedness**: A high-ranked chunk can still be misused. Evaluate the generated answer against retrieved evidence.
2. **Permission filters are part of retrieval quality**: A result the user cannot access is a retrieval failure, even if semantically relevant.
3. **Public web grounding changes the compliance story**: Prefer Azure AI Search, SharePoint, Fabric, or customer-controlled sources when data boundaries matter.

## Integration

- core memory-systems - Owns the generic memory and retrieval architecture.
- core context-optimization - Owns token efficiency and selective context loading.
- foundry-iq-knowledge-layer - Owns reusable managed enterprise knowledge bases.
- azure-identity-for-agents - Owns access semantics for private sources.
- responsible-ai-guardrails - Evaluates groundedness and injection risks.

## References

- Azure AI Search RAG overview: https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview
- Foundry IQ overview and announcements: https://aka.ms/iq-series
- Foundry File Search: https://learn.microsoft.com/azure/foundry/agents/how-to/tools/file-search
- SharePoint grounding: https://learn.microsoft.com/azure/foundry/agents/how-to/tools/sharepoint
- Foundry evaluations: https://learn.microsoft.com/azure/ai-foundry/concepts/evaluation-approach-gen-ai

---

## Skill Metadata

**Created**: 2026-05-24
**Last Updated**: 2026-05-24
**Author**: Agent Skills for Context Engineering Contributors
**Version**: azure-0.1.0
