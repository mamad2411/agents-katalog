---
name: super-worktree
description: Create isolated git worktrees for parallel feature work with monorepo-aware env file copying and node_modules symlinking.
---

# super-worktree

A skill for managing isolated git worktrees for parallel feature development with monorepo-aware env file copying and node_modules symlinking.

## Worktree Creation Overview

Git worktrees let you work on multiple branches simultaneously in a single repository. This skill enhances worktrees with:

- **Sensitive file copying** — `.env`, credentials, secrets propagated to new worktrees (configurable depth for monorepos)
- **node_modules symlinking** — saves disk space; supports nested workspace layouts
- **Detached terminal spawn** — opens new tmux/zellij/Kitty/WezTerm/Ghostty/Alacritty/GNOME/Konsole/Windows-Terminal/iTerm2 tab and auto-launches the detected AI tool (claude, opencode, codex, cursor, cline, windsurf, aider). Survives the calling AI session via `setsid`+`disown`.
- **Lifecycle hooks** — `preCreate`/`postCreate`/`preDelete`/`postDelete` shell commands from config
- **Local-only ignore** — uses `.git/info/exclude` instead of polluting tracked `.gitignore`
- **Metadata tracking** — base branch, creation timestamp, AI tool stored per worktree under `.worktrees/.metadata/<branch>.json`
- **Configurable patterns** — global (`~/.config/super-worktree/config.json`), project (`super-worktree.json`), or `--config` flag

## Creating a worktree

```bash
bash scripts/worktree-manager.sh create <branch> [from-branch] [options]
```

**Parameters:**
- `<branch>` — name of the new branch/worktree (required)
- `[from-branch]` — base branch to create from (defaults to `origin/HEAD` or `main`)

**Options:**
- `--config <file>` — custom config JSON path
- `--tool <name>` — force AI tool (claude, opencode, codex, cursor, cline, windsurf, aider)
- `--ide <name>` — open IDE instead of AI tool (code, cursor, idea, webstorm, pycharm, zed, subl, nvim, vim)
- `--ticket <id>` — ticket id, used for branch templating (e.g. `WFL-1234`)
- `--slug <text>` — slug text; combined with `--ticket` to form `wfl-1234-research-helmet`
- `--from-pr <num>` — fetch and check out a GitHub PR via `gh pr checkout`
- `--no-spawn` — skip terminal spawn (useful for scripts/CI)
- `--print-cd` — print `cd <path>` to stdout (so callers can `eval $(...)`)
- `--dry-run` — show intended actions; no changes

**Environment overrides:**
- `SUPER_WORKTREE_TOOL=<name>` — override AI tool detection
- `TRUST_DIRENV=1` — auto-run `direnv allow` on copied `.envrc`
- `NO_SPAWN=1` / `DRY_RUN=1` / `PRINT_CD=1` — equivalent to flags

**Examples:**
```bash
# Create feature branch from origin/HEAD
bash scripts/worktree-manager.sh create feature/new-login

# Custom config + force claude tool
bash scripts/worktree-manager.sh create feature/pay --config .super-worktree.json --tool claude

# CI-friendly creation (no terminal launch)
bash scripts/worktree-manager.sh create hotfix/urgent --no-spawn

# Eval cd into new worktree from your shell
cd "$(bash scripts/worktree-manager.sh create feat/x --print-cd --no-spawn | tail -1 | sed 's|^cd ||')"
```

## Deleting a worktree

```bash
bash scripts/worktree-manager.sh delete <branch>
```

Removes the worktree and optionally deletes the branch (use with caution).

**Example:**
```bash
bash scripts/worktree-manager.sh delete feature/new-login
```

## Cleaning up (merge)

```bash
bash scripts/worktree-manager.sh merge <branch>
```

Merges the branch into its upstream and then deletes the worktree. Use when feature is complete.

**Example:**
```bash
bash scripts/worktree-manager.sh merge feature/new-login
```

## Listing worktrees

