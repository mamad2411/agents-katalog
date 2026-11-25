# Niri Configuration

The daily-driver Wayland compositor (see `~/.config/CLAUDE.md`).

## Files

- `config.kdl` — rendered from a chezmoi **template** (`dot_config/niri/config.kdl.tmpl`). **Edit the template, never the rendered file.** Niri live-reloads on change, but silently keeps the old state if the new config is invalid — always run `niri validate` after applying.
- `scripts/` — chezmoi-managed helper scripts (source files use the `executable_` prefix, e.g. `dot_config/niri/scripts/executable_toggle_opacity.sh`).
- `launcher-ignore` — gitignore-syntax exclusions for the `Mod+Space` launcher's document sweep, handed straight to `fd --ignore-file`. Yours to edit; the script adds no exclusions of its own.

## Launcher (`Mod+Space`)

`scripts/launch_menu.py` is a merged picker — applications, PDFs, and Obsidian notes in one `fuzzel --dmenu` list (~10,900 rows, ~70ms to build). `Mod+Shift+Space` is the plain-fuzzel app-launcher escape valve; `Mod+Z` (full-`$HOME` PDF sweep) and `Mod+B` (bibliography) are unchanged.

Things worth knowing before editing it:

- **Rows are `payload <TAB> display <TAB> keywords \0icon\x1f<name>`.** fuzzel shows column 2, matches columns 2–3, returns column 1. The rofi icon protocol composes with the column flags because the icon marker is a NUL-terminated suffix — so entries keep real themed icons.
- **Sorting is fuzzel's**, with the `--cache` frecency counter as a tiebreaker. That cache is keyed on the **display column**, not the payload, so column 2 must stay stable across runs. It is seeded once from `~/.cache/fuzzel` (which fuzzel keys by desktop-file id) and thereafter owned by fuzzel.
- **`gio launch` cannot start `Terminal=true` entries** (htop, nvim, ranger, ipython, R). GLib searches a hardcoded terminal list containing none of kitty/foot/wezterm, and xterm is not installed. Those entries are routed to kitty explicitly.
- **Reference rows come from `~/Dropbox/references/refmenu.sh --print-rows`**, cached at `~/.cache/niri-launcher/refs.tsv` against `references.bib`'s mtime so `uv` never runs on the hot path. That script is *not* chezmoi-managed (it lives in its own git repo in Dropbox), so the launcher degrades gracefully when it is absent.
- **The document sweep passes `--no-ignore-vcs`.** A `.gitignore` is the wrong authority for a document search: project repos ignore `figures/`, `tables/`, `output/` and `logs/` because those PDFs are *generated*, and omitting the flag hides ~1,500 of them. It is narrower than the blanket `--no-ignore` in `Mod+Z` — `.ignore`/`.fdignore` and `launcher-ignore` all still apply.
- Sigils `@app` / `@doc` / `@ref` / `@note` sit in the hidden keyword column; `--match-mode=exact` tokenises on whitespace, so `@app k` narrows to applications.
- Test without opening a picker: `scripts/launch_menu.py --print-rows` and `scripts/launch_menu.py --dispatch '<payload>'`.

## Terminal integration

- `Mod+Return` spawns **kitty** (the primary terminal; the wezterm bind was removed July 2026).
- `Mod+Shift+T` runs `scripts/toggle_opacity.sh`, toggling background opacity for **both** wezterm (state file at `$XDG_RUNTIME_DIR/wezterm-opacity-toggle`) and kitty (per-process remote-control sockets). Sway parity: same binding exists there, but sway's own script only handles wezterm.
- Window rules exist in wezterm/kitty pairs (focus ring drawn around the translucent surface; inactive windows faded to 0.95). When adding a rule for one terminal, mirror it for the other.
