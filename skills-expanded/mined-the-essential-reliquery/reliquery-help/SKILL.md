---
name: reliquery-help
description: "Use this skill whenever the user asks about the Reliquery system, its tools, how to set it up, or needs help navigating the plugin. Trigger when the user says \"how does reliquery work\", \"what tools do I have\", \"help me set up mempalace\", \"how do I install this\", \"reliquery help\", \"what can the palace do\", \"list the MCP tools\", \"how do I use chronicle/memorize/forget\", or any question about Reliquery's capabilities, architecture, or configuration. Also trigger when a new user is onboarding for the first time, or when someone needs a refresher. This is the front door — when in doubt, trigger and route from here."
---

## Identity

Reliquery Help is the orientation guide for the entire system. It answers three questions: *What do I have?*, *How does it work?*, and *How do I set it up?* It performs no write operations — it reads, explains, and guides. Think of it as the help menu for the plugin.

Three modes — identify which the user needs:

- **Overview mode**: What Reliquery is and how the pieces fit together
- **Tool reference mode**: What MCP tools are available and what each does
- **Setup mode**: Installation, configuration, or troubleshooting

If unclear, start with a brief overview and ask what to dive into.

---

## Overview — What Is Reliquery?

Reliquery is a context management and memory system for AI-assisted worldbuilding, co-writing, and roleplaying. It solves LLM statelessness: maintaining persistent, accurate lore across sessions without dumping an entire knowledge base into every prompt.

The name is a portmanteau of **Relic** + **Query** — querying the sacred artifacts of your creative vault.

### Two Layers

**The Vault** — a folder of structured markdown files called **relics**, one per entity (character, location, faction, system, etc.), each with YAML frontmatter and `[[wiki-link]]` cross-references. The vault is the source of truth for all authored content. Reliquery creates and manages the vault folder structure itself — no special software required. The vault is just a folder of `.md` files.

**Obsidian is optional but recommended.** Obsidian is a free markdown editor that sits on top of the vault folder like a specialized file explorer with quality-of-life features: graph view to visualize entity connections, wiki-link navigation between relics, and plugin support (Dataview for queryable tables, Templater for relic scaffolding). Think of it as a secondary UI layer — it adds organization, editing, and visualization tools, but the vault works without it. You can use VS Code, Notepad, Google Drive, or any tool that edits markdown files.

**The Palace (MemPalace)** — a local-first AI memory system built on ChromaDB (vector search) and SQLite (knowledge graph). It stores verbatim chunks of vault content as searchable **drawers**, organized into a spatial hierarchy: Wings → Rooms → Drawers. The palace is how Claude remembers your vault between sessions.

### Five Skills

- **Chronicle** — intake pipeline. Raw content (manuscripts, transcripts, brain dumps) → structured relics in the vault. Handles extraction, staging, review, backup, and commit.
- **Memorize** — memory pipeline. Committed relics → searchable palace drawers. Handles chunking, duplicate detection, existing drawer updates, verification, and KG relationship offers.
- **Cartograph** — relational mapping. Relic relationships → structured knowledge graph triples. Handles survey, triple design, execution, and verification.
- **Forget** — deletion pipeline. Removes palace entries (and optionally vault files in Erase mode), with KG cleanup offers for orphaned triples.
- **Study** — the orchestrator. Chains chronicle → memorize → cartograph in a single pipeline, calling forget as needed. The default when the user's intent is "make the system learn this."

### How Recall Works

Claude doesn't keyword-match against a lorebook. It formulates contextual questions — "what is Sera's relationship with the Iron Council?" — and the palace's semantic search returns relevant verbatim fragments from across multiple relics. Claude reconstructs coherent context from those fragments, pulling exactly the slices needed for the current scene. Reconstructive recall, not archival retrieval.

The knowledge graph adds a temporal layer. Every fact has a validity window (`valid_from` / `valid_to`), tracking what was true *when*. Characters who shift allegiances or gain titles are tracked with precision. Past states remain queryable for flashbacks or historical reference.

---

## Tool Reference — MCP Tools

MemPalace exposes 29 tools across 5 categories.

### Read & Discovery

| Tool | Purpose |
|------|---------|
| `mempalace_status` | Palace overview: drawer counts, wing/room structure. Also injects the behavioral protocol. **Call first, every session.** |
| `mempalace_list_wings` | Lists all wings with drawer counts |
| `mempalace_list_rooms` | Lists rooms within a wing |
| `mempalace_get_taxonomy` | Full wing → room → drawer count tree |
| `mempalace_search` | Semantic search — returns verbatim drawer content with similarity scores. Filterable by wing/room. **The primary retrieval tool.** |
| `mempalace_check_duplicate` | Checks if content already exists before filing |
| `mempalace_get_aaak_spec` | Returns the AAAK compression dialect spec |

### Write

| Tool | Purpose |
|------|---------|
| `mempalace_add_drawer` | Files verbatim content. Auto-dedup at ~0.9 similarity. |
| `mempalace_update_drawer` | Updates existing drawer content and/or metadata |
| `mempalace_delete_drawer` | Deletes a drawer by ID. Irreversible. |
| `mempalace_get_drawer` | Fetches a single drawer by ID (full content + metadata) |
| `mempalace_list_drawers` | Lists drawers with pagination. Optional wing/room filter. |

### Knowledge Graph

| Tool | Purpose |
|------|---------|
| `mempalace_kg_query` | Query entity relationships with time/direction filtering |
| `mempalace_kg_add` | Add a fact triple with `valid_from` date |
| `mempalace_kg_invalidate` | Mark a fact as no longer true (soft delete, history preserved) |
| `mempalace_kg_timeline` | Temporal history of an entity's relationships |
| `mempalace_kg_stats` | KG statistics |

### Navigation

| Tool | Purpose |
|------|---------|
| `mempalace_traverse` | Walk the palace graph, exploring room/wing connections |
| `mempalace_find_tunnels` | Discover cross-wing connections |
| `mempalace_create_tunnel` | Create a cross-wing link |
| `mempalace_list_tunnels` | List existing tunnels |
| `mempalace_delete_tunnel` | Remove a tunnel |
| `mempalace_follow_tunnels` | Traverse through tunnel connections |
| `mempalace_graph_stats` | Structural statistics |

### Diary & System

| Tool | Purpose |
|------|---------|
| `mempalace_diary_write` | Timestamped diary entries for cross-session self-awareness |
| `mempalace_diary_read` | Read past diary entries |
| `mempalace_hook_settings` | Configure auto-save hook behavior |
| `mempalace_memories_filed_away` | Check if a recent checkpoint saved |
| `mempalace_reconnect` | Force reconnect to the palace database |

### The Memory Protocol

Every session follows this sequence:

1. `mempalace_status` — load palace layout and behavioral protocol
2. Identify all entities in the user's message
3. Dual lookup per entity: `mempalace_search` (prose context) + `mempalace_kg_query` (structured state)
4. Reconcile — KG wins on current state; prose wins on voice and detail
5. Incorporate naturally — never reference the lookups in your response
6. When the story changes entity state, note changes in a `<!-- CHANGELOG -->` block
7. At session end, `mempalace_diary_write` to record what happened

---

## Setup — Installation & Configuration

### Prerequisites

- Python 3.9+
- Claude Code or Claude Desktop (for MCP integration)
- ~300 MB disk for the default embedding model

### Option A — Claude Code Plugin (Recommended)

The fastest path. Two commands from your terminal:

```
claude plugin marketplace add MemPalace/mempalace
claude plugin install --scope user mempalace
```

This installs the MCP server, skills, and configuration in one step. Once installed, Claude Code can run palace commands directly.

### Option B — Manual MCP Setup (Claude Desktop or Claude Code)

If you prefer manual configuration or are using Claude Desktop:

**1. Install the package:**

```
pip install mempalace
```

**2a. Claude Code — register the MCP server:**

```
claude mcp add mempalace -- python -m mempalace.mcp_server
```

**2b. Claude Desktop — edit the config file:**

Edit `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "mempalace": {
      "command": "python",
      "args": ["-m", "mempalace.mcp_server"]
    }
  }
}
```

Restart Claude Desktop completely (exit from system tray, then relaunch).

### Initialize the Vault

Point `mempalace init` at the folder where your relics live (or will live):

```
mempalace init [your-vault-directory]
```

The **directory name becomes your wing name** in the palace. If you run `mempalace init ~/vaults/Ironhold`, your wing is `Ironhold`. Choose the name deliberately — it scopes all future searches and prevents cross-project contamination.

Creates `~/.mempalace/` with config files and ChromaDB storage.

### Mine Your Vault

Mine each content folder separately for clean room detection:

```
mempalace mine "path/to/Vault/World/Characters" --wing [your-wing]
mempalace mine "path/to/Vault/World/Factions" --wing [your-wing]
mempalace mine "path/to/Vault/World/Locations" --wing [your-wing]
```

Repeat for each content folder (History, Magic, Tech, Arcs, Sessions, etc.).

**Do not mine** `.obsidian/`, `Templates/`, or the vault root directly — plugin configs and empty scaffolding pollute search results.

### Verify

Ask Claude to call `mempalace_status`. You should see your wing and drawer counts. Test a search:

```
mempalace_search(query="[any entity from your vault]", wing="[your-wing]")
```

If results return relic content, you're live.

### Install Skills

Place each skill's `SKILL.md` in its own subfolder under your skills directory. The folder name becomes the skill's invocation name. If you used the Claude Code plugin install (Option A), skills are included automatically.

### Troubleshooting

| Symptom | Fix |
|---------|-----|
| "Palace not found" / empty status | Run `mempalace init` again |
| 0 drawers after mining | Verify you mined content folders, not the vault root |
| Claude can't reach palace | Check MCP config and fully restart Claude (system tray exit for Desktop) |
| Irrelevant search results | You may have mined `.obsidian/` — see the clean re-mining procedure in the MemPalace docs |
| Changes not showing up | Full restart required (system tray exit for Desktop, not just window close) |
| KG queries return nothing | Mining populates drawers, not KG triples. Add KG entries via `mempalace_kg_add` during narrative sessions. |

---

## Quick Reference

| I want to... | Use |
|---|---|
| Start a session | `mempalace_status` |
| Recall lore about an entity | `mempalace_search` + `mempalace_kg_query` |
| Process raw content into relics | `/chronicle` |
| Index relics into the palace | `/memorize` |
| Map entity relationships into the KG | `/cartograph` |
| Remove entries from the palace | `/forget` |
| Remove entries AND delete vault files | `/forget` (Erase mode — must be explicitly requested) |
| Full pipeline: content → relics → memory → KG | `/study` |
| Study a conversation or attached file | `/study` |
| Check what's indexed vs. what's on disk | `/memorize` (Audit mode) |
| Track how an entity changed over time | `mempalace_kg_timeline` |
| Record a new fact | `mempalace_kg_add` |
| Mark a fact as no longer true | `mempalace_kg_invalidate` |
| Find connections across projects | `mempalace_find_tunnels` |
| Get the full palace structure | `mempalace_get_taxonomy` |
| Get help | `/reliquery-help` |
