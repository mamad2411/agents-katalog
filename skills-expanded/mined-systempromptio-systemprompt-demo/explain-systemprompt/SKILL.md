---
name: "explain-systemprompt"
description: "Explain what systemprompt.io is by reading the official docs live through the systemprompt MCP hub (list_topics then get_topic)"
---

# Explain systemprompt.io

Explain what systemprompt.io is and why it exists, sourcing every claim from the
**live documentation hub** rather than memory. The hub is served by the
`systemprompt` MCP server and is open to every signed-in user.

## When to Use

Use this when someone asks "what is systemprompt.io?", "what does this do?", or
wants a grounded introduction. Always read the docs through the MCP tools so the
answer reflects the deployment you are actually connected to.

## How to Use

1. **List the topics.** Call the hub to see everything available:

   ```
   mcp__systemprompt__list_topics {}
   ```

2. **Read the introduction.** Fetch the overview topic in full:

   ```
   mcp__systemprompt__get_topic {"topic_id": "what-is-systemprompt"}
   ```

3. **Go one level deeper** where it matters for the question. Good follow-ups:

   ```
   mcp__systemprompt__get_topic {"topic_id": "architecture"}
   mcp__systemprompt__get_topic {"topic_id": "getting-started"}
   ```

   If the question is not covered by a topic you can name, search instead, then
   read the best hits in full before answering:

   ```
   mcp__systemprompt__search_docs {"query": "<the user's own words>"}
   ```

4. **Answer from what you read.** Summarise systemprompt.io as an open
   governance gateway for AI agents — a library you embed and extend that
   governs, audits, and meters every inference and tool call. Quote the topics'
   own framing (governance spine, compile-time extensions, per-user cost
   tracking) rather than inventing detail, and cite the topic id behind each
   claim so a reader can check it.

If a question cannot be answered from the hub, say so plainly rather than
filling the gap from memory. The point of this skill is that the answer is
traceable to a document this deployment actually serves.

## What the user is watching

Every call above is a real governed tool call: it suspends on the governance
gate, surfaces an approval card, and lands an audited row. The demonstration is
as much *that the reads were governed* as it is the content of the answer.

## Related

- `demonstrate_governance` — the four-stage pipeline, with two stages proven live.
- `analyse_governance_stats` — what those calls cost, and how each was judged.
