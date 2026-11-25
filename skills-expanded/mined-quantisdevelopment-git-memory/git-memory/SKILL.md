---
name: git-memory
description: Persistent project memory for AI agents — indexes git history, extracts features/decisions/anti-patterns, and builds a searchable knowledge graph per project. Use when working on any git-tracked codebase and you need to recall what was built, what was decided, which files handle what, or search project history. Activates when agent starts working in a project, needs context about past changes, wants to record decisions, or searches for features/files/anti-patterns.
---

# git-memory

Gives you persistent, queryable memory for any git project. Never lose context, redo work, or forget decisions.

## Quick Start

```bash
# In any git repo:
git-memory init         # Creates .git-memory/memory.db (gitignored)
git-memory sync         # Import commits, extract features, map files
git-memory query "X"    # Search everything
```

## When to Use

- **Session start**: Run `git-memory sync --if-stale` to ensure memory is fresh
- **Before building**: `git-memory query "search bar"` — check if it already exists
- **After building**: Features auto-extracted from `feat:` commits on next sync
- **Recording decisions**: `git-memory add-decision "Use SQLite not Postgres" --importance high`
- **Recording mistakes**: `git-memory add-anti "Never rm -rf the DB" --severity critical --rule "Use trash instead of rm"`
- **Finding files**: `git-memory file-for "parsing"` — shows relevant source files with purposes

## Commands

| Command | Purpose |
|---------|---------|
| `init` | Initialize memory for current git repo |
| `sync [--force] [--if-stale]` | Import new commits, extract features, map files |
| `query <text>` | BM25 semantic search across all knowledge |
| `features [--status active]` | List extracted features |
| `decisions` | List recorded decisions |
| `anti-patterns` | List anti-patterns (things NOT to do) |
| `files` | List source files with inferred purposes |
| `file-for <text>` | Find files related to a topic |
| `add-decision <text> [--category X --importance high]` | Record a decision |
| `add-anti <text> [--rule X --severity critical]` | Record an anti-pattern |
| `status` | DB stats, sync freshness, project info |
| `projects` | List all git-memory projects on disk |

## Proactive Usage Protocol

On every session start in a project directory:

1. Check if `.git-memory/` exists. If not, run `git-memory init && git-memory sync`
2. If exists, run `git-memory sync --if-stale --quiet` (skips if <1h old)
3. Before implementing anything, `git-memory query "<feature name>"` to check if it exists
4. After implementing, commit with `feat:` prefix — auto-extracted on next sync
5. Record important decisions with `add-decision`
6. Record mistakes/anti-patterns with `add-anti`

## Configuration

Per-project config at `.git-memory/config.json`:

```json
{
  "file_extensions": [".py", ".js", ".ts"],
  "src_dirs": ["src", "lib", "app"],
  "synonyms": {
    "trade": ["signal", "position", "order"],
    "dashboard": ["ui", "frontend", "panel"]
  },
  "extra_repos": [
    {"path": "~/other-repo", "name": "shared-lib"}
  ]
}
```

- **file_extensions**: Auto-detected on init. Add more as needed.
- **src_dirs**: Where to scan for source files.
- **synonyms**: Domain-specific search expansion (merged with base concepts).
- **extra_repos**: Index additional related repos into same DB.

## How It Works

- **Commits**: Imported via `git log` with file stats (insertions/deletions/files changed)
- **Features**: Auto-extracted from `feat:` conventional commits
- **Files**: Scanned from src dirs, purpose inferred from docstrings/comments
- **Search**: BM25 scoring with synonym expansion (no ML deps, pure Python)
- **Storage**: SQLite at `.git-memory/memory.db` — gitignored, survives reboots
- **Cross-refs**: Features auto-linked to files via commit change lists

## Systemd Timer (optional, for always-fresh memory)

```bash
# Create a user timer that syncs every 4 hours:
cat > ~/.config/systemd/user/git-memory-sync@.service << 'EOF'
[Unit]
Description=git-memory sync for %i

[Service]
Type=oneshot
WorkingDirectory=%h/projects/%i
ExecStart=/path/to/git-memory sync
TimeoutStartSec=120
EOF

systemctl --user enable --now git-memory-sync@myproject.timer
```

## Zero Dependencies

Pure Python 3.8+ and SQLite. No pip install needed. Works on any system with git.
