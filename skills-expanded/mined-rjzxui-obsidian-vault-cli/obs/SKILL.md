---
name: obs
description: "Manage Obsidian vaults from the terminal using obs CLI. Search notes, manage tags, properties, links, tasks, daily notes, templates, bookmarks, plugins, canvas, and bases. Use when the user works with Obsidian vaults, markdown notes, or wants to query/modify vault content from the command line."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
---

# obs — Open Vault CLI

`obs` is a community-built CLI for Obsidian vaults. It reads and writes vault files directly on disk — no running Obsidian instance needed.

## Installation

```bash
npm install -g obsidian-vault-cli
```

## Setup

```bash
obs init                              # Auto-detect vaults
obs vault config defaultVault /path   # Or set manually
```

## Global Options

| Flag | Description |
|------|-------------|
| `--vault <path>` | Path to Obsidian vault (overrides config) |
| `--json` | Output as JSON for scripting |
| `--help` | Show help for any command |

## Command Groups

### vault — Vault information and configuration

```bash
obs vault info                        # Name, path, file count, plugins
obs vault stats                       # Sizes, extensions, top tags
obs vault config                      # Print all config
obs vault config defaultVault /path   # Set default vault
```

### files — File operations

```bash
obs files list                        # List all files
obs files list --folder Notes --sort modified --limit 20
obs files read path/to/note.md        # Print file content
obs files read path/to/note.md --head 10
obs files write path/to/note.md --content "New content"
obs files create path/to/new.md       # Create a new file
obs files create path/to/note.md --template Meeting
obs files delete path/to/note.md      # Delete (with confirmation)
obs files move old/path.md new/path.md
obs files rename path/to/note.md new-name.md
obs files total                       # Count of markdown files
```

### search — Search vault content

```bash
obs search content "search term"      # Full-text search
obs search content "TODO" --case-sensitive --limit 10
obs search path "meeting"             # Find files by name
obs search path "**/*.canvas"         # Glob pattern
obs search regex "TODO|FIXME"         # Regex search
obs search regex "\d{4}-\d{2}-\d{2}" --flags gi
```

### tags — Manage tags

```bash
obs tags list path/to/note.md         # Tags from frontmatter
obs tags add path/to/note.md project  # Add a tag
obs tags remove path/to/note.md project
obs tags all                          # All tags with counts
obs tags all --sort name --min-count 5
```

### daily — Daily notes

```bash
obs daily create                      # Create today's note
obs daily create --date 2025-01-15    # Specific date
obs daily create --template "Daily Template"
obs daily open                        # Print today's note
obs daily open --date 2025-01-15
obs daily list                        # Recent daily notes
obs daily list --limit 30 --days 7
```

### properties — Frontmatter properties

```bash
obs properties read path/to/note.md           # All properties
obs properties read path/to/note.md title     # Specific property
obs properties set path/to/note.md status draft
obs properties set path/to/note.md tags "a,b,c"
```

### templates — Template management

```bash
obs templates list                    # List templates
obs templates apply "Meeting" Notes/standup.md
obs templates create "Weekly Review"
obs templates create "Bug Report" --content "## Bug\n\n## Steps"
```

### tasks — Find and manage tasks

```bash
obs tasks all                         # All tasks in vault
obs tasks pending                     # Unchecked only
obs tasks done                        # Completed only
obs tasks pending --file path/to/note.md
obs tasks add path/to/note.md "Buy groceries"
obs tasks toggle path/to/note.md 15   # Toggle at line 15
obs tasks remove path/to/note.md 15
```

### bookmarks — Vault bookmarks

```bash
obs bookmarks list
obs bookmarks add path/to/note.md
obs bookmarks remove path/to/note.md
```

### links — Analyze links

```bash
obs links list path/to/note.md       # Outgoing links
obs links outgoing path/to/note.md
obs links backlinks path/to/note.md  # Incoming links
obs links broken                     # Unresolved wikilinks
obs links broken --limit 20
```

### plugins — Plugin management

```bash
obs plugins list                     # All plugins with status
obs plugins list --enabled
obs plugins list --disabled
obs plugins versions                 # Community plugin versions
obs plugins enable dataview
obs plugins disable dataview
```

### dev — Developer tools

```bash
obs dev eval "vault.listFiles()"     # Evaluate JS
obs dev script ./my-script.js        # Run script with vault context
```

### sync — Git sync

```bash
obs sync status                      # Git status
obs sync push                        # Stage, commit, push
obs sync push --message "Updated notes"
obs sync pull                        # Pull latest
```

### themes — Theme management

```bash
obs themes list                      # Installed themes
obs themes apply "Minimal"           # Apply a theme
```

### canvas — Canvas files

```bash
obs canvas list                      # List canvases
obs canvas read path/to/canvas.canvas
obs canvas create path/to/new.canvas
obs canvas create path/to/new.canvas --text "Hello"
obs canvas nodes path/to/canvas.canvas
```

### bases — Base files

```bash
obs bases list                       # List base files
obs bases read path/to/base.base
obs bases create path/to/new.base
obs bases create path/to/new.base --source Notes
```

### import — Import content

```bash
obs import url https://example.com/article
obs import url https://example.com --name "My Article"
```

## JSON Mode & Scripting

All commands support `--json` for machine-readable output:

```bash
obs vault stats --json | jq '.fileCount'
obs tasks pending --json | jq -r '.[] | [.file, .line, .text] | @csv'
obs tags all --json | jq '.[0:5]'
obs search content "TODO" --json | jq '[.[].file] | unique'
```

## More Details

See [references/COMMANDS.md](references/COMMANDS.md) for full option details and advanced examples.
