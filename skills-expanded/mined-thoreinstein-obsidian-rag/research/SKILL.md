---
name: research
description: >-
  Use when the user asks a question about their vault, wants to explore a topic
  across notes, or says "research", "find out", "what do I know about", or
  "summarize my notes on". Chains semantic search, note reading, and link
  traversal for deep vault research.
---

# Deep Vault Research

Research a topic across the user's Obsidian vault using a multi-pass approach.

## Workflow

1. **Semantic Discovery** — Call `obsidian_rag_query` with the user's question (limit 5-10). This surfaces the most relevant chunks across the vault.

2. **Targeted Reading** — For each high-relevance result, call `obsidian_read_note` to get the full context. Skim for the most pertinent sections.

3. **Link Traversal** — Check `obsidian_get_links` on the most relevant notes to find connected knowledge. Read promising linked notes.

4. **Synthesis** — Combine findings into a clear answer with citations:
   - Reference specific notes by name: `[[Note Name]]`
   - Quote relevant passages when helpful
   - Note any gaps or contradictions in the vault's knowledge

## Arguments

The user's query follows the skill invocation. Example: `/research what do I know about authentication patterns`

## Tips

- If RAG returns no results, suggest running `/index` first
- For broad topics, do multiple RAG queries with different phrasings
- Always cite which notes your answer draws from
