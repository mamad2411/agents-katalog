---
name: nvim-config
description: >
  Reference and editing guide for Floris’s Neovim config (NvChad-based) at
  %LOCALAPPDATA%/nvim (C:\Users\floris\AppData\Local\nvim). Covers directory
  layout, init bootstrap order, chadrc theme, plugins, mappings, options, LSP
  servers, conform formatters, render-markdown for .md/.mdx, and Alacritty
  ConPTY XTGETTCAP startup junk (+q4D73) via configs/term_junk.lua. Use when
  the user runs /nvim-config, or asks about nvim config, Neovim setup, NvChad,
  lua/configs/lsp, lsp-servers, conform, mappings, chadrc, lazy.nvim plugins,
  render-markdown, markdown render, term_junk, Alacritty +q junk, or editing
  this nvim dotfiles repo.
---

# Neovim config (NvChad) — agent guide

## Location (source of truth)

| Path | Role |
|------|------|
| `C:\Users\floris\AppData\Local\nvim` | Config root (`stdpath("config")` on Windows) |
| `%LOCALAPPDATA%\nvim` | Same path |

This directory **is** the git repo. Edit here. Do not invent `~/.config/nvim` unless the user is on WSL and says so.

**Do not commit** runtime data:

| stdpath | Typical contents |
|---------|------------------|
| `data` | lazy plugins, mason, treesitter parsers |
| `state` | shada, logs (`render-markdown.log`, etc.) |
| `cache` | base46 under `vim.g.base46_cache` |

## Environment

| Piece | Value / notes |
|-------|----------------|
| Neovim | **0.12.x** (config uses `vim.lsp.config` / `vim.lsp.enable`) |
| Framework | **NvChad v2.5** (`import = "nvchad.plugins"`) |
| Plugin manager | **lazy.nvim** |
| Theme | base46 via `lua/chadrc.lua` — currently `"github_light"` |
| Terminal | **Alacritty 0.17+** on Windows |
| Shell | often **nu.exe** (Alacritty `[terminal.shell]`) |
| Font | **JetBrainsMono Nerd Font Mono** (required for icons / render-markdown) |
| `TERM` | `xterm-256color` (Alacritty `[env]`) |
| Nvim binary | `C:\Program Files\Neovim\bin\nvim.exe` |

## Layout

```
init.lua                      # term_junk FIRST, then lazy, theme, options, autocmds, mappings
lua/
  chadrc.lua                  # NvChad base46 theme + hl overrides
  options.lua                 # folds, ttimeout
  mappings.lua                # Telescope, conform, render-markdown globals
  autocmds.lua                # mdx filetype + markdown buffer local opts/maps
  configs/
    term_junk.lua             # XTGETTCAP +q4D73 scrub + Win32 clipboard (early)
    lazy.lua                  # lazy defaults / disabled stock rtp plugins
    lsp-servers.lua           # server name list (single source of truth)
    lspconfig.lua             # per-server settings + vim.lsp.enable
    conform.lua               # formatters_by_ft + mason tools list
    render-markdown.lua       # in-buffer md/mdx render opts
  plugins/
    init.lua                  # user plugin specs only
README.md
lazy-lock.json
```

## Bootstrap order (`init.lua`) — critical

Order matters. Do **not** move `term_junk` after plugins.

1. `vim.g.base46_cache`, `mapleader = " "`
2. **`require "configs.term_junk"`** → `setup_clipboard()` + `start()`  
   (must be **before** `lazy.setup` so UIEnter handlers exist early)
3. Bootstrap / prepend lazy.nvim
4. `lazy.setup({ NvChad, { import = "plugins" } }, lazy_config)`
5. `dofile` base46 `defaults` + `statusline` cache
6. `require "options"`, `require "autocmds"`
7. `vim.schedule` → `require "mappings"`

When adding plugins: edit **`lua/plugins/init.lua` only** (user layer).

## Theme / UI

- `lua/chadrc.lua` → `M.base46.theme` (`"github_light"`)
- Comment / `@comment` color overrides in same file
- Theme cache rebuild: restart or `:Lazy reload base46` if highlights look stale

## Options (`lua/options.lua`)

On top of NvChad defaults:

