---
name: agents-md-hierarchy
description: "Maintain hierarchical AGENTS.md frameworks (DOX-style) across a project portfolio — framework injection, child doc creation, tree initialization, system-wide discovery."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents-md, dox, hierarchy, documentation, project-context, ai-agent-instructions]
    triggers: [agents-md, dox, agent-context, AGENTS.md, initialize-dox, dox-tree, system-wide-search]
    related_skills: [project-documentation-standards, writing-plans]
---

# AGENTS.md Hierarchy Management

## When to Use

When the user asks you to:
- Add DOX (or any hierarchical framework) to existing AGENTS.md files
- "Initialize DOX tree for this project now"
- Find every AGENTS.md file across the filesystem
- Create child AGENTS.md files for subdirectory boundaries
- Populate or update a Child DOX Index in a root AGENTS.md
- "Enhance my entire system" with AGENTS.md structure

## Overview

DOX (from [github.com/agent0ai/dox](https://github.com/agent0ai/dox)) is a lightweight AGENTS.md framework that creates a hierarchy of project-context files. The core idea:

- **Root AGENTS.md** contains the DOX framework instructions + project-wide rules + Child DOX Index
- **Child AGENTS.md** files live in subdirectory boundaries (durable subsystems) with local rules
- **Before editing**, agents walk the tree from root to target path, reading every AGENTS.md along the route
- **After editing**, agents update the affected docs

The DOX framework is just Markdown — no install, no deps, no runtime.

## Workflow

### Phase 0: System-Wide Discovery

Before you can add DOX to AGENTS.md files, you need to find every one. **Your standard search tools may miss hidden directories (`~/.codex/`, `~/.hermes/`) AND entire secondary drives.**

#### Multi-Drive Scanning

the operator's repos span **both C: and E: drives**. Always search all drives:

```bash
# C: drive — primary projects, configs, home-dir repos
find /c/Users/USER -maxdepth 8 -name "AGENTS.md" \
  -not -path "*/node_modules/*" \
  -not -path "*/go/pkg/mod/*" \
  -not -path "*/venv/*" \
  -not -path "*/.venv/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/.git/*" \
  -not -path "*/.bun/*" \
  -not -path "*/Temp/*" \
  -not -path "*/pytest-*/*" \
  2>/dev/null | sort

# E: drive — agent-fleet, agent-universe, osint-framework, 50+ repos
find ${MY_REPOS} -name "AGENTS.md" \
  -not -path "*/node_modules/*" -not -path "*/.git/*" \
  -not -path "*/.opencode/*" -not -path "*n8n/data*" \
  -not -path "*_templates*" 2>/dev/null | sort
```

**CRITICAL** — Directory traversal depth:
- `maxdepth 5` misses AppData subdirectories 7+ levels deep
- Use `maxdepth 8` or higher for nested project trees on C:
- `maxdepth 3` is fine for E: drive repos (shallower structure)
- Always check hidden dirs: `~/.codex/`, `~/.hermes/`, `~/.config/`

**Separate targeted searches** by known project zone:
```bash
# Hermes config & profiles (AppData — deep paths)
find ~/AppData/Local/hermes -name "AGENTS.md" | sort
# Cloned repos on C:
find ~/Documents/github -name "AGENTS.md" | sort
# Home-directory repos
find ~ -maxdepth 1 -name "AGENTS.md"
# Cloned repos on E:
find ${MY_REPOS} -name "AGENTS.md" | sort
# Hidden config
find ~/.codex -name "AGENTS.md" 2>/dev/null
```

**When `find` on E: returns 0 files but you see them with `ls`**: The MSYS shell shows `/e/...` but Python's `os.path.isdir` returns `False` for that path. Use native Windows paths in Python: `E:\\yourdata\\Documents\\github`.

**Exclude these automatically** (dependencies, not user projects):
- `*/node_modules/*` — npm packages
- `*/go/pkg/mod/*` — Go modules
- `*/.bun/*` — Bun cache
- `*/Temp/*`, `*/pytest-*/*` — Test artifacts
- `*/.git/*`, `*/.opencode/*` — Git internals / auto-gen skills
- `*n8n/data*` — Data files, not project code
- `*_templates*` — Template files (copied, not edited)

**Categorize each result**:
- **User project repo** → Full DOX: framework + child docs + index
- **Agent definition / fleet profile** → DOX after YAML frontmatter + child doc shape
- **Config directory** (`~/.codex/`) → Add DOX to root, note leaf (no children)
- **Dependency** → skip (`node_modules/`, `go/pkg/mod/`, `.bun/`, Pub cache)

### Phase 1: Add DOX Framework to Root AGENTS.md

For each user-project AGENTS.md, **prepend** the DOX framework content. The framework block is:

```markdown
# DOX framework

- DOX is a highly performant AGENTS.md hierarchy installed here
- Agent must follow DOX instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

Do not rely on memory. Re-read the applicable DOX chain in the current session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately. Small edits that do not change behavior or contracts may leave docs unchanged, but the DOX pass still must happen.

## Hierarchy

- Root AGENTS.md is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- Child AGENTS.md files own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

## Child Doc Shape

- Create a child AGENTS.md when a folder becomes a durable boundary with its own purpose, rules, responsibilities, workflow, materials, or quality standards
- Work Guidance must reflect the current standards of the project or user instructions; if there are no specific standards or instructions yet, leave it empty
- Verification must reflect an existing check; if no verification framework exists yet, leave it empty and update it when one exists

Default section order:
- Purpose
- Ownership
- Local Contracts
- Work Guidance
- Verification
- Child DOX Index

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history
- Trim obvious statements, repeated rules, misplaced detail, and warnings for risks that no longer exist

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant
6. Report any docs intentionally left unchanged and why

## User Preferences

When the user requests a durable behavior change, record it here or in the relevant child AGENTS.md

## Child DOX Index

Leave this placeholder — it gets replaced during Phase 3 with the actual tree.
```

**How to prepend:** Use `patch` mode='replace' targeting the first non-fence line of the existing file. Include enough unique context (the first heading or first paragraph) in both `old_string` and `new_string` so the match is unambiguous. The `new_string` should be: DOX block + `---` separator + original first line.

### Phase 2: Scan Project for Durable Boundaries

Identify subdirectories that warrant their own child AGENTS.md. Look for folders that are:

- **Their own subsystem** — distinct purpose, rules, or tech stack (e.g., `gateway/`, `plugins/`, `tools/`)
- **Have their own workflow** — build commands, test patterns, conventions that differ from the root
- **Separate tech stack** — e.g. TypeScript React UI in a Python project
- **Owned by a different team/agent profile**

**Do NOT create child docs for:**
- `__pycache__/`, `node_modules/`, `venv/` — build artifacts
- Simple directories with no distinct rules — wait until they need documentation
- Single-file or single-responsibility folders — keep those rules in the parent

**For each durable boundary**, create a child AGENTS.md following the DOX child doc shape:

```markdown
## Purpose

One clear sentence about what this subsystem owns.

## Ownership

- `file1.py` — what it does
- `file2.rs` — what it does
- `dir/` — what lives here

## Local Contracts

Bullet-list rules specific to this subsystem:
- Build commands
- Naming conventions
- Tech stack constraints
- Required environment variables

## Work Guidance

How to work effectively in this subsystem.

## Verification

Concrete commands to verify changes:
- `cargo test -p foo` — unit tests
- `npm run lint` — lint

## Child DOX Index

No child AGENTS.md files in this subtree.
```

### Phase 3: Populate Child DOX Index in Root

Replace the "This project is not yet indexed" placeholder in each root AGENTS.md with a markdown table:

```markdown
## Child DOX Index

| Path | Scope |
|------|-------|
| `gateway/` | 🌐 Messaging gateway — platform adapters, session lifecycle, delivery |
| `plugins/` | 🔌 Plugin system — provider backends, lifecycle hooks |
| `tools/` | 🛠️ Tool registry and built-in implementations |
| ... | ... |
```

Use emoji prefixes for visual scanability (🌐 gateway, 🔌 plugins, 🛠️ tools, 🖥️ UI, 🐍 Python SDK, 🦀 Rust workspace, etc.). Sort alphabetically by path.

For **leaf directories** (no subdirectories that warrant children), add:
```
No child AGENTS.md files in this subtree.
```

For **config-only profiles** (like chief-of-staff), use:
```
This profile owns its own scope — no child AGENTS.md files in this subtree.
```

### Phase 4: Initialize Full DOX Tree

After DOX framework is added and child docs exist, tell the agents to initialize the tree. This means they'll scan the project structure and validate/replace the placeholders. The incantation:

> Initialize DOX tree for this project now.

This makes the agent walk the entire tree, identify every durable boundary, create any missing child docs, and update the Child DOX Index with the actual structure.

### Batch Processing At Scale (for 20+ files)

When adding DOX to 20+ AGENTS.md files across multiple repos, use a Python batch script with `os.walk` rather than editing files one by one. This is especially necessary for repos like agent-universe (71 files) or osint-framework (22 files).

**Key decisions:**
- Use `os.walk` with native Windows paths (`E:\\...`) — subprocess `find` may fail due to MSYS path translation
- The script must handle YAML frontmatter: detect `---` at content start, inject DOX after the closing `---`
- For roots with no frontmatter: prepend DOX + `---\n` separator
- Skip files that already have DOX (check for `# DOX framework`)
- Use the same DOX_BLOCK for all roots AND children in large-scale agent-definition repos

**Essential Windows path note:** `os.path.isdir('/e/path')` returns `False` on Python for Windows. Convert to `E:\\path` format before calling `os.walk`.

**Script skeleton:**
```python
DOX_BLOCK = """# DOX framework ..."""  # full framework block

def add_dox(filepath):
    with open(filepath, 'r', errors='replace') as f:
        content = f.read()
    if '# DOX framework' in content:
        return False  # already has DOX
    stripped = content.lstrip('\\ufeff').lstrip()
    if stripped.startswith('---'):  # has YAML frontmatter
        end_idx = stripped[3:].find('\\n---')
        if end_idx != -1:
            # Inject DOX after closing ---
            pos = end_idx + 5
            new = stripped[:pos] + '\\n' + DOX_BLOCK + '\\n' + stripped[pos:].lstrip()
            # write new
            return True
    # No frontmatter: prepend
    new = DOX_BLOCK + '\\n---\\n\\n' + content
    # write new
    return True

for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in {'node_modules','.git','__pycache__'}]
    if 'AGENTS.md' in filenames:
        add_dox(os.path.join(dirpath, 'AGENTS.md'))
```

The script should be disposable (created in /tmp and deleted after use) — not saved as a permanent artifact.

## Pitfalls

- **Discovery blind spot — another drive exists**: The user has projects on BOTH C: and E: drives. Always explicitly scan all drives (C:, D:, E:) when doing system-wide work. Missing a drive is the #1 miss category.
- **Discovery blind spot — hidden dirs**: search_files and ripgrep-based tools skip hidden directories (like ~/.codex/). Use find with explicit exclusions and maxdepth for thorough coverage.
- **AppData depth**: Windows AppData directories are 7+ levels deep. maxdepth 5 is NOT enough — use 8+.
- **Prepending vs appending**: DOX goes at the TOP of root AGENTS.md. Never append it.
- **YAML frontmatter — DOX placement depends on file type**:
  - **Project-root AGENTS.md**: DOX goes BEFORE the frontmatter (at the top). This is the primary pattern — the DOX framework is the first thing an agent reads when opening the file. Prepend to the file.
  - **Hermes profile AGENTS.md** (chief-of-staff pattern): DOX framework comes FIRST at the top, then the YAML frontmatter is embedded in the middle of the document (after the DOX content and Child DOX Index), followed by the agent definition. This works because Hermes parses frontmatter from anywhere in the file:
    ```
    # DOX framework (top)
    ...
    ## Child DOX Index
    This profile owns its own scope...
    ---
    name: agent-name      ← frontmatter here
    codename: ...
    ---
    # Agent Name — Agent Definition (below frontmatter)
    ```
  - **Standalone agent definition files** (agent-universe, osint-framework teams): DOX goes AFTER the closing `---` of the YAML frontmatter, not at the top. The frontmatter is the agent's identity; DOX is operational context that follows it.
  
  The key rule: DOX must be the first significant CONTENT a reader sees. If the file opens with frontmatter, the frontmatter borders (`---`) do NOT count as content — DOX goes after the closing `---`. If there's no frontmatter, DOX goes at the very top. For Hermes profiles, DOX goes at the top because the frontmatter is secondary identity data, not primary content.
- **Existing child docs**: If a subdirectory already has an AGENTS.md, reformat to DOX child doc shape rather than overwriting.
- **Root vs child distinction**: Only root AGENTS.md gets the full DOX framework. Child docs get the simplified shape.
- **Batch edits efficiently**: Use patch for root prepends in parallel. Write child docs via write_file in batch.
- **Windows path format in Python**: os.path.isdir('${MY_REPOS}/...') returns False on Windows Python. Use native paths: ${MY_REPOS}\Documents\github. os.walk works fine with E:\ paths.

## References

- `references/dox-framework.md` — The canonical DOX AGENTS.md content (source of truth for the framework block)
- `references/dox-readme.md` — DOX README: what it is, how it works, credits
- `references/discovery-pattern.md` — Real discovery sequences from a 21-file system-wide AGENTS.md search

## Related Skills

- `project-documentation-standards` — Covers README, ROADMAP, license work (human-facing docs vs AI-agent context)
