---
name: visionaire-knowledge
description: Inject relevant self-study knowledge into task context using BM25 search over Visionaire's knowledge base. Use before starting any creative, strategic, technical, or research task — brand work, Solana/Web3, content creation, prompt engineering, agent skills, or generative AI. Triggers on task starts and when phrases like "what do we know about", "recall knowledge", "check knowledge base", or "inject context" appear. Always run this before producing significant work so past study improves output quality.
---

# Visionaire Knowledge Injection

Before working on any significant task, search the knowledge base and inject relevant context.

## Steps

1. Derive a 3–7 word query from the task (e.g. "solana token mechanics", "brand strategy content", "prompt engineering techniques")
2. Run the search:
   ```
   node /data/.openclaw/skills/visionaire-knowledge/scripts/search-knowledge.mjs "<query>" --limit 5
   ```
3. Read the output — treat it as **## Relevant Context** for the task ahead
4. If results are thin or off-topic, try a second query with different terms

## Notes

- Knowledge base lives at `/data/.openclaw/workspace/memory/knowledge.json`
- Entries are scored by relevance + recency (30-day half-life decay — fresh study ranks higher)
- "(no relevant knowledge found)" is fine — just means the base hasn't studied that topic yet
- Don't inject stale or irrelevant results — use judgment on what's actually useful
