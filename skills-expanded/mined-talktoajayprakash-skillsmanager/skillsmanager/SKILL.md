---
name: skillsmanager
description: Discover, install, add, and update agent skills from local or remote storage using the sm CLI
---

# Skills Manager

Skills Manager is a CLI tool for managing agent skills stored locally or in remote storage (Google Drive, GitHub). Use it to find, install, share, and update skills. Works offline by default — no setup needed for local use.

## Prerequisites

- Local storage works out of the box — no setup needed.
- For Google Drive: a human must run `sm setup google` once to configure credentials.
- For GitHub: requires the `gh` CLI to be installed and authenticated (`gh auth login`). No additional sm setup needed.
- All commands except `setup google` are non-interactive and designed for agent use.

## Commands

### Find and install a skill

```bash
# Search by name or description (BM25 ranked — partial/reordered terms work)
sm search <query>

# Download and install for this agent
sm install <name> --agent <agent>

# Install to current project only (instead of global)
sm install <name> --agent <agent> --scope project

# Remove a skill's symlink (cache and storage untouched)
sm uninstall <name> --agent <agent>
sm uninstall <name> --agent <agent> --scope project

# List all available skills across all collections
sm list
```

Supported agents: `claude`, `codex`, `agents`, `cursor`, `windsurf`, `copilot`, `gemini`, `roo`, `openclaw`, `antigravity`

### Share a skill you own

```bash
# Upload a local skill directory to a collection
# The directory must contain a SKILL.md with name and description in YAML frontmatter
sm add <path>

# Upload to a specific collection
sm add <path> --collection <name>
```

### Register a skill path without uploading files (cross-repo / curated collections)

Use `--remote-path` when the skill files already exist in a remote backend and you just want to register a pointer to them. You cannot `add` local files to a cross-backend collection — you must use this flag instead.

```bash
# Register a skill entry by path — no file upload
sm add --remote-path <backend-path> --name <skill-name> --description "<description>" --collection <name>

# Example: register a skill that lives in a GitHub repo
sm add --remote-path skills/write-tests/ --name write-tests --description "Generate unit tests" --collection my-col
```

### Update a skill

```bash
# Push local edits back to storage
# The skill must have been fetched on this machine first
sm update <path>

# If the skill exists in multiple collections, specify which one
sm update <path> --collection <name>
```

After updating, the local cache is refreshed so all symlinks on this machine reflect the change immediately.

### Delete a skill

```bash
# Delete a skill from its collection (removes from backend, cache, and index)
sm skill delete <name>

# If the skill exists in multiple collections, specify which one
sm skill delete <name> --collection <collection-name>
```

### Registry and collection management

```bash
# Create a local registry (auto-created on first use)
sm registry create

# Create a registry in Google Drive
sm registry create --backend gdrive

# Create a registry in a GitHub repo (creates repo if it doesn't exist)
sm registry create --backend github --repo <owner/repo>

# Show all registries and their collection references
sm registry list

# Search a backend for registries owned by the current user
sm registry discover --backend gdrive
sm registry discover --backend github

# Add a collection reference to the registry
sm registry add-collection <name>

# Push local registry and collections to Google Drive (safe to re-run — skips already-synced collections)
sm registry push --backend gdrive

# Push local registry and collections to GitHub (safe to re-run — skips already-synced collections)
sm registry push --backend github --repo <owner/repo>

# Remove a collection reference from the registry (keeps data)
sm registry remove-collection <name>

# Remove and permanently delete the collection and all its skills
sm registry remove-collection <name> --delete

# Create a new collection (local by default)
sm collection create [name]

# Create a collection in a GitHub repo (skills stored in that repo)
sm collection create [name] --backend github --repo <owner/repo>

# Create a collection in Google Drive
sm collection create [name] --backend gdrive

# Create a collection whose skills live in a specific GitHub repo (cross-backend)
sm collection create [name] --backend gdrive --skills-repo <owner/repo>
sm collection create [name] --backend github --repo <owner/registry-repo> --skills-repo <owner/skills-repo>

# Re-discover collections from storage
sm refresh
```

### Install the sm skill for agents

```bash
# Install to all agent directories
sm install

# Install to specific agents
sm install --agent claude,codex

# Install to a custom path
sm install --path <dir>

# Remove from all agents
sm uninstall

# Remove from a specific agent
sm uninstall --agent claude
```

## Cross-backend collections (curated skill libraries)

A collection can declare that its skill files live in a different GitHub repo than the collection YAML. This is indicated by `type: github` in `SKILLS_COLLECTION.yaml`.

**When you encounter a cross-backend collection:**
- `sm add <local-path> --collection <name>` → **will fail** with an error like `skills source type is "github"`. This is expected — you cannot upload local files to a foreign repo.
- **Do this instead:** `sm add --remote-path <path-in-repo> --name <n> --description "<d>" --collection <name>`
- `sm install <skill> --agent claude` → **works normally** — files are automatically pulled from the declared GitHub repo

