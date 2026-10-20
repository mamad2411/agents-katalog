---
name: rag-pipelines-chunking-strategy
description: "Choose chunk sizes, overlaps, and structure-aware splits so retrieved context actually helps the model answer."
---
# Design a chunking strategy for retrieval

> Choose chunk sizes, overlaps, and structure-aware splits so retrieved context actually helps the model answer.

**Track:** 🤖 AI Engineering · **Domain:** RAG Pipelines · **Level:** foundation · **~25 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Choose chunk sizes, overlaps, and structure-aware splits so retrieved context actually helps the model answer.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Profile source documents: length distribution, headings, tables, code blocks
2. Pick structural splitter first (headings/paragraphs) over fixed character cuts
3. Set chunk size from your model's effective context budget minus prompt overhead
4. Add 10-20% overlap so facts spanning boundaries survive retrieval
5. Attach metadata per chunk: source title, section path, date, permissions
6. Build 20 golden questions and measure retrieval hit-rate before scaling up

## Common Pitfalls

- Fixed-size chunks that slice tables and lists into meaningless fragments
- Chunks larger than half the context window, starving the actual answer space
- No overlap, causing answers that cite half a sentence cut at a boundary

## Success Signals

- Recall@5 above 85% on golden set
- Median chunks-per-answer under 6

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill rag-pipelines-chunking-strategy
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill rag-pipelines-chunking-strategy -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills