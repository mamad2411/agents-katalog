---
name: lua-projects
description: >-
  Guides idiomatic Lua 5.4 programming, module design, and project maintenance
  for Neovim plugin/config ecosystems (LazyVim, lazy.nvim) and macOS bar tools
  (SketchyBar/SbarLua). Covers style, tooling (StyLua, Selene, LuaLS), module
  patterns, and testing. Use when writing Lua code, configuring Neovim plugins,
  working with SketchyBar Lua configs, debugging Lua require/module errors,
  or when the user mentions Lua, .lua files, LazyVim, lazy.nvim, SbarLua,
  SketchyBar, luarocks, LuaLS, StyLua, or Selene.
---

# Lua Projects

> **Scope**: Lua 5.4 (with LuaJIT notes where relevant). Targets config-driven
> projects like Neovim distributions, SketchyBar setups, and general Lua modules.

## Style and Formatting

### Naming

- `snake_case` for variables, functions, and file names
- `PascalCase` only for class-like constructor tables (rare)
- `UPPER_SNAKE` for true constants
- Prefix unused variables with `_` (e.g., `for _, v in ipairs(t)`)

### Indentation and Layout

- Use **2 spaces** (common in Neovim/LazyVim ecosystem) or **tabs** (SketchyBar default) -- be consistent within a project
- Wrap lines at 100 characters; hard limit 120
- Trailing commas in multi-line tables are encouraged
- No spaces inside `{}`, `()`, or `[]`; spaces after commas and around operators

### Formatter: StyLua

StyLua (v2.4+) is the standard Lua formatter. Configure via `stylua.toml` at the project root:

```toml
column_width = 100
line_endings = "Unix"
indent_type = "Spaces"
indent_width = 2
quote_style = "AutoPreferDouble"
```

For SketchyBar configs using tabs:

```toml
indent_type = "Tabs"
```

Run: `stylua .` or integrate as a pre-commit hook / editor format-on-save.

## Linting

### Selene (recommended)

Modern Lua linter written in Rust. Actively maintained (v0.30+). Provides rich diagnostics with named lint rules.

Config file `selene.toml`:

```toml
std = "lua54"
```

For Neovim configs, use the `vim` standard library definition so globals like `vim` are recognized:

```toml
std = "lua54+vim"
```

Run: `selene .`

### Luacheck (legacy)

Still detects some things Selene does not (uninitialized vars, unreachable code), but has been unmaintained since 2018. Use as a secondary pass if needed.

Config file `.luacheckrc`:

```lua
std = "lua54"
globals = { "vim" }
```

## Language Server: LuaLS

lua-language-server (`LuaLS`) provides diagnostics, completion, hover, and type checking.

Settings file `.luarc.json` at project root:

```json
{
  "runtime": { "version": "Lua 5.4" },
  "diagnostics": { "globals": ["vim"] },
  "workspace": {
    "library": [],
    "checkThirdParty": false
  }
}
```

For SketchyBar projects, add the SbarLua install path to `workspace.library` so LuaLS resolves the `sketchybar` module:

```json
"workspace": {
  "library": ["~/.local/share/sketchybar_lua"]
}
```

### Type Annotations

LuaLS supports EmmyLua-style annotations. Use them for public API surfaces:

```lua
---@param name string
---@param opts? { padding?: number, icon?: string }
---@return table item
local function add_item(name, opts)
  -- ...
end
```

## Module Patterns

### The Return-Table Pattern

Every module file should `return` a table (or a single value). Avoid polluting globals.

```lua
local M = {}

function M.greet(name)
  return "hello " .. name
end

return M
```

### Init Modules

A directory with an `init.lua` is requireable by its directory name. Use `init.lua` to re-export or orchestrate sub-modules:

```
items/
  init.lua      -- require("items") loads this
  apple.lua
  calendar.lua
```

```lua
-- items/init.lua
require("items.apple")
require("items.calendar")
```

