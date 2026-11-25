---
name: computer-use
description: Linux/X11 desktop control — inspect, click, type into visible windows via AT-SPI + xdotool. Returns @eN refs from the focused window's accessibility tree.
---

# computer-use (Linux/X11)

## Quick Start

```
list_windows                          # → @wN list (title, pid, geometry)
screenshot {window:"@w2"}             # focus + capture; returns @eN AX targets + PNG
click {ref:"@e3"}                     # click an element by ref
type_text {text:"hello"}              # type at cursor
keypress {keys:["Return"]}            # submit
```

## Tools

| name | use |
|---|---|
| list_windows | enumerate visible windows |
| screenshot | focus window, capture PNG, return AX targets `@eN` |
| click | click `@eN`/`@wN` or `x,y`; supports `button`, `clickCount` |
| type_text | type literal text at cursor |
| set_text | replace `@eN` text/entry value (AT-SPI; falls back to ctrl+a + type) |
| keypress | press keys/chords (`Return`, `["Ctrl","A"]`, `["ctrl+l","Return"]`) |
| scroll | scroll at ref/coords by `scrollY`/`scrollX` pixels |
| computer_actions | run a sequence (≤20) in one call |

## Pitfalls

- **X11 only.** Wayland sessions cannot capture other-app windows or synthesize input.
- Enable AT-SPI: `gsettings set org.gnome.desktop.interface toolkit-accessibility true`.
- Keystrokes go to whatever currently has focus — call `screenshot {window}` first to focus the target.
- Mouse cursor physically moves on every click (no stealth pointer).
- `@eN` refs are scoped to the bridge process and invalidated by the next `screenshot`. Re-screenshot after layout changes.
- AX walk capped at depth 12 / 200 elements per app.
- Chrome / Electron expose AT-SPI only when launched with `--force-renderer-accessibility`.
- LibreOffice needs `SAL_USE_COMMON_ONE_ACCESSIBILITY=1` and a real Xorg session (not Xvfb).
