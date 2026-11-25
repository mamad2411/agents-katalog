---
name: vault-synthesize
description: Deep-search the vault on a topic, read the most relevant project files, and produce a synthesis note that consolidates knowledge with wikilinks. Use when wanting to understand what this vault knows about a topic, or to create a reference note from scattered project folders.
---

# Vault Synthesize

Research assistant for the vault's own content. Searches across project folders, reads the best sources, and synthesizes a consolidated note.

## Workflow

1. **Clarify the topic** if needed. Accept a topic, question, or keyword cluster. Example: "Claude Code agent teams", "browser automation workflows", "MCP server patterns".

2. **Run multiple searches** to cast a wide net — use 2-4 query variations:
   ```bash
   obsidian search:context query="<primary term>" limit=10
   obsidian search:context query="<synonym or related term>" limit=10
   obsidian search:context query="<specific aspect>" limit=8
   ```
   Collect all matching file paths. Deduplicate. Prefer matches in `gemini3_summary.txt` and `README.md` files over `transcript.txt`.

3. **Rank results** by relevance:
   - Matches in multiple queries = higher priority
   - `gemini3_summary.txt` > `README.md` > `transcript.txt`
   - Folders whose names match the topic = higher priority
   - Aim for the top 5-10 sources

4. **Read the top sources** using the `Read` tool:
   - For each top folder, read `gemini3_summary.txt` if it exists, else `README.md`
   - Skim `transcript.txt` only if neither summary nor README is available
   - Read up to 10 files total

5. **Synthesize a note.** Write to disk using the `Write` tool (content will be long):

   ```markdown
   ---
   description: Synthesis of vault knowledge on <topic>
   title: Synthesis — <Topic>
   date: YYYY-MM-DD
   source: vault-synthesize
   ---

   # Synthesis — <Topic>

   ## Overview
   2-3 paragraph synthesis of what this vault collectively knows about the topic. Write from the perspective of someone who has read all the sources.

   ## Key Insights
   1. **Insight title** — explanation. Source: [[folder_name/gemini3_summary]]
   2. **Insight title** — explanation. Source: [[folder_name/README]]
   ...

   ## Patterns & Approaches
   How different sources approach the topic — agreements, disagreements, different angles.

   ## Source Notes
   | Project | Description | Link |
   |---------|-------------|------|
   | folder_name | What this source covers | [[folder_name/gemini3_summary]] |
   ...

   ## Gaps
   What this vault does NOT cover well on this topic. What's missing or outdated.
   ```

6. **Write the file:**
   ```
   Write tool → <vault-root>/Synthesis — <Topic>.md
   ```

7. **Log to daily note:**
   ```bash
   obsidian daily:append content="### HH:MM — Synthesized: <Topic>\nCreated [[Synthesis — <Topic>]] from <n> vault sources.\n"
   ```

8. **Report** the note path, number of sources consulted, and the top 3 insights found.

## Tips

- Capitalize synthesis notes with " — " separator: `Synthesis — Agent Teams.md`
- If the vault has many sources (>15 relevant), narrow to the 8-10 most specific rather than trying to read all
- The `## Gaps` section is often the most valuable — note what the user should look for next
- If sources conflict, note it explicitly in `## Patterns & Approaches`