### Avoid Globals

```lua
-- BAD: implicit global
sbar = require("sketchybar")

-- GOOD: local binding (use upvalues or pass explicitly)
local sbar = require("sketchybar")
```

Exception: SketchyBar's example config sets `sbar` as a global in `init.lua` because sub-modules reference it without an explicit require path. If following that convention, document it clearly and configure your linter to allow it:

```toml
# selene.toml
[lints]
global_usage = "allow"
```

## Project Structure Patterns

### Neovim Config (LazyVim / lazy.nvim)

```
~/.config/nvim/
  init.lua                -- minimal bootstrap: vim.loader.enable(), require("config.lazy")
  lua/
    config/
      lazy.lua            -- lazy.nvim bootstrap and setup
      options.lua
      keymaps.lua
      autocmds.lua
    plugins/
      lsp.lua
      treesitter.lua
      ui.lua
      editor.lua
```

Key conventions:
- `init.lua` stays minimal -- call `vim.loader.enable()` then require config
- One plugin spec per file (or group related specs) in `lua/plugins/`
- lazy.nvim auto-loads everything in `lua/plugins/`
- Use `opts` table merging over `config` functions when possible

Plugin spec pattern:

```lua
return {
  "author/plugin.nvim",
  event = "VeryLazy",
  dependencies = { "nvim-lua/plenary.nvim" },
  opts = {
    setting = true,
  },
  keys = {
    { "<leader>x", "<cmd>PluginAction<cr>", desc = "Do thing" },
  },
}
```

### SketchyBar Config (SbarLua)

```
~/.config/sketchybar/
  sketchybarrc              -- shell entry: sketchybar --config init.lua (or similar)
  init.lua                  -- requires sbar, wraps in begin_config/end_config, runs event_loop
  bar.lua                   -- bar-level properties
  default.lua               -- default item properties
  colors.lua                -- color palette table
  icons.lua                 -- icon constants (SF Symbols / Nerd Font)
  settings.lua              -- shared settings (paddings, fonts)
  items/
    init.lua                -- requires each item module
    spaces.lua
    front_app.lua
    media.lua
    ...
  helpers/
    init.lua
    app_icons.lua
    default_font.lua
    event_providers/        -- native helpers (C compiled)
```

Key conventions:
- Wrap all setup between `sbar.begin_config()` / `sbar.end_config()` for batching
- Always call `sbar.event_loop()` at the end of `init.lua`
- Use `sbar.exec()` instead of `os.execute()` to avoid blocking the event handler
- Properties use sub-tables instead of dot notation: `icon = { y_offset = 10 }` not `icon.y_offset`
- Color values are `0xAARRGGBB` hex integers
- Keep color/icon/settings as pure data modules that return a table

## Common Patterns

### Safe Require

```lua
local ok, mod = pcall(require, "optional_module")
if not ok then
  return
end
```

### Metatables for OOP-ish Tables

```lua
local Item = {}
Item.__index = Item

function Item.new(name)
  return setmetatable({ name = name }, Item)
end

function Item:display()
  return self.name
end
```

### Config Merging

```lua
local defaults = { padding = 4, color = 0xffffffff }

local function apply(user_opts)
  local cfg = {}
  for k, v in pairs(defaults) do cfg[k] = v end
  for k, v in pairs(user_opts or {}) do cfg[k] = v end
  return cfg
end
```

For deep merging in Neovim: `vim.tbl_deep_extend("force", defaults, user_opts)`.

## Testing

### Busted

The standard Lua test framework. Install via luarocks:

```bash
luarocks install busted
```

```lua
-- spec/greet_spec.lua
describe("greet", function()
  local mod = require("mymod")

  it("returns greeting", function()
    assert.are.equal("hello world", mod.greet("world"))
  end)

  it("handles nil", function()
    assert.has_error(function() mod.greet(nil) end)
  end)
end)
```

