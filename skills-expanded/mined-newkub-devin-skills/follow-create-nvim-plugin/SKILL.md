---
name: follow-create-nvim-plugin
description: Configure Neovim plugins with lazy.nvim
argument-hint: "[scope]"
related:
  - follow-create-sdk
  - deep-review-codebase
  - ship

---
## Goal

Set up and manage Neovim plugins with `lazy.nvim` per best practices

## Scope

Use for projects that create or manage Neovim plugins

- Packages: Neovim >= 0.8.0 + `lazy.nvim` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (no pinning in this file — per `/update-devin-global-skills`)
- Neovim 0.12 ships the built-in `vim.pack` plugin manager — an acceptable alternative to lazy.nvim when advanced lazy-loading features aren't needed

## Execute

### 1. Review Tech Stack

> Goal: verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
3. Record the rationale for the chosen stack and libraries for future reference (create nvim plugins)

### 2. Prepare

> Goal: check requirements before starting

1. Install Neovim >= 0.8.0 (check the latest version with `/deep-research`)
2. Install Git >= 2.19.0
3. Have an `init.lua` as the entry point

### 3. Config Structure

> Goal: create the config structure for lazy.nvim

1. Create a `lua/plugins/` directory for plugin specs
2. Split plugin specs into files by category — `lua/plugins/core.lua`, `ui.lua`, `lsp.lua`, `coding.lua`; in the setup use `{ import = "plugins" }`
3. Use `return {}` for each plugin spec

### 4. Bootstrap lazy.nvim

> Goal: install lazy.nvim from `init.lua`

1. Bootstrap in `lua/config/lazy.lua`: clone lazy.nvim to `vim.fn.stdpath("data") .. "/lazy/lazy.nvim"` if missing, then `vim.opt.rtp:prepend(lazypath)`
2. Set the leader keys before loading lazy.nvim: `vim.g.mapleader = " "`, `vim.g.maplocalleader = "\\"`
3. Use `require('lazy').setup({ import = "plugins" })` or a specs table directly

### 5. Plugin Specs

> Goal: define plugin specs

1. Define plugins by URL (e.g. `github.com/user/plugin`)
2. Keep `lazy = true` as the default
3. Use `ft`, `cmd`, `keys`, `event` as lazy-loading triggers
4. Prefer an `opts` table over a `config` function (lazy.nvim merges `opts` for plugins with a `setup()`); use `config` only when custom logic is required
5. Use `dependencies` for plugin dependencies; `dev = true` + `dir` for local plugin development; pin versions with `version`/`tag`/`branch`/`commit` as needed

### 6. Performance

> Goal: improve Neovim startup performance

1. Lazy-load every plugin — group specs by usage and profile startup with `:Lazy profile`
2. Avoid loading plugins that aren't needed
3. Use `priority` for plugins that must load first
4. Commands: `:Lazy` (UI), `:Lazy install`, `:Lazy update`, `:Lazy sync`, `:Lazy clean`; troubleshoot with `:version`, `git --version`, and the `:Lazy` status

### 7. Ship

> Goal: deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Plugin Management

- Use `lazy.nvim` for plugin management
- Every plugin lazy-loads by default
- Split plugin specs into separate files under `lua/plugins/`
- Commit `lazy-lock.json` to git for a reproducible setup

### 2. Performance

- Use `ft`, `cmd`, `keys`, `event` as lazy-loading triggers
- Avoid loading unnecessary plugins
- Neovim startup time < 50ms (check with `:Lazy profile`)

- Use /follow-create-sdk if needed

## Expected Outcome

- Neovim plugins are managed with `lazy.nvim`
- Every plugin lazy-loads by default
- Plugin specs are split into files under `lua/plugins/`
- Neovim startup < 50ms
- A lockfile pins plugin versions

