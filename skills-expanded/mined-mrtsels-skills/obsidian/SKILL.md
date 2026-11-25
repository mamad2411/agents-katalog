---
name: obsidian
description: Read, search, and manage notes in the Obsidian vault. Includes community plugin installation via GitHub API.
version: 2.0.0
category: note-taking
tags: [obsidian, notes, vault, plugin]
---

# Obsidian Vault

**Location:** Set via `OBSIDIAN_VAULT_PATH` env var (e.g. in `~/.hermes/.env`).
Defaults to `~/wiki` (user's primary vault).

Note: Vault paths may contain spaces — always quote them in shell commands.

## Read a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/wiki}"
cat "$VAULT/Note Name.md"
```

## List notes

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/wiki}"
find "$VAULT" -name "*.md" -type f
find "$VAULT/Subfolder/" -name "*.md"
```

## Search

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/wiki}"
# By filename
find "$VAULT" -name "*.md" -iname "*keyword*"
# By content
grep -rli "keyword" "$VAULT" --include="*.md"
```

## Create a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/wiki}"
cat > "$VAULT/New Note.md" << 'ENDNOTE'
# Title

Content here.
ENDNOTE
```

## Append to a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/wiki}"
echo -e "\nNew content here." >> "$VAULT/Existing Note.md"
```

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. Use these to link related content when creating notes.

---

## Community Plugin Installation

Install any Obsidian community plugin directly from GitHub — no browser needed.

### Step 1: Get release assets via GitHub API

```bash
# Get latest release assets (returns download URLs for main.js, manifest.json, etc.)
curl -s "https://api.github.com/repos/AUTHOR/REPO/releases/latest" | \
  python3 -c "import sys,json,base64; d=json.load(sys.stdin); \
  [print(a['name'], ':', a['browser_download_url']) for a in d.get('assets',[])]"
```

### Step 2: Download plugin files

Standard plugin files needed:
- `main.js` — always required
- `manifest.json` — always required
- `styles.css` — optional, for UI styling
- Any other assets (check the release)

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/wiki}"
PLUGIN_DIR="$VAULT/.obsidian/plugins/PLUGIN-NAME"
mkdir -p "$PLUGIN_DIR"

# Download required files
curl -sL "https://github.com/AUTHOR/REPO/releases/download/TAG/main.js" -o "$PLUGIN_DIR/main.js"
curl -sL "https://github.com/AUTHOR/REPO/releases/download/TAG/manifest.json" -o "$PLUGIN_DIR/manifest.json"
# styles.css is optional — only if it exists
curl -sL "https://github.com/AUTHOR/REPO/releases/download/TAG/styles.css" -o "$PLUGIN_DIR/styles.css"
```

### Step 3: Enable in community-plugins.json

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/wiki}"
COMMUNITY_PLUGINS="$VAULT/.obsidian/community-plugins.json"

# Read existing enabled plugins
python3 -c "
import json
with open('$COMMUNITY_PLUGINS') as f:
    plugins = json.load(f)
if 'PLUGIN-NAME' not in plugins:
    plugins.append('PLUGIN-NAME')
with open('$COMMUNITY_PLUGINS', 'w') as f:
    json.dump(plugins, f, indent=2)
print('Updated:', plugins)
"
```

### Step 4: Activate in Obsidian

Obsidian must reload the vault to pick up new plugins. Options:
- Press `Cmd+P` in Obsidian, type `reload`, press Enter
- Or close and reopen the vault
- Then go to `Settings → Community Plugins` and enable the plugin

### Step 5: Verify

```bash
# Check server is running (for REST API plugins)
curl -k https://127.0.0.1:27124/

# With auth (get API key from Settings → Local REST API)
curl -k -H "Authorization: Bearer YOUR_API_KEY" https://127.0.0.1:27124/vault/
```

### Finding the right GitHub repo

- Community plugins are on GitHub under the author's account
- Search at https://obsidian/plugins or the Obsidian community plugin list
- The repo typically contains `manifest.json` and `main.js` in its releases
