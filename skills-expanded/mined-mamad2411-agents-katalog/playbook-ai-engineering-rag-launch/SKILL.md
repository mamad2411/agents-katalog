---
name: playbook-ai-engineering-rag-launch
description: "Take retrieval-augmented answers from empty repo to evaluated production feature."
---
# Playbook: Launch a RAG feature end to end

> Take retrieval-augmented answers from empty repo to evaluated production feature.

**Track:** 🗺️ AI Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~135 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Take retrieval-augmented answers from empty repo to evaluated production feature.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Design a chunking strategy for retrieval: start with "Profile source documents: length distribution, headings, tables, code blocks"
2. Step 2 — Implement hybrid keyword + vector search: start with "Stand up a lexical index (BM25) alongside your vector index on the same chunks"
3. Step 3 — Evaluate RAG answer quality automatically: start with "Freeze 30-100 test questions with known-good source passages"
4. Step 4 — Budget LLM latency end to end: start with "Trace one real request through every hop and record percentile timings"
5. How it fits together: Sequence matters: chunking decisions gate retrieval quality; evals gate launch. Do not skip golden-set creation even under deadline.

### Referenced Skills

- `rag-pipelines-chunking-strategy`
- `rag-pipelines-hybrid-search`
- `rag-pipelines-eval-rag-quality`
- `inference-mlops-latency-budgeting`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill rag-pipelines-chunking-strategy && npx skills add aniruddhaadak80/skills --skill rag-pipelines-hybrid-search && npx skills add aniruddhaadak80/skills --skill rag-pipelines-eval-rag-quality && npx skills add aniruddhaadak80/skills --skill inference-mlops-latency-budgeting
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills