---
name: agent-memory
description: Guide and workflow reference for agent-memory-mcp v3.3 — per-project SQLite + FTS5 architectural memory, centralized global knowledge graph, two-tier dead-end taxonomy, multi-folder workspace policies & cross-folder guardrails, zero-process git/remote identity, token budgeting middleware, and legacy .ag-memory.json JIT migration.
---

# Agent Memory (`agent-memory-mcp` v3.3)

`agent-memory-mcp` provides persistent, ACID-safe, full-text searchable memory for AI coding agents. Backed by Node 22.5+/24+ native `node:sqlite` (`WAL` + `FTS5`), it features per-project databases, zero-process git/worktree identity and remote URI support, prompt-first multi-folder workspace policies, cross-folder write guardrails, a centralized global knowledge graph, a two-tier anti-loop dead-end registry, and token budgeting middleware.

## Storage Architecture
- **Per-Project Live Stores:** `~/.ag-memory-mcp/stores/<project-slug>-<hash>.db` (keeps repository trees 100% clean — zero dotfiles written in user repos).
- **v4 Workspace & Identity Registry:** `~/.ag-memory-mcp/stores/projects_index.json` (lock-protected store aliases, 4-tier monotonic `gitIdentity`, and `(primary, secondary)` `workspacePolicies`).
- **Central Global Knowledge Graph:** `~/.ag-memory-mcp/global.db` (cross-project patterns, library quirks, and token audit logs).
- **Configuration:** `~/.ag-memory-mcp/config.json` (or `AG_MEMORY_MAX_RESPONSE_TOKENS` environment variable).
- **Zero-Loss JIT Migration:** Automatically detects, verifies, and archives legacy `<project_path>/.ag-memory.json` (`v2.0`) to `~/.ag-memory-mcp/backups/` (skipped safely on remote URIs).

## Tool Quick Reference (16 Tools)

### Project-Scoped & Workspace Tools (1–10, 16)
| Tool | Mode | Best Used For |
| :--- | :--- | :--- |
| `check_memory_status` | Read-only | 1-shot check returning initialization state, architecture TOC, dead-end count, and top 5 timeline logs. Accepts optional `git_remote` for remote URI binding. |
| `get_session_timeline` | Read-only | Chronological feed filterable by `category` (`session`, `architecture`, `decision`, `note`, `all`), `tag`, and `since`. |
| `save_project_memory` | Write/Upsert | Single or atomic batch (`entries: [...]`) save; auto-upserts matching `id` or `slug`. Accepts optional `git_remote`, `allow_external_files`, and `force_isolate`. |
| `search_project_memory` | Read-only | Weighted `FTS5` BM25 search across `title`, `tags`, `files`, and `summary` (plus matching dead-ends) with snippets. |
| `read_memory_node` | Read-only | Reads single `id` or batch `ids: [...]` (supports slugs like `"tech-stack"` or `"g-..."` global IDs), checking local & `@<slug>/` `files[]` disk `mtime` for staleness (skipped on remote URIs). |
| `update_memory_node` | Write | Partial update to `title`, `summary`, `tags`, `category`, or `files` with automatic revision backup. Accepts optional `allow_external_files`. |
| `delete_memory_node` | Write | Soft-archives obsolete memories (`hard_delete: false` default) or permanently deletes (`hard_delete: true`). |
| `record_dead_end` | Write | Logs `{ error_pattern, attempted_solution, root_cause, files, kind, constraints }` (`error_loop` vs `architectural`). Accepts optional `allow_external_files`. |
| `check_dead_ends` | Read-only | Searches recorded dead-ends by error message, keyword, or `file_path` (normalizing linked folder paths to `@<slug>/...`), filterable by `kind`. |
| `get_file_memories` | Read-only | Returns all memories and dead-ends anchored to `file_paths: [...]` (including `@<slug>/...` linked-folder anchors) before refactoring. |
| `configure_workspace` | Write | Actions: `set_folder_policy` (`independent` / `linked` / `ignored`), `link_project_identity` (`source_project_path`, `target_store_key`, `git_remote`, `isolate`), and `inspect`. |

### Global Knowledge & Taxonomy Tools (11–15)
| Tool | Mode | Best Used For |
| :--- | :--- | :--- |
| `save_global_knowledge` | Write | Saves cross-project patterns or library quirks to `global.db` (auto-generates `g-` prefixed IDs). |
| `search_global_knowledge` | Read-only | BM25 ranked FTS5 search across global patterns, filterable by `tech_stack` and `category`. |
| `promote_to_global` | Write | Promotes a validated project-specific memory node into the machine-wide global knowledge graph. |
| `reopen_dead_end` | Write | Reopens a past dead-end when external constraints, library updates, or requirements change. |
| `get_token_metrics` | Read-only | Retrieves machine-wide token efficiency statistics and audit logs from `global.db`. |

## Multi-Folder Workspace Policies & Guardrails (Prompt-First)

1. **Secondary Folder Policies (`[AGENT-MEMORY MULTI-FOLDER ACTION REQUIRED]`):**
   - When `SessionStart` detects uninitialized, unconfigured secondary folders, **ask the user** before bootstrapping or saving:
     - `independent`: separate project store for that folder.
     - `linked`: shared inside the primary store with `@<folderSlug>/` file anchors. **Always pass the primary workspace's `project_path`** when reading or saving memories for a linked folder.
     - `ignored`: reference-only in this multi-folder workspace (never suppresses standalone opening of that folder).
   - Persist via `configure_workspace`:
     ```json
     {
       "action": "set_folder_policy",
       "primary_path": "C:/Projects/PrimaryApp",
       "folder_path": "C:/Projects/CompanionLib",
       "mode": "linked",
       "folder_slug": "companion-lib"
     }
     ```
   - If `SessionStart` emits `[AGENT-MEMORY LINKED-ORDER NOTICE]`, route memory calls using the primary owner's `project_path`.
   - Up to 4 initialized secondary folders auto-hydrate at startup; overflow folders appear as on-demand.

2. **Cross-Folder Write Guardrail:**
   - `save_project_memory` (validated atomically across all `entries[]`), `update_memory_node`, and `record_dead_end` reject external file references (`isError: true`) unless the folder is `linked` or `allow_external_files: true` is passed.
   - Always **ask the user** whether to save to the owning folder's `project_path`, retry with `allow_external_files: true`, or save to both before overriding.

## Remote Workspaces, Git Identity & Clone Disambiguation

- **Supported Remote URIs:** `vscode-remote://`, `ssh://`, `wsl://`, `devcontainer://`, `remote://`, and Windows WSL UNC paths (`\\wsl.localhost\...`, `\\wsl$\...` — canonicalized to `wsl://` without triggering `wsl.exe`).
- **`[AGENT-MEMORY REMOTE WORKSPACE]` (Rule 2 Exception):** If `SessionStart` flags an uninitialized remote URI, inspect its git origin remote URL (if it is a git repo) and re-run `check_memory_status(project_path, { git_remote })` or `configure_workspace(action: "link_project_identity", project_path, git_remote)` before bootstrapping.
- **`[AGENT-MEMORY CLONE DISAMBIGUATION REQUIRED]`:** Simultaneous live clones sharing a remote `gitIdentity` block accidental writes until the user decides whether to isolate (`configure_workspace(action: "link_project_identity", project_path, isolate: true)` or `force_isolate: true` on `save_project_memory`) or share (`target_store_key`).
- **`[CONFLICT]`:** Surfaced by `check_memory_status` and `configure_workspace(action: "inspect")` if another store already owns the detected `gitIdentity`; ask the user before relinking.

## Canonical Bootstrap Pattern (Single Atomic Call)

When initializing a new project workspace, save all 3 core architectural nodes in **one** atomic transaction:

```json
{
  "project_path": "C:/Projects/MyApp",
  "entries": [
    {
      "slug": "tech-stack",
      "title": "Tech Stack & Ecosystem",
      "category": "architecture",
      "tags": ["architecture", "stack"],
      "summary": "..."
    },
    {
      "slug": "project-structure",
      "title": "Project Structure & Architecture",
      "category": "architecture",
      "tags": ["architecture", "structure"],
      "files": ["src/index.ts"],
      "summary": "..."
    },
    {
      "slug": "build-run",
      "title": "Build & Run Instructions",
      "category": "architecture",
      "tags": ["architecture", "build"],
      "files": ["package.json"],
      "summary": "..."
    }
  ]
}
```
