# FISH SHELL CONFIG

Layered: `config.fish` → `conf.d/*.fish` (auto) → `functions/*.fish` (lazy)

## STRUCTURE

```
fish/
├── config.fish
├── conf.d/          # auto-sourced fragments
├── functions/       # lazy-loaded (1 function per file)
└── completions/
```

## WHERE TO LOOK

| Task | Location |
|------|----------|
| Alias | `conf.d/aliases.fish` |
| PATH | `conf.d/paths.fish` |
| Function | `functions/<name>.fish` |
| Git abbrs | `functions/__git.init.fish` via `conf.d/git.fish` |
| Tool init | `conf.d/<tool>.fish` |

## CONVENTIONS

- Functions use `-d "description"`
- Private helpers prefix `__`
- Prefer `fish_add_path` over hand-rolled PATH
- Use `set -gx` for exports
- Keep `config.fish` minimal

## KEY ALIASES / COMMANDS

| Name | Meaning |
|------|---------|
| `n`/`vim`/`vi` | nvim (cwd if no args) |
| `p` | pi |
| `op` | opencode --port |
| `t` | tmux attach/new |
| `ff`/`fvim`/`eff` | fzf helpers |
| `g`/`gst`/… | git + abbrs from `__git.init` |
| `skill-add` | Vendor/lock upstream skills (`./dot add-skill`) |
| `aiup` / `agents-upgrade` | Upgrade mise coding agents with fresh metadata and no release-age delay (`--dry-run` to preview) |
| `agents-prune` | Remove unused mise coding-agent versions only (`--dry-run` to preview; restart old sessions first) |

## NOTES

- Omarchy bash defaults are reimplemented lightly here (eza, zoxide, mise, starship)
- System login shell may still be bash until `chsh`; ghostty/herdr force fish