Run: `busted` or `busted spec/`

### Neovim Plugin Testing

Use `plenary.nvim`'s test harness for Neovim-specific tests:

```bash
nvim --headless -c "PlenaryBustedDirectory tests/ {minimal_init = 'tests/init.lua'}"
```

## Performance Notes

- `local` lookups are register-based; global lookups go through `_ENV` hash. Always localize hot-path references.
- Pre-size tables with known lengths: `local t = table.create and table.create(n) or {}`
- String concatenation in loops: accumulate in a table and `table.concat()` at the end
- Prefer `ipairs` over `pairs` when iterating sequential arrays (faster and order-guaranteed)
- In LuaJIT (Neovim): avoid NYI (Not Yet Implemented) operations in tight loops -- check <https://wiki.luajit.org/NYI>

## Lua 5.4 Specifics

Features available in 5.4 that older references may not cover:

- **Integer subtype**: integers and floats are distinct; `type(1)` is `"number"` but `math.type(1)` is `"integer"`
- **Bitwise operators**: `&`, `|`, `~` (xor), `~` (unary not), `<<`, `>>` -- no need for `bit32` or `bit` libraries
- **Integer for-loop**: `for i = 1, n` uses native integers
- **Generational GC**: `collectgarbage("generational")` for lower-latency collection
- **`<const>` and `<close>`**: local attributes for immutability and deterministic cleanup

```lua
local path <const> = "/tmp/data"
local f <close> = io.open(path, "r")
```

Note: Neovim uses LuaJIT (Lua 5.1 compatible), so 5.4 features are **not** available in Neovim configs. Use 5.4 features only in standalone Lua or SketchyBar (if built against Lua 5.4).

## Debugging

- `print(vim.inspect(t))` in Neovim for table inspection
- `print(require("inspect")(t))` in standalone Lua (install via luarocks)
- SketchyBar logs to `~/.local/share/sketchybar/` -- check there for Lua errors
- LuaLS diagnostics surface most type/require errors before runtime

## Tooling Summary

| Tool | Purpose | Config File | Install |
|------|---------|-------------|---------|
| StyLua | Formatter | `stylua.toml` | `cargo install stylua` or npm |
| Selene | Linter | `selene.toml` | `cargo install selene` |
| LuaLS | Language server | `.luarc.json` | via Mason or package manager |
| Busted | Test framework | `.busted` | `luarocks install busted` |
| Luarocks | Package manager | `*.rockspec` | system package manager |

## Reference Projects

| Project | URL | Focus |
|---------|-----|-------|
| LazyVim | <https://github.com/LazyVim/LazyVim> | Neovim distribution, plugin orchestration |
| lazy.nvim | <https://github.com/folke/lazy.nvim> | Plugin manager, spec system |
| SbarLua | <https://github.com/FelixKratz/SbarLua> | SketchyBar Lua bindings |
| SketchyBar | <https://github.com/FelixKratz/SketchyBar> | macOS bar, config examples |
| nvim-lspconfig | <https://github.com/neovim/nvim-lspconfig> | LSP client configs |
| plenary.nvim | <https://github.com/nvim-lua/plenary.nvim> | Neovim Lua utilities and test harness |
| telescope.nvim | <https://github.com/nvim-telescope/telescope.nvim> | Fuzzy finder, well-structured plugin |

## Additional Resources

- Lua 5.4 Reference Manual: <https://www.lua.org/manual/5.4/>
- Programming in Lua (4th ed): <https://www.lua.org/pil/>
- LuaRocks style guide: <https://github.com/luarocks/lua-style-guide>
- Neovim Lua guide: <https://neovim.io/doc/user/lua-guide.html>
- StyLua: <https://github.com/JohnnyMorganz/StyLua>
- Selene: <https://github.com/Kampfkarren/selene>
- LuaLS wiki: <https://luals.github.io/>
