# DOTFILES

Personal Linux (Omarchy) env via GNU Stow. Fish + Neovim + Tmux + Herdr + Ghostty + MPV.

## STRUCTURE

```
.dotfiles/
├── dot                     # CLI: stow/doctor
├── home/.agents/skills/    # Shared Agent Skills (Pi, Codex, etc.)
├── home/.config/
│   ├── nvim/               # Editor (see nvim AGENTS)
│   ├── fish/               # Shell (see fish/AGENTS.md)
│   ├── tmux/               # Prefix C-s, default shell fish
│   ├── ghostty/            # command = fish; shaders/
│   ├── herdr/              # Prefix C-;, default_shell fish
│   ├── mpv/
│   ├── git/
│   └── starship.toml
├── home/.gitconfig
└── packages/
    └── herdr-toggle-popup/  # local Herdr float popup plugin (not stowed)
```

## WHERE TO LOOK

| Task | Location |
|------|----------|
| Neovim plugin | `home/.config/nvim/lua/plugins/<name>.lua` |
| Neovim keymap | `home/.config/nvim/lua/config/keymaps.lua` |
| Neovim option | `home/.config/nvim/lua/config/options.lua` |
| Shell alias | `home/.config/fish/conf.d/aliases.fish` |
| Shell function | `home/.config/fish/functions/<name>.fish` |
| Tmux | `home/.config/tmux/tmux.conf` |
| Herdr | `home/.config/herdr/config.toml` |
| Herdr float popup plugin | `packages/herdr-toggle-popup/` |
| Ghostty | `home/.config/ghostty/config`, `home/.config/ghostty/shaders/` |
| Git | `home/.gitconfig` |
| Agent skill | `home/.agents/skills/<name>/SKILL.md` |

## CONVENTIONS

- Stow layout: `home/` mirrors `~`
- Neovim: 1 plugin per file in `lua/plugins/`, returns lazy.nvim spec
- Keymaps: navigation-first (search, def, back, splits)
- No neo-tree — use Snacks explorer
- Fuzzy: Telescope

## ANTI-PATTERNS

- Edit `~/.config/*` real files while stowed (edit through symlink / repo)
- Add shared skills under `~/.pi/agent/skills`; use `home/.agents/skills/`
- Re-adding neo-tree / oil as primary explorer without asking
- Hardcoding machine-specific absolute paths under `/Users/...` or old macOS paths
- Committing herdr logs/sockets or mpv memo history

## COMMANDS

```bash
./dot stow [part...] # all, or selected parts such as fish/agents/nvim
./dot herdr-plugin   # build/link packages/herdr-toggle-popup only
./dot add-skill <github-skill-url>
./dot remove-skill <name> # remove skill folder + matching lock entry
./dot skills-sync
./dot doctor         # tools + links + herdr float plugin
./dot unstow [part...]
```

## NVIM KEY BINDINGS (IMPORTANT)

| Key | Action |
|-----|--------|
| `<C-p>` | Find files |
| `<leader>ss` | Live grep |
| `<leader>sw` | Word under cursor (project) |
| `<C-f>` | Buffer search |
| `<leader>e` | Snacks explorer (reveal file) |
| `gd` | Definition |
| `<C-o>` | Jump back |
| `<leader>gd` / `<leader>gD` | Def in vsplit / hsplit |
| Telescope/Explorer `<C-v>` / `<C-c>` | Open in vsplit / hsplit |
| `<C-w>` / `<C-q>` | Save / save+quit |

## THEME

Tokyo Night Storm across Ghostty, Neovim, Fish, Tmux, Herdr, and Pi.