```bash
bash scripts/worktree-manager.sh list           # human-readable table
bash scripts/worktree-manager.sh list --json    # machine-readable
```

Prints branch, base, creation timestamp, and AI tool for each worktree.

## Status

```bash
bash scripts/worktree-manager.sh status         # clean/dirty per worktree
bash scripts/worktree-manager.sh status --json  # machine-readable
```

## Sync (re-pull env into existing worktree)

```bash
bash scripts/worktree-manager.sh sync <branch>
```

Re-runs copy + symlink + dev-tool trust against an existing worktree. Use after rotating `.env` or adding new credentials.

## Pruning orphans

```bash
bash scripts/worktree-manager.sh prune
```

Runs `git worktree prune` and removes stale `.worktrees/.metadata/*.json` entries.

## Version

```bash
bash scripts/worktree-manager.sh version
```

## Configuration

Create a `super-worktree.json` in your project root for custom patterns:

```json
{
  "sync": {
    "copyFiles": [
      ".env",
      ".env.*",
      ".envrc",
      ".local.*",
      "*.secret",
      "*.key",
      ".secrets.*",
      "credentials.json",
      "credentials.yml",
      "credentials.env",
      "auth.json",
      "auth.yml",
      "auth.env",
      ".dev.vars",
      ".prod.vars",
      ".staging.vars"
    ],
    "symlinkDirs": [
      "node_modules"
    ],
    "exclude": [
      "node_modules",
      ".git",
      "dist",
      "build",
      ".next",
      "out",
      "coverage",
      ".turbo",
      ".vercel",
      ".worktrees"
    ],
    "copyDepth": 2
  },
  "hooks": {
    "preCreate":  "echo creating $BRANCH",
    "postCreate": "pnpm install --frozen-lockfile",
    "preDelete":  "echo cleaning $BRANCH"
  }
}
```

### Glob negation

Prefix any `copyFiles` entry with `!` to exclude it. Defaults already exclude `.env.example`, `.env.sample`, `.env.template`.

```json
{
  "sync": {
    "copyFiles": [".env", ".env.*", "!.env.example", "credentials.json"]
  }
}
```

### Env interpolation

Whitelisted variables expand inside `copyFiles` paths: `$HOME`, `${HOME}`, `$USER`, `${USER}`, `${XDG_CONFIG_HOME}`. Use absolute paths to copy files outside the repo:

```json
{
  "sync": {
    "copyFiles": ["${HOME}/.aws/credentials"]
  }
}
```

### Hooks

Hook commands run with `cd $GIT_ROOT` and these env vars: `BRANCH`, `BASE`, `WORKTREE_PATH`. Non-zero exit emits a warning but does not abort the operation.

Common uses:
- `postCreate`: `pnpm install`, `bun install`, `composer install`, `make setup`, etc.
- `preDelete`: archive logs, dump db, kill watchers tied to the worktree.

### Config Priority

Configuration is loaded in this order (later overrides earlier):

1. **Built-in defaults** - Always available
2. **Global config** - `~/.config/super-worktree/config.json`
3. **Project config** - `.super-worktree.json` in repo root
4. **CLI flag** - `--config <file>` argument (highest priority)

### JSON Schema

A [JSON Schema](schemas/super-worktree.schema.json) is provided for config validation:

```json
{
  "$schema": "./schemas/super-worktree.schema.json",
  "sync": {
    "copyFiles": [".env", ".env.local"],
    "symlinkDirs": ["node_modules", ".pnpm-store"],
    "exclude": ["dist", "build"]
  }
}
```

## Default Patterns

The skill includes sensible defaults that cover most projects:

### copyFiles (copied to worktree)
- `.env`, `.env.*` - Environment files
- `.envrc` - direnv config
- `.local.*` - Local overrides
- `*.secret`, `*.key`, `.secrets.*` - Secret files
- `credentials.json`, `credentials.yml`, `credentials.env` - Credentials
- `auth.json`, `auth.yml`, `auth.env` - Auth config
- `.dev.vars`, `.prod.vars`, `.staging.vars` - Environment-specific vars