- Folds: `foldmethod=indent`, `foldenable`, high `foldlevel` / `foldlevelstart`
- `ttimeout` + `ttimeoutlen=50` — shorter keycode timeout for CSI/DCS on ConPTY

## Mappings (`lua/mappings.lua`)

Leader = **space**.

| Keys | Action |
|------|--------|
| `;` | Command mode (`:`) |
| `jk` (insert) | Escape |
| `<leader>ff` | Telescope find files |
| `<leader>fg` | Telescope live grep |
| `<leader>fb` | Telescope buffers |
| `<leader>fh` | Telescope help |
| `<C-t>` | Find files |
| `<S-t>` | Live grep |
| `<leader>fm` | Conform format buffer |
| `<leader>mR` | Toggle markdown render (global) |
| `<leader>mp` | Markdown side preview |
| `<leader>mE` / `<leader>mD` | Enable / disable markdown render (global) |
| `<leader>mr` | Toggle render (buffer; set on md/mdx FileType) |
| `<leader>md` | render-markdown debug current line (md/mdx) |

NvChad stock maps still apply.

## Plugins (`lua/plugins/init.lua`)

| Plugin | Notes |
|--------|--------|
| `stevearc/conform.nvim` | Format on `BufWritePre`; opts from `configs.conform` |
| `nvim-telescope/telescope.nvim` | `cmd = Telescope`; rg for find_files |
| `mason-org/mason-lspconfig.nvim` | `ensure_installed` from `lsp-servers`; **`automatic_enable = false`** |
| `WhoIsSethDaniel/mason-tool-installer.nvim` | installs `conform.tools` |
| `neovim/nvim-lspconfig` | `require "configs.lspconfig"` |
| `nvim-treesitter/nvim-treesitter` | branch **main**; `require("nvim-treesitter").install { ... }` |
| `MeanderingProgrammer/render-markdown.nvim` | `ft` markdown/mdx/quarto/rmd; opts from `configs.render-markdown` |

### Treesitter languages installed

`python`, `yaml`, `json`, `lua`, `javascript`, `typescript`, `tsx`, `html`, `css`, **`markdown`**, **`markdown_inline`**.

### MDX

- `vim.filetype.add { extension = { mdx = "mdx" } }` in `autocmds.lua`
- `vim.treesitter.language.register("markdown", "mdx")` in treesitter plugin config
- render-markdown `file_types` includes `mdx`

## LSP

**List (only here):** `lua/configs/lsp-servers.lua`

```
lua_ls, rust_analyzer, pyright, taplo, jsonls, ts_ls, cssls, html, yamlls, sqls
```

**Wire-up:** `lua/configs/lspconfig.lua`

1. `require("nvchad.configs.lspconfig").defaults()`
2. Custom `vim.lsp.config("rust_analyzer", …)` — all-features, clippy, proc macros, binding-mode inlay hints
3. Custom `vim.lsp.config("pyright", …)` — `diagnosticMode = "openFilesOnly"`
4. `vim.lsp.enable(servers)` for the full list

Mason installs the same names; it does **not** auto-enable.

**Add a server:** append to `lsp-servers.lua` → optional `vim.lsp.config` → restart / open matching buffer.

## Formatting (conform)

`lua/configs/conform.lua` — format on save (`timeout_ms = 1000`).

| Filetype | Formatter |
|----------|-----------|
| lua | stylua |
| rust | rustfmt (+ LSP fallback) |
| python | ruff_format (+ LSP fallback) |
| toml | taplo |
| json, jsonc, js, jsx, ts, tsx, css | biome, then prettierd |
| scss, html, yaml, markdown, mdx | prettierd |
| sql | sqlfluff (+ LSP fallback) |

`options.tools` = stylua, ruff, taplo, biome, prettierd, sqlfluff (for mason-tool-installer).  
Manual format: `<leader>fm`.

## Markdown / MDX in-buffer rendering

| Piece | Path / value |
|-------|----------------|
| Plugin | `MeanderingProgrammer/render-markdown.nvim` |
| Opts | `lua/configs/render-markdown.lua` |
| Buffer setup | `lua/autocmds.lua` FileType markdown/mdx |

Behavior:

