# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal Arch Linux dotfiles repo. It is not a library or app — there is no build, lint, or test suite. Most files are configuration that gets symlinked into `$HOME` (or `/etc`) by `setup.sh`. The handful of "code" lives in `bin/` (bash + Python utility scripts), `config/xmonad/` (Haskell), and `config/nvim/init.vim`.

## The setup.sh model

`setup.sh` is the single entrypoint and the source of truth for what this repo *does*. Read it before adding anything that needs installation or linking.

- `install_everything` calls a tree of `setup_*` functions. Each one is idempotent: it installs packages via `ensure_packages_exist` / `ensure_aur_packages_exist`, then symlinks config via `link_dotfile` / `link_etc_dotfile`.
- `link_dotfile foo/bar` symlinks `$HOME/.foo/bar` → `$DOTFILES_DIR/foo/bar`. That convention is why top-level paths look like `config/`, `gnupg/`, `ssh/`, etc. — they map to `~/.config/`, `~/.gnupg/`, `~/.ssh/`.
- `link_etc_dotfile foo/bar` symlinks `/etc/foo/bar` → `$DOTFILES_DIR/etc/foo/bar` (needs sudo). Anything under `etc/` is system-level.
- When adding a new config file or script: add or extend the appropriate `setup_*` function so it's installed and linked, then wire that function into the right `setup_*` group if it's not already called transitively.
- The script assumes Arch with `pacman` and `yay`. Don't add cross-distro abstractions — it's explicitly a personal setup.
- `set -euo pipefail` is on; commands must tolerate it.

## Component layout

- `bin/` — personal scripts on `$PATH` (the directory is symlinked to `~/bin`). Mostly bash, a few Python. Dependencies for each script are declared as `ensure_packages_exist` calls in `setup_bin_dir` with a comment naming the script — keep that pattern when adding scripts.
- `config/xmonad/` — Haskell XMonad config built with `stack`. The three submodules under `xmonad-libs/` (singlespacing, contexts, pseudotiling) are vendored XMonad libraries linked in via `config/xmonad/lib/XMonad/`. Rebuild with `xmonad --recompile` (the binary lands in `~/.cache/xmonad/` and `bin/xmonad` is a symlink to it).
- `config/nvim/init.vim` — Neovim config using vim-plug. Plugins are grouped by load-time cost (fast / slow / very slow) — preserve that grouping if adding plugins. LSP servers, formatters, linters, and tree-sitter CLI are installed via `setup_neovim` in `setup.sh`, not via Mason.
- `config/systemd/user/` — user-level systemd units (backup, reminder, tad, watchdog, background, git-maintenance). These reference scripts in `bin/`, so changes to a script may affect a timer.
- `etc/` — system-level configs (pacman, NetworkManager dispatcher, udev rules, security/limits, sysctl, X11 keyboard). Linked into `/etc` via `link_etc_dotfile`.
- Top-level shell files: `profile` (env), `bashrc` / `zshrc` (interactive), `shellrc` (shared shell-agnostic settings), `aliases`. `zprofile` is a symlink to `profile`. Zsh uses prezto.

## Color scheme

base16-mocha is defined in many places independently (see `README.md` for the full list: `colors`, `Xresources`, alacritty, dunst, rofi, xmobar, xmonad.hs, nvim, spacemacs, dzen, i3lock). If you change colors, change them everywhere consistently — there is no central source.

## Submodules

`xmonad-libs/{singlespacing,contexts,pseudotiling}` are git submodules pointing at sibling repos (`../xmonad-*`). `setup.sh`'s update path runs `git submodule update --init --recursive` after pulling.