### symlinkDirs (symlinked to save space)
- `node_modules` - Node dependencies

### exclude (not copied or symlinked)
- `node_modules`, `.git`, `dist`, `build`, `.next`, `out`, `coverage`, `.turbo`, `.vercel`, `.worktrees`

## Shell Completions

Bash, zsh, and fish completion files live in `completions/`:

```bash
# bash
echo 'source /path/to/super-worktree/completions/super-worktree.bash' >> ~/.bashrc

# zsh
cp completions/_super-worktree /usr/local/share/zsh/site-functions/

# fish
cp completions/super-worktree.fish ~/.config/fish/completions/
```

Completes subcommands, branch names (for `delete`/`merge`/`sync`), and flag values (`--tool`, `--ide`).

## AI Tool Detection

Resolution precedence (first match wins):
1. `--tool <name>` flag
2. `SUPER_WORKTREE_TOOL` env var
3. Parent process walk: traverses up to 12 ancestors, skipping shells (`bash`, `zsh`, `fish`, `pwsh`, …), matches against `claude`, `opencode`, `codex`, `cline`, `cursor`, `windsurf`, `aider`
4. Fallback: `opencode` (with warning)

## Terminal Spawn Priority

Tries in order, stops at first success:
1. **cmux** (when `$CMUX_WORKSPACE_ID` set)
2. **tmux** — new window inside session, or detached `wt-<branch>` session outside
3. **zellij** (when `$ZELLIJ` set)
4. **WezTerm** — `wezterm cli spawn` tab, fallback to detached window
5. **Kitty** — `kitty @ launch` tab, fallback to detached window
6. **Ghostty**
7. **Alacritty**
8. **GNOME Terminal**
9. **Konsole**
10. **Windows Terminal** (`wt.exe`, WSL)
11. **iTerm2** / **Terminal.app** (macOS, AppleScript)
12. Fallback: prints manual `cd … && <ai_tool>` instructions

External terminals are launched via `setsid nohup … & disown` so they survive the calling AI session exiting.

## Troubleshooting

### "worktree already exists"

The branch already has a worktree. Delete it first:

```bash
bash scripts/worktree-manager.sh delete <branch>
```

### "jq not found"

The script uses `jq` for JSON parsing. Install with:

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt install jq

# CentOS/RHEL
sudo yum install jq
```

### "python3 not found"

Fallback JSON parser requires Python 3. Ensure it's installed:

```bash
# Verify
python3 --version

# Install (macOS)
brew install python3

# Install (Ubuntu)
sudo apt install python3
```

### "cannot stat: No such file or directory"

The base branch or reference doesn't exist. Verify:

```bash
git branch -a
git log --oneline -5
```

### Permission denied

Make the script executable:

```bash
chmod +x scripts/worktree-manager.sh
```

### symlink fails with "File exists"

Remove existing `node_modules` in worktree first:

```bash
rm -rf .worktrees/<branch>/node_modules
bash scripts/worktree-manager.sh create <branch>
```

## Installation

### OpenCode (recommended via OCX)

```bash
# Install via OCX registry (recommended)
ocx add marioxe301/super-worktree --from https://marioxe301.github.io/super-worktree

# Or manual copy
cp -r super-worktree ~/.config/opencode/skills/
```

### Claude Code

```bash
# Claude marketplace
/plugin install marioxe301/super-worktree

# Or npx skills
npx skills add marioxe301/super-worktree -a claude-code
```

### Other AI Agents

```bash
# npx skills works with Codex, Cursor, Windsurf, Cline, and 40+ agents
npx skills add marioxe301/super-worktree

# Install to specific agents
npx skills add marioxe301/super-worktree -a codex -a cursor
```

### Manual

```bash
cp -r super-worktree ~/.config/opencode/skills/
```

## Requirements

- Git 2.5+ (worktree support)
- Bash 4.0+
- `jq` (optional, for JSON config; Python 3 fallback available)
- `python3` (optional, for JSON config fallback)