- In-buffer render (not browser): headings, **pipe tables**, fenced code + language icons, bullets, checkboxes, callouts, links, HR, quotes, yaml frontmatter
- `render_modes = { "n", "c", "t" }` — raw source in insert
- `file_types = { "markdown", "mdx" }`, `restart_highlighter = true`
- Buffer: wrap, linebreak, breakindent, conceallevel; maps `<leader>mr` / `<leader>md`
- Commands: `:RenderMarkdown`, toggle, preview, debug, get
- Needs Nerd Font + TS parsers `markdown` + `markdown_inline`

Do not switch to browser-only preview as default unless the user asks.

## Alacritty startup junk (`+q4D73`) — `configs/term_junk.lua`

### Symptom

Opening nvim in Alacritty injects text like `+q4D73` or ` +q4D73` into a buffer.

### Cause

Neovim TUI sends **XTGETTCAP** (DCS) queries. Capability **`Ms`** (clipboard / OSC 52) is hex **`4D73`**. Windows **ConPTY** + Alacritty often mishandles the reply, so fragments are typed as input.

### Implementation (do not regress)

| API | Role |
|-----|------|
| `setup_clipboard()` | Win32 `clip.exe` + PowerShell paste; set `vim.g.clipboard` early |
| `start()` | Timed scrubs (0–4000 ms) + autocmds on UIEnter/VimEnter/BufEnter/TextChanged* |
| `scrub_all()` | Walk loaded `buftype=""` buffers; strip tokens matching `+q` + hex digits |

**Matching rules (bugs already fixed once — keep them):**

- Detect with **plain** find: `line:find("+q", 1, true)` — **not** `find("%+q", 1, true)` (that searches literal `%+q` and never matches).
- Remove with **pattern** gsub: `"%+q[%x]+"` then trim surrounding spaces.
- If the buffer was only junk/whitespace, set `modified = false`.

**Load site:** top of `init.lua` before lazy — **not** only in `autocmds.lua`.

**Manual clear:**

```vim
:lua require("configs.term_junk").scrub_all()
```

**If junk returns after edits:**

1. Confirm term_junk is still first after mapleader in `init.lua`
2. Confirm plain `"+q"` find (not `"%+q"` with plain flag)
3. Fully quit all nvim instances and reopen
4. Optional long-term: newer ConPTY / Alacritty; `conpty.dll` next to nvim.exe per Neovim Windows docs

## Safe edit patterns for agents

1. Prefer `lua/plugins/init.lua`, `lua/configs/*`, `mappings.lua`, `options.lua`, `autocmds.lua`, `chadrc.lua`, `init.lua` (bootstrap only carefully).
2. **One** LSP list: `lsp-servers.lua` only.
3. Keep term_junk **before** lazy; do not “simplify” scrub with plain `"%+q"` finds.
4. After plugin changes: user opens nvim once; `lazy-lock.json` updates.
5. Do not commit `stdpath("data"|"state"|"cache")`.
6. Windows paths + PowerShell/nu — no bash-only scripts unless asked.
7. Markdown: keep in-buffer render-markdown + TS parsers; prettierd for md/mdx format.
8. Alacritty config lives outside repo: `%APPDATA%\alacritty\alacritty.toml`.

## Quick diagnostics

| Check | Action |
|-------|--------|
| LSP | `:LspInfo` |
| Formatters | `:ConformInfo` |
| Mason | `:Mason` |
| Markdown render | `:RenderMarkdown get` / `<leader>md` |
| Treesitter | `:checkhealth nvim-treesitter` |
| render-markdown | `:checkhealth render-markdown` |
| Startup junk | bare `nvim` in Alacritty; buffer should clear; or `:lua require("configs.term_junk").scrub_all()` |

## Open these files first

| Task | Files |
|------|--------|
| New LSP | `configs/lsp-servers.lua`, `configs/lspconfig.lua` |
| New formatter | `configs/conform.lua` |
| New plugin | `plugins/init.lua` |
| Keymap | `mappings.lua` |
| Theme | `chadrc.lua` |
| Markdown look | `configs/render-markdown.lua`, `autocmds.lua` |
| Terminal `+q` junk | `configs/term_junk.lua`, `init.lua` (load order), `options.lua` (ttimeout) |
| Bootstrap / load order | `init.lua` |

## References

- `references/layout.md` — compact path map
