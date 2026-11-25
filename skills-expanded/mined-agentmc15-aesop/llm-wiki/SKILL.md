---
name: llm-wiki
description: Incrementally compile messy source documents into a persistent, cross-linked Markdown knowledge base instead of re-reading raw docs every time. Use when the user has a pile of documents/notes/tickets and wants durable understanding, a project wiki, an onboarding doc, or asks "summarize everything we know about X" across many sources.
---
# llm-wiki

Karpathy's LLM-knowledge-base pattern. Classic RAG answers each question from raw documents every
time; this instead *compiles* sources into a living wiki — summaries, entity pages, concept pages,
contradictions, cross-links, and an evolving synthesis. No classical program could maintain that
over messy human docs; an LLM can. It's synthetic-data-generation over fixed data, and each new
projection of the information yields insight.

## Steps
1. Ingest sources (docs, tickets, threads) into a staging area.
2. For each source, extract: key facts, entities, concepts, and any contradictions with what's
   already in the wiki.
3. Write/update Markdown pages: one per entity and per concept, cross-linked. Append to a change log.
4. When sources conflict, record the conflict explicitly rather than silently picking one.
5. Re-run as new sources arrive; the wiki is append-and-revise, persisted on disk.

## Notes
- The point is **understanding**, not just retrieval — you (the human) stay the director, and the
  wiki is a tool that enhances your understanding so you can direct well.
- Pairs with the agentic-RAG harness in `evals/` when you need to *measure* retrieval quality.