**How to identify a cross-backend collection:**
- `sm registry list` — collections with a `--skills-repo` are shown with their skills repo
- Reading the `SKILLS_COLLECTION.yaml` directly — look for `type: github` + `metadata.repo`

**Quick rule:**
- Own the skill files? → `sm add <path>`
- Files already in a GitHub repo? → `sm add --remote-path <path> --name <n> --description "<d>"`

---

## Common Workflows

**User asks to find a skill:**
1. `sm search <relevant terms>`
2. `sm install <skill-name> --agent claude`

**User asks to share a skill they created locally:**
1. Ensure the skill directory has a `SKILL.md` with `name` and `description` in YAML frontmatter
2. `sm add <path-to-skill-directory>`
3. Install the skill to make it immediately available to the agent:
   - For all projects: `sm install <skill-name> --agent claude`
   - For current project only: `sm install <skill-name> --agent claude --scope project`

**User asks to update a skill:**
1. Edit the skill files locally
2. `sm update <path-to-skill-directory>`

**User asks to install a skill for this project only:**
1. `sm install <name> --agent claude --scope project`

**User wants to back up local skills to Google Drive:**
1. `sm setup google` (one-time, human-only)
2. `sm registry push --backend gdrive`

**User wants to store skills in a GitHub repo:**
1. `sm collection create <name> --backend github --repo <owner/repo>` — creates the GitHub repo if needed, and auto-registers the collection
2. `sm add <path> --collection <name>` — upload the skill into that collection

**User wants to create a curated collection of skills from a public GitHub repo (cross-backend):**

Use this when you want to expose skills from an external GitHub repo (e.g. `anthropics/skills`) via a collection the user can install from, without copying the files.

1. `sm collection create <name> --backend gdrive --skills-repo <owner/skills-repo>`
   - This creates the collection YAML in the user's Google Drive with `type: github` + `metadata.repo` pointing to the skills repo
2. Register each skill by its path in the skills repo (no file upload needed):
   ```bash
   sm add --remote-path skills/write-tests/ --name write-tests --description "Generate unit tests" --collection <name>
   ```
3. Users install skills normally — `sm install write-tests --agent claude` — and the files are pulled from the skills repo

**User wants to add a skill from a public GitHub repo without uploading files:**
1. Create or identify a collection with `--skills-repo <owner/repo>`
2. `sm add --remote-path <path-in-repo> --name <skill-name> --description "<desc>" --collection <name>`

**User wants to discover GitHub-hosted collections:**
1. `sm registry discover --backend github`

**User wants to see what registries and collections exist:**
1. `sm registry list`

**User asks to delete/remove a single skill:**
1. `sm skill delete <skill-name>`
2. If the skill lives in multiple collections, add `--collection <name>` to target the right one

**User wants to remove a collection:**
1. `sm registry remove-collection <name>` (removes reference only, data is kept)
2. `sm registry remove-collection <name> --delete` (permanently deletes collection and skills)

## Collection types

Most collections store skill files directly in their backend. But a collection can also declare that skill files live in a different GitHub repo — this is useful for curating public skills or pointing to a shared library repo.

| Collection backend | Skills repo | What `add` does | What `install` does |
|---|---|---|---|
| `gdrive` or `local` | (none) | Uploads files to Drive/local | Downloads from Drive/local |
| `github` | (same repo as collection) | Commits files to the repo | Clones/pulls from repo |
| `gdrive` or `local` | `--skills-repo owner/repo` | **Requires `--remote-path`** — registers a path pointer only | Downloads files from the GitHub repo |
| `github` (registry repo) | `--skills-repo owner/skills-repo` | **Requires `--remote-path`** — registers a path pointer only | Downloads files from the skills repo |

When you try to `sm add <local-path>` to a collection with a cross-backend skills repo, the command will fail with a clear error pointing you to `--remote-path`.

The `install` column above refers to `sm install <name> --agent <agent>`.

## Architecture

- **Registry** (`SKILLS_REGISTRY.yaml`): root index pointing to all collections across backends
- **Collection** (`SKILLS_COLLECTION.yaml`): folder of skills with an index file
- **Backends**: `local` (default, `~/.skillsmanager/`), `gdrive` (Google Drive), and `github` (GitHub repo via `gh` CLI)
- **Cache**: skills are cached at `~/.skillsmanager/cache/<uuid>/` and symlinked to agent directories
- **Symlinks**: all agents share one cached copy — updating the cache updates all agents
- **RoutingBackend**: transparent middleware that intercepts skill-file operations and dispatches to the right backend based on the collection's declared `type` field

## Scope

- `--scope global` (default): installs to `~/.agent/skills/` — available across all projects
- `--scope project`: installs to `./.agent/skills/` in the current working directory — this project only
