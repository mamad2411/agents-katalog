---
name: azure-memory-state
description: This skill should be used when implementing Microsoft-native agent memory and state: Cosmos DB, Blob or ADLS scratchpads, Azure Cache for Redis, session stores, episodic memory, entity state, vector memory, and append-only logs.
---

# Azure Memory and State

Agent memory is the durable state that survives the prompt. In Microsoft-native systems, memory should be split by retrieval shape, consistency need, identity boundary, and audit requirement instead of collapsing everything into a vector store.

## When to Activate

Activate this skill when:

- Choosing Azure storage for agent session state, long-term memory, scratchpads, or audit logs.
- Deciding between Cosmos DB, Blob Storage, ADLS Gen2, Azure Files, Azure Cache for Redis, or Azure AI Search.
- Persisting summaries, user preferences, entity records, tool outputs, or multi-agent handoffs.
- Designing append-only logs for evaluation, governance, or recovery.
- Separating working memory from long-term knowledge.

Do not activate this skill for adjacent work owned by other skills:

- Generic memory architecture independent of Azure services: core `memory-systems`.
- File-backed context patterns independent of Azure service choice: core `filesystem-context`.
- Retrieval over indexed documents: `azure-agentic-retrieval`.
- Identity and access control for state stores: `azure-identity-for-agents`.

## Core Concepts

Pick memory by access pattern:

| Memory type | Microsoft-native default |
| --- | --- |
| Working cache | Azure Cache for Redis |
| Session state | Cosmos DB or durable application store |
| Episodic records | Cosmos DB documents with timestamps and user scope |
| Semantic retrieval | Azure AI Search or Cosmos DB vector where appropriate |
| Scratchpads and large tool outputs | Blob Storage or ADLS Gen2 |
| Append-only audit logs | Append blobs or JSONL in controlled storage |
| Shared filesystem mount | Azure Files for hosted containers that need POSIX-like access |

The key design rule from the core memory skill still applies: start with the shallowest layer that satisfies retrieval quality and operational requirements.

## Practical Guidance

1. Classify state as working, session, episodic, semantic, artifact, or audit.
2. Store large tool outputs in Blob or ADLS and return references, not full text.
3. Use Cosmos DB when the agent needs low-latency entity state, session records, or globally distributed documents.
4. Use Azure AI Search for document retrieval and citation-oriented knowledge access.
5. Use append-only logs for decisions, rejected attempts, safety events, and evaluation records.
6. Put user and tenant scope in every durable memory record that can influence future responses.

## Examples

**Example: customer support agent memory**

```text
Session messages: Cosmos DB session container.
Customer facts: Cosmos DB entity records with freshness metadata.
Policy documents: Azure AI Search index.
Large diagnostic logs: Blob Storage with search-friendly filenames.
Audit trail: append blob JSONL with tool calls and release decisions.
```

**Example: context offloading**

```text
Tool returns a long trace.
Agent stores trace in Blob, writes a short summary to session state, and keeps only the Blob URI plus key excerpts in active context.
```

## Guidelines

1. Do not use one memory store for every memory type.
2. Include freshness, source, user scope, and deletion semantics in memory records.
3. Use references to durable artifacts to keep prompts small.
4. Prefer append-only logs for governance-sensitive events.
5. Test memory retrieval with stale, conflicting, and permission-mismatched records.

## Gotchas

1. **Vector memory is not state management**: Similarity search does not replace session consistency, entity updates, or audit logs.
2. **Summaries can become false memory**: Store source links and timestamps with compressed state so later agents can verify.
3. **Shared memory can leak context across users**: Partition by tenant, user, session, and data classification before retrieval.

## Integration

- core memory-systems - Owns the general memory architecture.
- core filesystem-context - Owns file-backed context and scratchpad patterns.
- azure-agentic-retrieval - Owns document and knowledge-source retrieval.
- azure-identity-for-agents - Owns state-store permissions and user scoping.

## References

- Cosmos DB for AI agents: https://learn.microsoft.com/azure/cosmos-db/ai-agents
- Azure AI Search RAG overview: https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview
- Azure Blob Storage: https://learn.microsoft.com/azure/storage/blobs/
- API Management semantic caching: https://learn.microsoft.com/azure/api-management/azure-openai-enable-semantic-caching

---

## Skill Metadata

**Created**: 2026-05-24
**Last Updated**: 2026-05-24
**Author**: Agent Skills for Context Engineering Contributors
**Version**: azure-0.1.0

