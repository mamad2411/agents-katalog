---
name: rag-pipelines-hybrid-search
description: "Combine BM25-style lexical search with dense embeddings and fuse results so both rare terms and paraphrases are found."
---
# Implement hybrid keyword + vector search

> Combine BM25-style lexical search with dense embeddings and fuse results so both rare terms and paraphrases are found.

**Track:** 🤖 AI Engineering · **Domain:** RAG Pipelines · **Level:** intermediate · **~35 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Combine BM25-style lexical search with dense embeddings and fuse results so both rare terms and paraphrases are found.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Stand up a lexical index (BM25) alongside your vector index on the same chunks
2. Embed queries with the same model and distance metric used at ingestion
3. Retrieve top-k from both indexes with k at least double your final context size
4. Fuse rankings with Reciprocal Rank Fusion (RRF), k=60 as default
5. Optionally rerank fused candidates with a cross-encoder on top-50
6. A/B against pure-vector on your golden questions; keep the winner per query class

## Common Pitfalls

- Mixing similarity metrics between ingestion and query time
- Fusing raw scores instead of ranks across incompatible scales

## Success Signals

- Hit-rate lift over best single retriever
- P95 retrieval latency under 300ms

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill rag-pipelines-hybrid-search
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill rag-pipelines-hybrid-search -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills