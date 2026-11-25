---
name: workspace-bridge
description: "This skill should be used when the user asks to 'sync workspace', 'pull from Google', 'push to Google', 'workspace-bridge pull', 'workspace-bridge push', 'workspace-bridge status', 'publish account brief', 'create meeting note', 'polish sheets', or mentions workspace-bridge sync operations. Bridges git-based account workspaces to Google Sheets/Docs with bidirectional sync."
user-invocable: true
---

# Workspace Bridge

Bridges local markdown workspace files to shared Google Sheets/Docs. The account team sees live data in Google; the SA works in git.

## Prerequisites

1. `/google-auth` must be run first (valid ADC token)
2. `.workspace-bridge.json` must exist in the workspace root (run `/workspace-bridge-init` first)

## Script Paths

All scripts are in this skill's resources directory. Resolve via:
```
RESOURCES="$(dirname "$(dirname "$(readlink -f "$0")")")/skills/workspace-bridge/resources"
```

Or use the plugin's installed path — the hooks auto-resolve via `__file__`.

## Commands

### `/workspace-bridge pull`

Pull latest data from Google Sheets/Docs into local markdown cache files.

```bash
python3 $RESOURCES/sync_pull.py --workspace "$PWD" --all
```

**What it does:**
- Reads each Google Sheet/Doc listed in `.workspace-bridge.json`
- Converts data to markdown tables/content
- Writes local cache files with sync timestamp headers
- Reports rows/lines synced per item

### `/workspace-bridge push`

Push local markdown changes to Google Sheets/Docs.

```bash
python3 $RESOURCES/sync_push.py --workspace "$PWD" --all
```

Use `--force` to push even if files haven't changed since last sync:
```bash
python3 $RESOURCES/sync_push.py --workspace "$PWD" --all --force
```

**What it does:**
- Parses local markdown tables from each tracked file
- Clears and re-writes the corresponding Google Sheet tabs
- Recreates Table objects with dropdown columns from table definitions
- For Google Docs, replaces the document body
- Skips unchanged files (unless --force)

### `/workspace-bridge status`

Show sync status for all bridged resources.

```bash
python3 $RESOURCES/bridge_config.py --workspace "$PWD"
```

Shows each resource, its Google ID, local file path, and whether the local file exists.

### `/workspace-bridge publish`

Regenerate the Account Brief Google Doc from current workspace data.

```bash
python3 $RESOURCES/publish_brief.py --workspace "$PWD"
```

**What it does:**
- Reads README.md, CLAUDE.md, and renewal war room docs
- Compiles an executive summary with key metrics, risks, and open items
- Updates the Account Brief Google Doc

### `/workspace-bridge publish-folder`

Publish a folder of markdown files as Google Docs.

```bash
python3 $RESOURCES/publish_folder.py --workspace "$PWD"
```

Requires a `folder_publish` sync item in config. Use `--force` to republish unchanged files.

### `/workspace-bridge publish-themes`

Group Q&A entries by theme and publish as separate Google Docs.

```bash
python3 $RESOURCES/publish_themes.py --workspace "$PWD"
```

Requires a `generated_publish` sync item in config. Themes are configurable via `publish_themes` in `.workspace-bridge.json`. Use `--force` to republish.

### `/workspace-bridge polish`

Apply professional formatting (headers, borders, conditional colors) to synced sheets.

```bash
python3 $RESOURCES/polish_sheets.py --workspace "$PWD" --all
```

### `/workspace-bridge meeting "Topic"`

Create or find a meeting note in Google Docs.

```bash
python3 $RESOURCES/meeting_notes.py --workspace "$PWD" create --topic "Topic" --date "2026-03-12" --attendees "Spencer,Andrew"
```

List existing meeting notes:
```bash
python3 $RESOURCES/meeting_notes.py --workspace "$PWD" list --date "2026-03-12"
```

Append SA processing to a meeting note:
```bash
python3 $RESOURCES/meeting_notes.py --workspace "$PWD" append --doc-id "DOC_ID" --section "SA Processing" --content "Analysis..."
```

**Anti-duplicate:** Searches folder for existing docs matching the date before creating.
**Anti-clobber:** Appends with timestamped section markers, never overwrites.

## Hook Behavior

### SessionStart (auto-pull)
When a session starts in a workspace with `.workspace-bridge.json`:
1. Auto-runs `sync_pull.py --all` silently
2. Local cache files refreshed from Google
3. Session protocol reads fresh cache

### Stop (auto-push)
When Claude finishes a response that modified bridged files:
1. Detects modified cache files (mtime > sync timestamp)
2. Runs `sync_push.py --all` for changed files only
3. Triggers publish scripts if source files changed
4. Reports items pushed

## Config Schema

The `.workspace-bridge.json` file supports these fields:

| Field | Required | Description |
|-------|----------|-------------|
| `workspace_name` | Yes | Account name |
| `sync_items` | Yes | Array of sync item definitions |
| `drive_folder_id` | No | Google Drive folder ID |
| `meeting_notes_folder_id` | No | Meeting Notes subfolder ID |
| `shared_with` | No | Array of email addresses |
| `table_definitions` | No | Custom table schemas (overrides defaults) |
| `publish_themes` | No | Custom theme keywords for Q&A grouping |

### Custom Table Definitions

Override default column schemas by adding `table_definitions` to your config:

```json
{
  "table_definitions": {
    "tracker": [{
      "tab_match": "Active",
      "table_name": "TrackerActive",
      "columns": [
        {"name": "Status", "type": "DROPDOWN", "values": ["New", "WIP", "Done"]}
      ]
    }]
  }
}
```

### Custom Publish Themes

Override default Q&A theme keywords:

```json
{
  "publish_themes": {
    "Infrastructure": ["networking", "security", "vpc"],
    "AI/ML": ["model", "serving", "agent", "llm"]
  }
}
```

## Resource Mapping

Resources are defined in `.workspace-bridge.json`. Common patterns:

| Local File | Google Resource | Direction |
|------------|----------------|-----------|
| tracker.md | Sheet (multi-tab) | Bidirectional |
| customer-qa.md | Sheet | Bidirectional |
| risk-register.md | Sheet | Bidirectional |
| research/index.md | Sheet (multi-tab) | Bidirectional |
| docs/org-intelligence.md | Doc | Bidirectional |
| Account Brief | Doc | Publish only |
| Meeting Notes | Docs (folder) | Create/append |

## Troubleshooting

- **"Token expired"** — Run `/google-auth` to refresh
- **"Config not found"** — Run `/workspace-bridge-init` first
- **"Permission denied"** — Ask folder owner to re-share
- **"fe-google-tools not found"** — Install fe-google-tools from the marketplace

## Reference Files

For detailed documentation, see the companion reference files:

- **Config Schema** — `references/config-schema.md` — Full .workspace-bridge.json schema with all field details, validation rules, and examples
- **Sync Patterns** — `references/sync-patterns.md` — How bidirectional sync works: pull/push flow, change detection, sync headers, multi-tab handling
- **Publishing Guide** — `references/publish-guide.md` — Publishing framework: folder_publish, generated_publish, theme classification, manifest tracking
