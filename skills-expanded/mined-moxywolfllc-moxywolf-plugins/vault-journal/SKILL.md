---
name: vault-journal
description: Log a research entry to today's Obsidian daily note, automatically finding and wikilinking related vault projects. Use when the user wants to capture something they learned, worked on, or found interesting about Claude Code or AI tooling.
---

# Vault Journal

Log structured research entries to today's daily note. Automatically discovers related vault projects and wikilinks them.

## Workflow

1. **Get the user's entry content** — what they learned, worked on, or want to capture. Accept freeform text.

2. **Read today's daily note:**
   ```bash
   obsidian daily:read
   ```
   Note whether it exists and what sections are already present.

3. **If the daily note is empty or missing**, create an initial structure first:
   ```bash
   obsidian create path="YYYY-MM-DD.md" content="---\ndescription: Daily research log\ndate: YYYY-MM-DD\n---\n\n# YYYY-MM-DD\n\n## Research Log\n" silent
   ```
   Use today's actual date in YYYY-MM-DD format.

4. **Search for related vault projects** using keywords extracted from the user's entry:
   ```bash
   obsidian search query="<keywords>" limit=10
   ```
   Run 1-2 searches with different keyword combinations. Extract matching folder names from results.

5. **Compose the journal entry:**
   ```markdown
   ### HH:MM — Topic Title
   User's content here (cleaned up, concise).
   **Related:** [[folder_name/README]], [[another_folder/gemini3_summary]]
   ```
   - Use current time for HH:MM
   - Keep the entry focused — 1-4 sentences max
   - Only include related links if you found genuinely relevant folders (don't force it)
   - If a source URL was mentioned, add `**Source:** <url>`

6. **Append the entry:**
   ```bash
   obsidian daily:append content="### HH:MM — Topic Title\nContent here.\n**Related:** [[folder/README]]\n"
   ```

7. **Confirm** by reading back the daily note or reporting what was appended.

## Tips

- Extract 2-4 specific keywords from the user's entry for search (e.g., "agent teams parallel" not just "agents")
- Link to `gemini3_summary.txt` for content-summary folders, `README.md` for code project folders
- If the user says "log this conversation" or similar, summarize the current conversation's key insight as the entry
- Multiple entries in one session are fine — each gets its own `### HH:MM` block
