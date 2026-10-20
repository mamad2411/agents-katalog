# AGENTS.md - Neovim Configuration

## Build/Test/Lint Commands
- **Lua formatting**: `stylua .` (uses .stylua.toml: 2 spaces, no trailing commas)
- **No traditional build/test**: This is a Neovim config, test by opening nvim and checking functionality
- **Plugin management**: `:Lazy` to manage plugins, `:Mason` for LSP tools

## Code Style Guidelines
- **Language**: Lua for all configuration files
- **Indentation**: 2 spaces (set in lua/aqua/options.lua:9-12)
- **Structure**: Modular - core in `lua/aqua/`, plugins in `lua/plugins/` and `lua/plugins.lua`
- **Plugin loading**: Use lazy.nvim patterns - `event = "VeryLazy"`, `ft = {...}`, `cmd = {...}`
- **Naming**: snake_case for files, camelCase for Lua variables/functions
- **Leader key**: Space (`" "`) for both leader and localleader
- **Comments**: Use `--` for single line, `--[[]]` for blocks
- **Error handling**: Use pcall() for risky operations, provide fallbacks
- **Imports**: Use `require()` at function scope when possible for lazy loading
- **Configuration**: Always use setup() functions in config callbacks
- **Keymaps**: Define in plugin config or lua/aqua/remaps.lua, use descriptive desc fields
- **Options**: Set vim options in lua/aqua/options.lua using vim.opt syntax
- **File organization**: Split complex plugin configs into separate files in lua/plugins/