---
name: context-window-budget
description: Manage context window budget explicitly — prune stale content, compress retrieved data, never let context grow unbounded.
---

# Context window budget

Treat the context window as a **finite resource with diminishing marginal returns** — not something to fill. As the token count grows, the model's ability to accurately recall any individual fact from the window *decreases* ("context rot"). Every token spent on stale or redundant information is a token taken from the current task, and it also degrades recall of everything else.

## Rules

- Before appending retrieved content (tool results, file reads, search results), estimate its token cost relative to what's already in context.
- Prune messages or retrieved blocks that are no longer relevant to the current subtask before starting a new retrieval-heavy operation.
- Summarize long retrieved documents rather than appending verbatim. One dense paragraph beats five paragraphs of boilerplate.
- When the same fact appears in multiple sources (e.g. a README and a config file), cite one — the most authoritative — and discard the rest.
- Never re-read a file you already have in context unless you need to verify it changed.

## Two budget tactics for agent loops

- **Just-in-time retrieval.** Don't pre-stuff everything the agent *might* need. Hold lightweight identifiers (file paths, stored queries, links) and load the data into context at runtime via tools, only when a step actually needs it.
- **Compaction.** When a conversation nears the window limit, summarize it — preserving decisions, unresolved problems, and key implementation details, discarding redundant tool output — and reinitiate a fresh window from that summary rather than letting it run to the edge. (Structure the summary as a delta/append over named retention fields — `decisions`, `open_problems`, `implementation_details` — rather than a single end-to-end monolithic rewrite; a monolithic rewrite silently drops load-bearing context when the model misjudges what is "redundant".)

## Source

Anthropic, "Effective context engineering for AI agents," 2025-09 — <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>: context "must be treated as a finite resource with diminishing marginal returns"; recall decreases as tokens grow; the just-in-time and compaction tactics are defined there. The recall-degradation effect is independently corroborated across 18 frontier models by Chroma's "Context Rot" study (see [context-pollution-prevention](context-pollution-prevention.md)).

## Examples

```text
// BAD — reads entire 800-line file to find one function
read_file("src/utils/helpers.ts")

// GOOD — grep for the specific symbol, then read only the relevant section
grep("function formatDate", "src/utils/")
read_file("src/utils/date.ts", offset=42, limit=30)
```
