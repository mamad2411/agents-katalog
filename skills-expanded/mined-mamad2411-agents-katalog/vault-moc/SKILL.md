---
name: vault-moc
description: Generate a Map of Content (MOC) note that categorizes and wikilinks vault project folders by theme. Can create a full vault index or a focused MOC for a specific category (e.g., "skills", "agents", "browser automation"). Use when wanting to create a navigational index of vault content.
---

# Vault MOC

Generate a categorized Map of Content that organizes vault project folders into thematic groups with wikilinks.

## Workflow

1. **Determine scope.** Ask the user if they want:
   - **Full vault MOC** — indexes all ~312 project folders by category
   - **Focused MOC** — a specific theme (e.g., "all agent team projects", "browser automation", "skills and plugins")

2. **Get the folder list:**
   ```bash
   obsidian folders
   ```
   This returns all folder paths. Filter to root-level folders only (no `/` in path after vault root).

3. **For a focused MOC**, also search for relevant folders:
   ```bash
   obsidian search query="<theme keyword>" limit=30
   ```

4. **Categorize folders by prefix and keyword patterns:**

   | Category | Pattern |
   |----------|---------|
   | Agent Teams & Orchestration | `*agent_team*`, `*agent_swarm*`, `*parallel_agent*`, `*council*` |
   | Skills & Prompts | `*skill*`, `*prompt*`, `cc_skills*`, `*slash*` |
   | Browser Automation | `*browser*`, `*playwright*`, `*chrome*`, `*cdp*` |
   | MCP Servers | `*mcp*`, `*tool_search*` |
   | Loops & Scheduled Tasks | `*loop*`, `*scheduled*`, `*cron*` |
   | Obsidian Integration | `*obsidian*` |
   | Web Projects & Design | `*web*`, `*design*`, `*pencil*`, `*figma*` |
   | Research & Autoresearch | `autoresearch_*` |
   | Plugins & Extensions | `*plugin*`, `*extension*` |
   | Other / Misc | Everything else |

5. **Sample descriptions** for folders (read first 5 lines of README.md or gemini3_summary.txt):
   - For full MOC: sample the top 2-3 folders per category to write category descriptions
   - For focused MOC: read descriptions for all folders in scope

6. **Compose the MOC note** using the `Write` tool:

   ```markdown
   ---
   description: Map of Content — <scope>
   title: MOC — <Scope>
   date: YYYY-MM-DD
   source: vault-moc
   ---

   # MOC — <Scope>

   > Index of <n> project folders. Generated <date>.

   ## Stats
   - **Total folders:** <n>
   - **Categories:** <n>

   ## Category Name
   > Brief description of what's in this category.

   - [[folder_name/README|Display Name]] — one-line description
   - [[folder_name/gemini3_summary|Display Name]] — one-line description
   ...

   ## Another Category
   ...

   ## Uncategorized
   Folders that don't fit the above categories.
   - [[folder_name/README]]
   ...
   ```

7. **Write the file:**
   ```
   Write tool → <vault-root>/MOC — <Scope>.md
   ```
   Use `MOC — Vault Index.md` for a full vault MOC.

8. **Report** the categories created, folder count, and file path.

## Tips

- For the full vault MOC, don't try to read every folder's README — categorize by name pattern first, then sample a few per category for descriptions
- Use `[[folder/README|Friendly Name]]` display text to make the MOC readable (strip underscores, title-case the display name)
- `__IMPORTANT` folders deserve a dedicated **⭐ Highlights** section at the top
- A focused MOC (e.g., "Skills") is more immediately useful than a full vault index — suggest this for first use
