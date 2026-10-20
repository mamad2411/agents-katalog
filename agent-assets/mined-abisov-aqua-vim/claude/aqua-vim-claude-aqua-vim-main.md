# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Configuration Structure

This is a Neovim configuration using the lazy.nvim plugin manager with a modular architecture:

- `init.lua` - Main entry point that bootstraps lazy.nvim and loads core modules
- `lua/aqua/` - Core configuration modules (globals, options, remaps)
- `lua/plugins.lua` - Main plugin definitions and configurations
- `lua/plugins/` - Specialized plugin configurations split into separate files
- `ftplugin/` - Filetype-specific configurations (go.lua, java.lua)

## Plugin Management

Uses lazy.nvim with lazy loading strategies:
- Most plugins load on `VeryLazy` event for performance
- Language-specific plugins use filetype loading (`ft = {...}`)
- Command-triggered plugins use `cmd = {...}`
- Plugins are split between `lua/plugins.lua` (main definitions) and `lua/plugins/*.lua` (complex configurations)

## Key Configuration Patterns

**Leader Key**: Space (`" "`) is set as both leader and localleader

**Code Formatting & Linting**:
- conform.nvim handles formatting with language-specific formatters
- nvim-lint provides linting with eslint_d, ktlint, tflint
- Format with `<leader>l`, lint with `<leader>ll`

**LSP Configuration**:
- Uses lsp-zero.nvim for simplified LSP setup
- Mason manages LSP servers, formatters, and linters
- Standard LSP keybindings: `gd` (definition), `gr` (references), `K` (hover)

**Testing**:
- neotest.nvim for test running with adapters for Jest, RSpec, Minitest, Elixir, Go
- Test keybindings: `<leader>t` (run test), `<leader>tf` (run file), `<leader>td` (run directory)

**Debugging**:
- nvim-dap with language-specific configurations
- Debug keybindings: `<leader>dt` (start), `<leader>b` (toggle breakpoint)

## Common Development Commands

**Plugin Management**:
- `:Lazy` - Open plugin manager
- `:Mason` - Manage LSP servers and tools

**File Navigation**:
- `<leader>ff` - Find files (Telescope)
- `<leader>fg` - Live grep with args
- `<leader>fb` - Find buffers
- `-` - Open Oil file browser in float

**Testing**:
- `<leader>t` - Run current test
- `<leader>tf` - Run all tests in current file
- `<leader>tp` - Toggle test output panel

**Git Integration**:
- `<leader>gs` - Open Fugitive
- `<leader>lg` - Open LazyGit
- Gitsigns for comprehensive git hunk management (see Git Operations section)
- Diffview for advanced diff visualization and merge conflict resolution
- Octo.nvim for GitHub integration (`:Octo`)

## Git Operations

**Gitsigns (lua/plugins/gitsigns.lua)**:
- Hunk navigation: `]c` (next), `[c` (previous)
- Hunk actions: `<leader>ghs` (stage), `<leader>ghr` (reset), `<leader>ghp` (preview)
- Buffer actions: `<leader>ghS` (stage all), `<leader>ghR` (reset all), `<leader>ghu` (undo stage)
- Blame: `<leader>ghb` (full), `<leader>ghB` (summary), `<leader>gtb` (toggle line blame)
- Diff: `<leader>ghd` (diff this), `<leader>ghD` (diff cached), `<leader>gq` (exit diff cleanly)
- Toggles: `<leader>gts` (signs), `<leader>gtn` (number highlight), `<leader>gtl` (line highlight), `<leader>gtw` (word diff), `<leader>gtd` (deleted lines)
- Text object: `ih` (select hunk)

**Diffview (lua/plugins/diffview.lua)**:
- `<leader>gdo` - Open Diffview (compare working tree with index)
- `<leader>gdc` - Close Diffview
- `<leader>gdh` - Open file history view
- `<leader>gdr` - Refresh Diffview
- `<leader>gdt` - Toggle file panel
- File panel navigation: `j/k` (move), `<CR>/o` (open diff), `-` (stage/unstage)
- Merge conflict resolution: `<leader>co` (ours), `<leader>ct` (theirs), `<leader>cb` (base), `<leader>ca` (all), `dx` (delete)
- Layout cycling: `g<C-x>` (cycle through diff layouts)

## Language-Specific Features

**Supported Languages**: JavaScript/TypeScript, Lua, Go, Java/Kotlin, Ruby, Rust, Elixir, Terraform

**Code Completion**: nvim-cmp with LSP, buffer, path, and snippet sources

**Treesitter**: Configured for syntax highlighting, indentation, and text objects with custom keybindings for function/class navigation

## Dependencies

**Required External Tools**:
- ImageMagick (for image.nvim plugin)
- Node.js/npm (for JavaScript/TypeScript tools)
- Language-specific tooling (go, rustc, java, etc.)

**Notable Integrations**:
- Obsidian vault integration (obsidian.nvim)
- Tmux navigation (vim-tmux-navigator equivalent)
- GitHub integration (octo.nvim)
- AI coding assistance (codecompanion.nvim with Ollama)

## Custom Configurations

**Appearance**: Uses tokyonight theme with transparency, custom illuminate highlighting

**Terminal**: FloatTerm for floating terminals (`<leader>ft`)

**Productivity**: Harpoon for quick file switching, marks.nvim for bookmarks, Flash for quick navigation

## Documentation

- `docs/git-workflow.md` - Comprehensive guide for using gitsigns and diffview features