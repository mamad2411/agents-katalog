---
name: research-topic
description: Find and synthesise what the vault already says about a topic using MCP vault tools. Use when the user asks "what do my notes say about X", "summarise my thinking on X", or any broad discovery question over the vault.
---

# research-topic

Answer discovery questions over the vault by chaining MCP tools, not by grepping files directly. The MCP tools use Obsidian's metadata cache, so they return structured results (frontmatter, tags, link graph) that raw reads can't.

## When to use

- "What do my notes say about X?"
- "Summarise my thinking on X."
- "Find all notes that discuss X and how they connect."
- Any question that needs both content retrieval *and* relational context.

## Do not use

- Single-file lookups (call `vault_context` directly).
- Write-side tasks (see `link-hygiene` or `reviewed-edit`).

## Tool chain

1. **`vault_search`** with the topic as query, `limit: 20`. This gives you the candidate set of relevant notes with a snippet per match.
2. **Rank by signal.** Prefer notes whose title matches the topic, then notes with matching tags or frontmatter. Pull tags/frontmatter with `vault_tags` (topic as tag) or `vault_properties` if the user's vault uses structured metadata.
3. **`vault_context`** on the 3–5 highest-signal hits. Each call returns content + frontmatter + tags + headings + outgoing links + backlinks in one shot. **Do not** call `vault_read`, `vault_frontmatter`, `vault_links`, `vault_backlinks` separately: `vault_context` subsumes them.
4. **`vault_graph_neighborhood`** at `depth: 1–2` on the single most-linked note from step 3 to find adjacent notes the search may have missed (e.g. notes that link to it but don't mention the keyword).
5. **Optional:** `vault_backlinks` on a key note if you need who cites it.

## Synthesis rules

- Cite note paths inline (e.g. `notes/foo.md`) so the user can jump to them.
- If hits disagree, surface the disagreement. Don't pick one without saying so.
- If the search returns nothing, do not fabricate. Say "no notes matched" and ask the user for adjacent terms: `vault_suggest_links` requires a starting `file` so it can't help here.

## Example

User: "What do I have on distributed systems consensus?"

```
1. vault_search(query="consensus", limit=20)
   → 7 hits, top: notes/raft.md, notes/paxos.md, notes/fl-impossibility.md
2. vault_context(path="notes/raft.md")  // most backlinks in the snippet
3. vault_context(path="notes/paxos.md")
4. vault_context(path="notes/fl-impossibility.md")
5. vault_graph_neighborhood(path="notes/raft.md", depth=2)
   → notes/replication.md, notes/byzantine.md (not in search hits)
6. vault_context(path="notes/replication.md")
```

Then synthesise: "Three primary notes cover consensus: Raft (notes/raft.md), Paxos (notes/paxos.md), and the FL impossibility result (notes/fl-impossibility.md). Your Raft note links out to replication and byzantine-fault-tolerance …"
