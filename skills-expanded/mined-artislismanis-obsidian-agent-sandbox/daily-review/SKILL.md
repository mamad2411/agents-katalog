---
name: daily-review
description: Summarise what the user worked on in a recent time window (today, this week, last N days). Use when the user asks "what did I work on", "summarise my week", "recap my recent notes", or wants a digest of recent activity.
---

# daily-review

Produce a concise digest of recent vault activity. Optimise for the user's attention. This is a skim, not a dump.

## When to use

- "What did I work on today/this week?"
- "Summarise my recent notes."
- "What's been changing in my vault lately?"
- "Recap the last 7 days."

## Do not use

- Full-vault summaries (that's a research task; see `research-topic`).
- Finding notes by topic (use `vault_search` or `research-topic`).

## Tool chain

1. **`vault_recent`** with `limit: 30` and (optionally) a folder filter for the user's journal or work area. This returns files sorted by modification time with ISO timestamps.
2. **Group by day.** Parse the timestamps and bucket notes by date. Skip auto-touched files (e.g. index notes that get rewritten on every save) if you can detect them.
3. **Filter by window.** Default to "today" if the user didn't specify; otherwise use their stated window (e.g. "this week" = last 7 days).
4. **`vault_context`** on the top 3–5 most-recently-modified notes in the window. This gives content + frontmatter + headings in one call. Don't call it on every note; that's a dump, not a digest.
5. **Optional: `vault_graph_neighborhood`** depth 1 on the single most-linked note to find adjacent threads.

## Synthesis

Output a short digest. Typical structure:

```
## Recent activity (last 7 days)

**Monday 2026-04-13**: 3 notes
- notes/research/consensus.md: started exploring Raft vs Paxos
- journal/2026-04-13.md: daily log

**Wednesday 2026-04-15**: 5 notes
- projects/obsidian-agent-sandbox/roadmap.md: planned Phase 4H
- notes/research/consensus.md: added failure-mode comparison
- …

### Threads
- **Consensus research** continues across three notes (raft.md, paxos.md, fl-impossibility.md). The common thread is failure modes.
- **Plugin roadmap** was the main Wednesday focus.
```

## Rules

- **Cite paths** so the user can click through.
- **Group when it helps, flatten when it doesn't.** For "today" with 4 notes, a flat list is fine. For "this week" with 30 notes, daily buckets + thread summary is better.
- **Don't restate content.** The user already wrote it. Say what's *new* or *changing*, not what the notes contain.
- If the window is empty ("no notes modified in the last 24h"), say so and stop. Don't pad.
- Exclude tmp/scratch paths the user explicitly asks you to ignore.

## Example

```
User: "What did I work on this morning?"

1. vault_recent(limit=30)
   → filter to today's mtimes (5 notes)
2. vault_context for the 3 most-recently-edited:
     - projects/plugin/mcp-tools.ts
     - notes/research/consensus.md
     - journal/2026-04-19.md
3. Write digest:

This morning (2026-04-19):
- **Plugin work**: overhauled the MCP write-handler scaffolding in
  projects/plugin/mcp-tools.ts; the new runWrite helper consolidates
  review + apply + success across 8 tools.
- **Research**: added a note on FL-impossibility edge cases in
  notes/research/consensus.md.
- **Journal**: journal/2026-04-19.md captured the morning standup.

Nothing else touched today.
```
