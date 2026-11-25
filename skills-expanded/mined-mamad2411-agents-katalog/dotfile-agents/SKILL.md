# dotfile — Machine Provisioning Guide

This repo bootstraps a development environment on macOS or Linux, with special support for shared Docker/headless setups where each container has a different `$HOME`.

## Architecture

```
~/dotfile/          ← this repo (cloned from git)
  ├── .codex/       ← gitignored shared runtime, symlinked to ~/.codex
  ├── .agents/      ← gitignored local agent/runtime workspace, when present
  ├── zsh/          ← modules sourced into generated ~/.zshrc
  ├── tmux/         ← symlinked to ~/.tmux.conf
  ├── git/          ← symlinked to ~/.gitconfig
  ├── nvim/         ← symlinked to ~/.config/nvim
  ├── yazi/         ← symlinked to ~/.config/yazi
  └── init.sh       ← idempotent bootstrap script
```

Key design: `~/.codex` is a **symlink into this repo**, not a copy. The directory inside the repo is a shared runtime target and is gitignored, so multiple Docker containers can share sessions, settings, credentials, hooks, and local installed agent assets without each container rebuilding its own `$HOME`.

When provisioning a machine that already has a real `~/.codex` directory, quit active Codex processes first. `init.sh` moves that complete directory into the repository and then creates the symlink. If the home and repository runtime directories both contain data, it refuses to merge them automatically.

Tracked files in this repo are the reproducible bootstrap surface: `init.sh`, shell modules, tmux, git, Neovim, Yazi, and documentation. Runtime state and secrets stay out of Git.

## Prerequisites

Before provisioning, verify the bootstrap requirements:

- `git` — required to clone this repo
- `curl` — macOS provides it; required by the user-local network installers
- `brew` — required on macOS for package installation

The script installs Bun, jq, fnm, Node.js LTS, and the remaining managed tools when they are missing.

`init.sh` uses `fnm` to install the latest Node.js LTS and keeps Bun as an independent runtime. Do not install Node.js with Homebrew/apt or create Bun compatibility shims for `node`, `npm`, `npx`, `yarn`, `pnpm`, or `corepack`.

## Provisioning a new machine

### Step 1: Clone and bootstrap

```bash
# Ask the user for the repo URL, then:
git clone <url> ~/dotfile
cd ~/dotfile
./init.sh
```

`init.sh` is idempotent — safe to rerun. It:
- Detects OS (macOS → Homebrew, Linux → apt-get)
- Reuses macOS system zsh, Git, and curl when available; installs missing core tools plus tmux, ripgrep, fzf, Neovim, fnm, GitHub CLI, unzip, and Yazi support tools
- Installs Oh My Zsh + plugins (autosuggestions, syntax-highlighting)
- Installs Rust + Yazi via rustup/cargo
- Installs uv and ruff as user-local Python tooling
- Uses fnm to install the latest Node.js LTS and default alias; installs Bun independently without compatibility shims
- Falls back to the official latest Neovim tarball on Linux if system nvim < 0.11.2
- Backs up conflicts to `~/.dotfile-backups/<timestamp>/`
- Creates symlinks: `~/.tmux.conf`, `~/.gitconfig`, `~/.config/nvim`, `~/.config/yazi`, `~/.codex`
- Generates `~/.zshrc` from tracked zsh modules
- Switches default shell to zsh

Useful options:
```bash
./init.sh --link-only      # only generate dotfiles/symlinks; no installs or chsh
./init.sh --no-packages    # skip apt/Homebrew installs
./init.sh --no-user-tools  # skip Rust, fnm/Node LTS, Bun, Yazi, and Oh My Zsh
./init.sh --upgrade-neovim # install the latest official Neovim release
./init.sh --no-chsh        # do not change login shell
```

After `init.sh` completes, it prints a summary. Check the **Warnings** section — any tool listed there needs attention before continuing. If init.sh succeeded without warnings, proceed to Step 2.

### Step 2: Verify symlinks

```bash
ls -la ~/.codex ~/.tmux.conf ~/.gitconfig ~/.config/nvim ~/.config/yazi
```

All should point into `~/dotfile/`. If any is missing or broken, re-run `./init.sh`.

### Step 3: Create secret files (manual, not in git)

If an existing Codex runtime was migrated, its authentication and configuration are preserved automatically. On a machine with no previous runtime, create `~/.codex/auth.json` and `~/.codex/config.toml` after provisioning. These files are gitignored; ask the user for the required credentials and settings.

### Step 4: Configure machine-specific shell values

Edit `~/.zshrc` and modify only the block between:
```
# >>> dotfile local block >>>
# <<< dotfile local block <<<
```

Put machine-only exports here (private paths, cluster URLs, etc.). This block survives `init.sh` reruns.

### Step 5: Install Neovim plugins

```bash
nvim --headless "+Lazy! sync" +qa  # installs LazyVim plugins non-interactively
```

Requires internet access.

### Step 6: Verify tooling

```bash
# Check core tools are on PATH
which zsh tmux git curl rg fzf nvim yazi gh fnm bun node npm npx

# Authenticate the GitHub CLI credential helper once per machine
gh auth login

# Check Codex reads its config
ls -la ~/.codex/auth.json ~/.codex/config.toml
```

## Linux / Docker / Headless specifics

In minimal or headless environments, some tools may be missing:

1. **No sudo / no apt**: `init.sh` still creates symlinks and generates `~/.zshrc`. Install packages manually or as root before running.

## What lives where

### .codex/ (OpenAI Codex CLI)

| Path | What | Tracked |
|------|------|---------|
| `AGENTS.md` | Global Codex guidance | No |
| `rules/default.rules` | Local allow-list rules | No |
| `skills/.system/` | Local system skills | No |
| `skills/inspire/` | Local Inspire platform skill | No |
| `skills.disabled-*/`, `agents.disabled-*/` | Archived local skills/agents, not active | No |
| `vendor_imports/skills/` | Local upstream skill sync, if installed | No |
| `auth.json` | Credentials | **No** — gitignored |
| `config.toml` | Config | **No** — gitignored |
| `sessions/`, `log/`, `*.sqlite` | Runtime state | **No** — gitignored |

## Updating after repo changes

| Change type | Apply with |
|-------------|-----------|
| Shell modules | `./init.sh && source ~/.zshrc` |
| tmux | `tmux source-file ~/.tmux.conf` |
| Neovim / Yazi | Restart application |
| Codex runtime rules, skills, agents, hooks | Immediate — `~/.codex` is a live symlink, but gitignored |

## Troubleshooting

- **Symlink broken**: `ls -la ~/.codex` should point into `~/dotfile/`. If not, `./init.sh` will fix it.
- **Neovim plugins missing**: First launch needs internet. If LazyVim errors, check `nvim --version` is >= 0.11.2.
- **Existing Codex runtime**: If only `~/.codex` contains data, `./init.sh` migrates the complete directory into this repo and creates the symlink. Quit active Codex processes before doing this.
- **Codex runtime conflict**: If both `~/.codex` and `~/dotfile/.codex` contain data, the installer stops without changing either one. Compare and merge them manually, then rerun `./init.sh`.
