---
name: helix-themes
description: >-
  Port design-system palettes (especially darkmatter/prelude themes.nix) into
  Helix editor themes and wire them through Cooper's nix-darwin/home-manager
  Helix module. Use when adding/updating Helix colorschemes, porting Prelude
  (or similar token palettes) to Helix TOML, changing theme = in helix config,
  or installing themes under ~/.config/helix/themes via ~/darwin.
---

# Helix themes (Prelude + darwin)

## When to use

- User asks to port **prelude** / palette themes to **Helix**
- Edit Helix colors, `theme = "…"`, or `files/helix/themes/`
- Wire new themes into home-manager so they survive rebuilds

## Source of truth

| What | Where |
|------|--------|
| Prelude semantic palettes | `~/git/darkmatter/prelude/src/prelude/themes.nix` |
| Helix theme TOMLs (managed) | `~/darwin/files/helix/themes/` |
| Helix HM module | `~/darwin/modules~/helix.nix` |
| Live user themes | `~/.config/helix/themes/` (often mix of nix-store symlinks + writable copies) |
| Active config | `~/.config/helix/config.toml` (usually a HM symlink) |

Existing hand-tuned themes (do **not** overwrite casually):

- `apathy.toml`, `apathy-minted.toml` — richer syntax maps than the semantic Prelude ports

## Naming

- Prefix Prelude ports **`prelude-<name>`** (e.g. `prelude-nord`, `prelude-phosphor`).
- Bare names like `nord` / `gruvbox` / `solarized` **collide with Helix built-ins** under the default runtime.
- Keep `apathy` / `apathy-minted` as the historical non-prefixed names unless the user renames them.

## Port workflow

1. **Read palettes** from `themes.nix` (tokens: `bg`, `surface`, `secondary`, `fg`, `muted`, `dim`, `border`, `accentBorder`, `accent`, `accent2`, `success`, `warning`, `info`, `error`, `selectionFg`).
2. **Generate** Helix TOML under `~/darwin/files/helix/themes/prelude-<name>.toml`:
   - UI + syntax scopes map onto those tokens (see `templates/prelude-theme.toml`).
   - Derive UI-only colors from tokens (don't invent unrelated hues):
     - dark themes: `gutter` = darken(`bg`); `panel` = mix(`bg`,`surface`); `cursorline` = mix(`bg`,`secondary`); `selection` ≈ `secondary`; `search` = mix(`surface`,`accent2`); `invisible` = mix(`bg`,`dim`)
     - **light** themes (`paper`): invert darken/lighten direction
     - **prelude brand**: `secondary` is a mid chrome gray — do **not** use it as selection fill; mix `surface`+`accent` instead
3. **Wire HM** in `helix.nix`:
   - Keep a `preludeThemes = [ "prelude-…" … ];` list
   - Install via `xdg.configFile // lib.listToAttrs (map … preludeThemes)` — **one** merged `xdg.configFile` attrset (duplicate top-level `xdg.configFile =` keys are a footgun)
   - Add the same names to `randomThemes` if `helix-random` should pick them
4. **Live install** for immediate use without full rebuild:
   - `~/.config/helix/themes/` is usually a **real directory** with store **symlinks** for HM files — you can `cp -f` new `prelude-*.toml` alongside them
   - Config `theme =` itself is often a store symlink; changing default theme requires editing `helix.nix` + rebuild (or a one-off temp `-c` config)
5. **Validate** (see `scripts/verify-prelude-helix-themes.sh`):
   - Every `fg`/`bg`/`color` palette ref resolves
   - Hex anchors match `themes.nix` for `bg`/`accent`/`fg`/etc.
   - `nix-instantiate --parse` on `helix.nix`
   - Load each theme: temp `XDG_CONFIG_HOME`, `theme = "prelude-…"`, `printf ':q\n' | timeout 2 hx …`, no theme errors in helix log

## Semantic → Helix role map (Prelude ports)

| Token | Typical Helix use |
|-------|-------------------|
| `bg` | `ui.background`, statusline fg on accent modes (`selection_fg`) |
| `surface` / `panel` | popups, bufferline active, statusline bg |
| `secondary` | selection (except brand `prelude`) |
| `fg` | default text, variables |
| `muted` / `dim` | comments, linenr, punctuation, inactive UI |
| `accent` | functions, headings, menu selected bg, insert-adjacent chrome |
| `accent2` | types, operators, constructors, jump labels |
| `success` | strings, diff plus |
| `warning` | regex, diagnostics warning, diff delta |
| `info` | keywords, constants, links, directories |
| `error` | errors, diff minus |
| `selectionFg` | text on accent/status mode backgrounds |

Hand-tuned `apathy*.toml` may keep a larger bespoke palette; Prelude ports stay on the compact semantic set.

## Pitfalls

- **Built-in name collision** — always `prelude-` prefix for ports of nord/gruvbox/solarized/etc.
- **Don't clobber** `apathy.toml` / `apathy-minted.toml` when bulk-generating Prelude ports.
- **Single `xdg.configFile` merge** — use `//` with `listToAttrs`; multiple `xdg.configFile =` assignments in one module fight each other.
- **Brand `prelude.secondary`** is not a dark surface; bad selection contrast if used raw.
- **HM rebuild** replaces only managed symlinks; loose `cp`'d themes stay until removed — still add sources under `~/darwin/files/…` so rebuilds install them.
- **Verification**: `hx --health` does **not** deeply validate theme scope refs — use open+`:q` under isolated `XDG_CONFIG_HOME` and check the log / palette ref script.

## Related files

- `templates/prelude-theme.toml` — scope skeleton (substitute palette)
- `references/prelude-token-map.md` — token notes + known theme list
- `scripts/verify-prelude-helix-themes.sh` — presence, anchors, load check
