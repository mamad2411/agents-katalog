---
name: follow-tool-nvim
description: Set up Neovim configuration with lazy.nvim following best practices
argument-hint: "[scope]"
related:
  - follow-lang-lua
  - follow-tool-formatter
  - follow-create-plugins
  - follow-test
---

## Goal

Set up a modular, lazy-loaded, maintainable Neovim configuration with `lazy.nvim`

## Scope

For creating or refactoring a Neovim config at `~/.config/nvim` or a project-specific config

- Use this skill for Neovim/`lazy.nvim` only — it doesn't cover Vim script configs or other editors (VS Code, Zed)

- Latest: Neovim `0.12.5`, lazy.nvim `11.17.5` (verified 2026-09-13)
- Neovim 0.12+ ships `vim.pack` as a built-in plugin manager — consider it instead of lazy.nvim when a minimal config is wanted

## Execute

### 1. Install Neovim

> Goal: install Neovim before configuring lazy.nvim

1. Install Neovim >= 0.8.0 (built with LuaJIT):
   - Windows: download from [Neovim releases](https://github.com/neovim/neovim/releases) or `scoop install neovim`
   - macOS: `brew install neovim`
   - Linux: `sudo apt install neovim` or `sudo pacman -S neovim`
   - mise: `mise use -g neovim` (if using mise)
2. Install Git >= 2.19.0 (lazy.nvim uses partial clones)
3. Verify `nvim --version` before continuing
4. See details in 

### 2. Bootstrap lazy.nvim

> Goal: install the lazy.nvim plugin manager

1. Create `init.lua` at `~/.config/nvim/init.lua`
2. Create `lua/config/lazy.lua` to clone the stable branch of `lazy.nvim`
3. Use `require("config.lazy")` in `init.lua`
4. Run `:checkhealth lazy` to verify
5. See details in 

### 3. Structure Config

> Goal: split config files by responsibility

1. Create `lua/core/options.lua` for `vim.opt`
2. Create `lua/core/keymaps.lua` for keymaps
3. Create `lua/core/autocmds.lua` for autocommands
4. Create `lua/plugins/*.lua` for plugin specs
5. See details in 

### 4. Add Plugins

> Goal: add plugins with lazy loading

1. Use `lazy = true` as the default
2. Use `ft`, `cmd`, `keys`, `event` for lazy-loading
3. Use `dependencies` for plugin dependencies
4. Use `version`, `tag`, `branch`, or `commit` to pin versions
5. See details in 

### 5. Configure LSP and Formatting

> Goal: configure LSP, formatter, and linting

1. Use `vim.lsp.config` / `vim.lsp.enable` (Neovim ≥0.11) with `nvim-lspconfig` and `mason.nvim`
2. Use `conform.nvim` for formatting and `nvim-lint` for linting (null-ls is archived — don't use it)
3. Configure auto format on save via an autocommand
4. Use `stylua` to format Lua
5. See details in 

### 6. Add Tests

> Goal: write tests for utility functions

1. Install `plenary.nvim`
2. Create `tests/utils_spec.lua` for unit tests
3. Run `:PlenaryBustedFile %` or `:PlenaryBustedDirectory tests/`
4. See details in 

### 7. CI and Quality

> Goal: configure automated checks

1. Use GitHub Actions to run `stylua --check .`
2. Run Plenary tests with `nvim --headless -c "PlenaryBustedDirectory tests/ { minimal_init = 'init.lua' }"`
3. Keep startup time under 50ms
4. See details in 

## Rules

### 1. Structure

- `init.lua` only bootstraps `lazy.nvim`
- Split `options.lua`, `keymaps.lua`, `autocmds.lua`, and plugins into sub-files
- Every plugin lazy-loads, except the colorscheme that must load on startup

### 2. Performance

- Use `ft`, `cmd`, `keys`, `event` to lazy load
- Check startup time with `vim-startuptime` or `:StartupTime`
- Target startup time < 50ms

### 3. Code Quality

- Use `stylua` to format Lua
- Use `plenary.nvim` to write unit tests for utilities
- Add `desc` to every keymap for `which-key`

### 4. Maintenance

- Pin plugin versions when stability is needed
- Update plugins via `:Lazy update`
- Review `lazy-lock.json` after updates

- Use /follow-lang-lua if needed
- Use /follow-tool-formatter if needed
- Use /follow-create-plugins (nvim) if needed
- Use /follow-test if needed

## References

- [CLI reference](references/cli.md)


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- A modular, easy-to-maintain Neovim config
- Every plugin lazy-loads by default
- LSP, formatter, and linter working
- Unit tests for utilities runnable
- CI checks format and tests automatically

