---
name: ghq-sector-cli
description: >
  Step-by-step guide for using ghq-sector (gsec) — a CLI that layers categorized workspace views
  on top of ghq. Use this skill whenever the user asks about setting up ghq-sector, running gsec
  commands (init, clone, sync, edit, doctor, apply), configuring ghq-sector.config.json, managing
  multi-repo workspaces with AI agents, or organizing ghq-managed repositories into categories.
  Also use when the user mentions ghq-sector, gsec, workspace views, categorized repos, or
  .code-workspace generation with ghq, even if they don't explicitly name the tool.
---

# ghq-sector CLI Usage Guide

ghq-sector builds a categorized workspace on top of `ghq` — keeping clones where `ghq` put them while creating a clean directory structure with symlinks, copied resources, and a `.code-workspace` file.

## Prerequisites

- Node.js 20+
- `ghq` — installed and configured (`ghq root` must return a valid path)
- `gh` — optional but recommended (enables owner detection and shorthand clone flows)

## Quick Start

```
npx ghq-sector init
```

This creates `ghq-sector.config.json`, the workspace root, and default category directories. After init, open the visual editor:

```
gsec edit
```

If installed globally (`npm install -g ghq-sector`), use the `gsec` shorthand. Otherwise use `npx ghq-sector` or `bunx ghq-sector`.

## Commands

### `gsec init` — Bootstrap a new workspace

Creates the config file and workspace structure.

```bash
gsec init
gsec init --ghq-root ~/ghq --workspace-root ~/workspace/sector --yes
```

**Options:**
- `--ghq-root <path>` — set the ghq root directory
- `--workspace-root <path>` — set where category directories and symlinks live
- `--yes` — skip all prompts, use detected/defaults

**What happens:**
1. Prompts for (or detects) ghq root and workspace root
2. Creates `ghq-sector.config.json` in the current directory
3. Creates workspace root directory and default categories (`projects`, `tools`, `docs`)
4. Offers to open the visual editor

### `gsec clone <repository>` — Clone and add a repo

Clones via `ghq`, appends to config, syncs workspace.

```bash
gsec clone owner/repo
gsec clone repo --owner myorg --category tools
gsec clone github.com/owner/repo --provider github.com
gsec clone owner/repo --yes
```

**Accepted formats:**
- `provider/owner/name` — fully qualified
- `owner/name` — uses `defaults.provider`
- `name` — requires `--owner`, `defaults.owner`, or interactive gh account selection

**Options:**
- `--category <name>` — which category to place the repo in
- `--owner <name>` — override the repo owner
- `--provider <name>` — override the git provider
- `--yes` — skip owner selection, use active/default account

### `gsec sync` — Regenerate workspace from config

Rebuilds symlinks, copies resources, regenerates `.code-workspace`.

```bash
gsec sync
```

Run this after editing the config manually or when the workspace is out of date.

### `gsec edit` — Visual config editor

Starts a local web UI built with visual-json.

```bash
gsec edit
gsec edit --config ./ghq-sector.config.json --no-open
gsec edit --host 0.0.0.0 --port 4173
```

**Options:**
- `--config <path>` — config file or directory containing it
- `--host <host>` — bind address (default `127.0.0.1`)
- `--port <port>` — port (default `4173`)
- `--no-open` — don't auto-open browser

### `gsec doctor` — Validate environment and config

Checks ghq/gh availability, config validity, resource paths, symlink health, and workspace state.

```bash
gsec doctor
```

Run this when something seems wrong — it reports warnings and successes for every aspect of the setup.

### `gsec apply` — Full apply (clone missing + sync + copy config)

Ensures all configured repos are cloned, then syncs the workspace and copies the config into the workspace root.

```bash
gsec apply
```

## Config File: `ghq-sector.config.json`

```json
{
  "ghqRoot": "/Users/you/ghq",
  "workspaceRoot": "/Users/you/workspace/main",
  "categories": ["projects", "tools", "docs"],
  "defaults": {
    "provider": "github.com",
    "owner": "your-github-username",
    "category": "projects"
  },
  "repos": [
    {
      "provider": "github.com",
      "owner": "owner",
      "name": "repo-name",
      "category": "projects"
    }
  ],
  "resources": [
    { "from": ".envrc.template", "to": ".envrc" }
  ],
  "hooks": {
    "afterInit": [],
    "beforeClone": [],
    "afterClone": [],
    "afterLink": [],
    "afterSync": []
  },
  "editor": {
    "codeWorkspace": {
      "enabled": true
    }
  }
}
```

### Key fields

| Field | Description |
|---|---|
| `ghqRoot` | Absolute path to ghq root |
| `workspaceRoot` | Absolute path where categories and symlinks are created |
| `categories` | Array of category directory names |
| `defaults` | Default provider, owner, category for shorthand clones |
| `repos` | Array of repo entries (`provider`, `owner`, `name`, `category`) |
| `resources` | Files to copy into workspace on sync (`from`/`to` paths) |
| `hooks` | Shell commands run at lifecycle points. Use `{{ var }}` for template variables |
| `editor.codeWorkspace` | Controls `.code-workspace` generation |

### Hook template variables

| Hook | Available variables |
|---|---|
| `afterInit` | `ghqRoot`, `workspaceRoot` |
| `beforeClone` / `afterClone` | `provider`, `owner`, `repo`, `category`, `ghqPath`, `workspacePath`, `ghqRoot`, `workspaceRoot` |
| `afterLink` | Same as `afterClone` |
| `afterSync` | `ghqRoot`, `workspaceRoot`, `linkedCount` |

## Typical Workflow

1. **First time:** `gsec init` → configure via `gsec edit` or edit JSON directly
2. **Adding repos:** `gsec clone owner/repo --category projects`
3. **After config changes:** `gsec sync`
4. **Reproducing on another machine:** copy config → `gsec apply`
5. **Health check:** `gsec doctor`

## Tips

- The config file is the single source of truth — share it via dotfiles or version control for reproducibility
- `gsec apply` is the easiest way to get a full workspace set up from a config file on a new machine
- Use `--yes` with init and clone for non-interactive/CI usage
- The visual editor (`gsec edit`) provides both a UI view and raw JSON editing
