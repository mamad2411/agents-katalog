---
name: twilio-enterprise-knowledge
version: 1.0.0
description: Build and govern the RAG Knowledge base that grounds Twilio AI Assistants — ingest sources, chunk and embed, keep content fresh, enforce access control, and evaluate answer quality to prevent hallucination.
author: matrixx0070
tags: [twilio, knowledge, rag, embeddings, grounding]
capabilities: []
---

## When to use

Use this when you own the knowledge that grounds a Twilio AI Assistant: deciding what documents/URLs/DB exports to ingest, how they get chunked and embedded, how you keep them fresh and reindexed, how citations map back to sources, who is allowed to see what, and how you measure whether answers are correct and grounded rather than hallucinated.

**Not for:** designing the end-to-end support system (use twilio-customer-support-architect), moving live messages over Conversations (use twilio-conversations-classic-api), or persisting per-user conversation state (use twilio-conversation-memory).

## Method

1. Inventory sources. List candidate sources by type (documents/files, public URLs, plain text, exported DB/help-center content) and by sensitivity. Decision point: only ingest content you are licensed and cleared to surface to the assistant's audience.
2. Ingest into Knowledge. Attach each source under `https://assistants.twilio.com/v1/Knowledge`; Twilio chunks and embeds it into a vector index. Associate the Knowledge with an assistant via `/Assistants/{id}/Knowledge`. Decision point: one shared base vs per-audience bases when access rules differ (public FAQ vs internal runbooks).
3. Tune chunking for retrieval. Aim for semantically coherent chunks (roughly a few hundred tokens) so a retrieved chunk is self-contained enough to answer and cite. Over-large chunks dilute relevance; over-small chunks lose context.
4. Enforce grounding + citations. Configure the assistant to answer only from retrieved chunks and to return citations. Decision point: if top-k retrieval scores fall below a relevance threshold, the assistant should decline ("I don't have that") rather than free-generate.
5. Manage freshness. Track each source's `last_ingested`. Reindex on a cadence and on source change; remove or supersede stale documents so retired policies stop being cited. Decision point: event-driven reindex for fast-moving content, scheduled for stable content.
6. Enforce access control. Segregate sensitive knowledge into bases bound only to assistants serving authorized audiences. Never place internal-only content in a base that a public-facing assistant can retrieve.
7. Evaluate quality. Maintain a golden Q&A set; score answers for correctness, groundedness (every claim traces to a citation), and citation precision. Decision point: block a Knowledge update from shipping if eval regresses.
8. Close the loop. Route unanswered/low-confidence questions and low-CSAT topics back into ingestion as content gaps.

## Example

```python
import os, requests
AUTH = (os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
BASE = "https://assistants.twilio.com/v1"

# 1. Create a Knowledge source (chunked + embedded by Twilio)
kn = requests.post(f"{BASE}/Knowledge", auth=AUTH, data={
    "Name": "billing-faq",
    "Type": "web",                       # e.g. web URL, file, or text source
    "Source[url]": "https://help.example.com/billing",
    "Description": "Public billing FAQ",
}).json()
knowledge_id = kn["id"]

# 2. Attach it to an assistant so answers are grounded on it
requests.post(f"{BASE}/Assistants/{ASSISTANT_ID}/Knowledge/{knowledge_id}", auth=AUTH)

# 3. Freshness check — reindex sources whose upstream changed
for src in list_sources(knowledge_id):
    if upstream_changed(src) or stale(src["last_ingested"], days=7):
        requests.post(f"{BASE}/Knowledge/{knowledge_id}/Reindex", auth=AUTH)  # re-embed
```

## Pitfalls

- Ingesting internal-only docs into a public assistant's base leaks confidential content through retrieval. Segregate by audience.
- No freshness policy means retired prices/policies keep getting cited with confidence. Track `last_ingested` and reindex.
- Chunks that are too large drown the relevant passage; too small strip needed context. Tune for self-contained, citable chunks.
- Letting the assistant answer when retrieval scores are low is the main hallucination vector. Gate on a relevance threshold and decline otherwise.
- Shipping Knowledge changes with no eval set turns every edit into an unmeasured regression risk.
- Duplicated/near-duplicate documents split retrieval scores across copies and can surface the wrong version. Deduplicate before ingest.

## Output format

Return a Knowledge inventory as JSON: `[{ "knowledge_id", "name", "type", "source", "audience", "last_ingested", "chunk_count", "attached_assistants": [] }]`. For evaluations, return per-question `{ "q", "expected", "answer", "grounded": bool, "citations": [], "score" }` plus an aggregate correctness/groundedness summary.

## Reference

- Knowledge endpoints: `https://assistants.twilio.com/v1/Knowledge` (create/list/get/delete sources) and `https://assistants.twilio.com/v1/Assistants/{id}/Knowledge` (attach/detach a source to an assistant). Base API: `https://assistants.twilio.com/v1`. Auth: Basic (Account SID + Auth Token).
- Source types ingest documents/files, URLs, and raw text; Twilio chunks and embeds each source into a vector store used for retrieval at answer time.
- Grounding: the assistant retrieves top-k relevant chunks and answers with citations back to the originating source; configure it to decline when retrieval relevance is below threshold.
- Freshness: re-ingest/reindex on source change or on a schedule; remove superseded sources so they stop being retrieved.
- Access control: bind sensitive Knowledge only to assistants serving authorized audiences; keep public and internal bases separate.
- Evaluation: measure correctness, groundedness (claim→citation traceability), and citation precision against a golden set; gate Knowledge updates on no regression.
- Consumed by the deflection layer in twilio-customer-support-architect; live message transport is twilio-conversations-classic-api (`https://conversations.twilio.com/v1`).
