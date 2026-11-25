---
name: connect
description: "Discover hidden relationships between ideas in Obsidian vaults. Find how two topics bridge, trace an idea's evolution, or surface recurring themes. Use when the user senses connections but can't articulate them, or wants to find patterns in their notes."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
  pack: cognitive-toolkit
---

# Connect Pack — "I sense these relate but can't see how"

Tools for finding relationships, patterns, and evolution of ideas across your vault.

## Commands

### /connect — Find how two ideas bridge

When the user invokes `/connect <topicA> <topicB>`:

1. Search for notes related to each topic:
   - `obs search content "<topicA>" --json`
   - `obs search content "<topicB>" --json`
2. Try direct graph path between related notes:
   - `obs links path "<noteA>" "<noteB>"` for the most relevant notes
3. If a direct path exists, explain each hop — read each note in the chain and summarize why it connects them
4. If no direct path exists:
   - Find notes that mention both topics: `obs search content "<topicA>" --json`, then check those results for topicB
   - Look for shared tags: `obs tags all --json` and find tags used by both topic clusters
   - Check for shared backlinks
5. Present the connection:
   - The bridge notes or shared concepts
   - A narrative explanation of how A connects to B through the user's own thinking
   - Suggest creating a new "bridge note" that makes this connection explicit

### /trace — Track an idea's evolution over time

When the user invokes `/trace <topic>`:

1. Find all notes mentioning the topic:
   - `obs search content "<topic>" --json`
   - `obs search path "<topic>" --json`
2. For each match, get the file modification date and read a summary:
   - Sort by date (oldest first)
3. Check backlinks and outgoing links for each note to find the thread
4. Present a timeline:
   ```
   ## Evolution of "<topic>"

   ### First appearance — YYYY-MM-DD
   [file]: [what you said then]

   ### Development — YYYY-MM-DD
   [file]: [how the idea evolved]

   ### Current state — YYYY-MM-DD
   [file]: [where you are now]

   ## Trajectory
   [Summary of how thinking shifted]

   ## Open questions
   [Unresolved threads in the evolution]
   ```
5. Use `obs files list --since 1y --sort modified --json` to ensure you're capturing the full timeline

### /drift — Surface what you're circling around

When the user invokes `/drift`:

1. Gather recent activity:
   - `obs files list --since 2w --sort modified --json` — recent files
   - `obs tags all --json` — tag distribution
2. Read the recent files and analyze:
   - What topics come up repeatedly?
   - What tags cluster together?
   - What wikilinks appear across multiple recent notes?
3. Look for patterns:
   - `obs search content "<recurring term>" --json` to see depth
   - `obs links orphans --json` — are orphan notes related to the pattern?
4. Present findings:
   ```
   ## What you've been circling

   ### Theme 1: [name]
   Appeared in: [list of notes]
   Related tags: [tags]
   [Brief description of the pattern]

   ### Theme 2: [name]
   ...

   ## Hidden connections
   [Themes that seem unrelated but share notes/tags]

   ## Suggestion
   [What might be worth writing about or exploring next]
   ```

## Tips

- Always use actual vault data. Never fabricate connections.
- When reading notes for summaries, focus on the first few paragraphs — they usually contain the thesis.
- The user's wikilinks are intentional connections. Treat them as strong signals.
- For /drift, 2 weeks is the default window. The user can say "/drift last month" and you should use `--since 4w`.
