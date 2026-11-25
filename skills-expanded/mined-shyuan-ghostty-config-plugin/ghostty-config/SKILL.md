---
name: ghostty-config
description: >
  Use when configuring, troubleshooting, or exploring Ghostty terminal
  settings, themes, fonts, keybindings, colors, opacity, scrollback,
  or any Ghostty config option
---

# Ghostty Config Management

## The Iron Law

```
ALWAYS CHECK DOCS VIA MCP TOOL BEFORE GIVING CONFIG ADVICE.
NEVER ASSUME A VALUE'S TYPE, UNIT, OR BEHAVIOR FROM ITS NAME.
```

## Config File Location

- **macOS**: `~/Library/Application Support/com.mitchellh.ghostty/config`
  - This path takes priority over XDG. Both can coexist, macOS path wins.
- **Linux**: `${XDG_CONFIG_HOME:-~/.config}/ghostty/config`

The config is a plain text file named `config` (no extension) inside the directory.

## Config Syntax

- `key = value` — spaces around `=` optional
- `#` comments **only at line start** — `font-size = 14 # comment` is WRONG, `# comment` becomes part of the value
- Empty value resets to default: `font-size =`
- Multi-value: repeat the key (e.g. `font-family` for fallback chain)
- Clear then set: `font-family = ""` then `font-family = NewFont`
- `keybind =` (empty) **removes ALL keybinds including defaults** — this does NOT reset to defaults
- Use `ctrl+slash` not `ctrl+/` in keybinds — `/` is parsed as key table separator

## Core Workflow: Changing Any Config Option

1. `ghostty_get_config_option` → read full docs for the option
2. Check the **value type and unit** — e.g. `scrollback-limit` is bytes, not lines
3. Edit the config file
4. `ghostty_validate_config` → verify syntax
5. Most settings hot-reload; theme changes with `light:X,dark:Y` syntax may need full restart on macOS

## Workflows

### Theme
1. `ghostty_list_themes` — filter with `color="dark"` or `"light"`
2. Set `theme = <name>` — manual color settings (`background`, `foreground`) override theme colors
3. Dual theme: `theme = light:catppuccin-latte,dark:catppuccin-mocha`
4. After changing themes, if tab bar looks wrong → restart Ghostty (known macOS reload bug)

### Font
1. `ghostty_list_fonts` → name must match **exactly** (case-sensitive)
2. For fallback: repeat `font-family` on multiple lines
3. `ghostty_show_face` → verify which font renders specific characters
4. macOS CJK users: explicitly set a CJK font (e.g. `PingFang SC`) to avoid oversized fallback

### Keybind
1. `ghostty_list_actions` → available actions
2. `ghostty_list_keybinds` → current bindings
3. Format: `keybind = super+shift+c=copy_to_clipboard`
4. Chord: `keybind = ctrl+a>ctrl+b=action`
5. Unbind: `keybind = super+c=unbind`

### Troubleshooting "Config Not Working"

1. `ghostty_validate_config` → check syntax errors
2. `ghostty_show_current_config` with `changes_only=true` → see what's actually set
3. Check for inline `#` comments (they become part of the value)
4. Check for conflicting settings (manual colors override theme)
5. Try opening a new window — some settings need new window or full restart
6. macOS: check both config paths — macOS path takes priority over XDG

## Red Flags — STOP and Check Docs First

- "I know what this option does" → check anyway, units may surprise you
- "The value should be about 10000" → is it bytes? pixels? lines? check docs
- "This is similar to other terminals" → Ghostty syntax has unique rules
- "Just set it to true/false" → some options use `default`, `false`, or specific enum values

## Critical Gotchas (Inline)

- **`scrollback-limit`** = bytes, not lines. Default `10000000` = 10 MB. Setting `10000` gives only ~10 KB
- **`background-opacity`** has color blending bugs with light themes (premultiplied alpha). Tab appearance may break on Linux
- **`macos-titlebar-style = transparent`** silently reverts to `native` when background ≤ `#0c0c0c`
- **Linux fractional scaling** (125%, 150%): fonts will be blurry, no config workaround
- **`copy-on-select = true`** on macOS is effectively a no-op (no selection clipboard). Use `clipboard` to get "select to copy" on macOS

See `references/config-gotchas.md` for the complete list with details and workarounds.
See `references/config-recipes.md` for curated config patterns and combos (visual optimization, font tuning, macOS experience).
