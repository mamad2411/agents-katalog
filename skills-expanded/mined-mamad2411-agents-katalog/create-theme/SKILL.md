---
name: create-theme
description: >
  Create custom color themes for Sidecar, including base theme selection,
  color overrides, gradient borders, tab styles, per-project themes,
  community themes, and programmatic theme registration. Use when creating
  or modifying themes, adjusting UI appearance, or debugging color/style
  issues. See references/palette-reference.md for the full color palette
  with all keys and per-theme values.
---

# Create Theme

## Configuration Location

Themes are configured in `~/.config/sidecar/config.json`:

```json
{
  "ui": {
    "showFooter": true,
    "showClock": true,
    "nerdFontsEnabled": false,
    "theme": {
      "name": "default",
      "overrides": {
        "primary": "#FF5500",
        "success": "#00FF00"
      }
    }
  }
}
```

## Available Base Themes

Sidecar ships with 21 modern, contrast-compliant themes designed around a 7-step neutral ramp and single signature chrome accent:

- **sidecar-modern** - Modern default with signature gold accent (`#c0982f`) and dark neutral ramp
- **catppuccin-mocha** - Soothing lavender/blue (`#89b4fa`) with dark mantle
- **tokyonight-storm** - Tokyo neon night blue (`#7aa2f7`)
- **gruvbox-dark** - Retro warm gold (`#fabd2f`) & aqua (`#8ec07c`)
- **dracula** - Refined vampire violet (`#bd93f9`)
- **nord** - Arctic frost cyan (`#88c0d0`)
- **atom-one-dark** - Balanced editor cyan/blue (`#61afef`)
- **kanagawa-wave** - Woodblock print wave blue (`#7e9cd8`)
- **rose-pine** - Soho rose (`#eb6f92`) & pine cyan (`#9ccfd8`)
- **everforest-dark** - Earthy forest green (`#a7c080`) & warm amber (`#dbbc7f`)
- **solarized-dark** - Precision amber/yellow (`#b58900`) & cyan (`#2aa198`)
- **monokai-pro** - Crisp gold (`#ffd866`) & green (`#a6e22e`)
- **night-owl** - Deep navy blue (`#82aaff`)
- **ayu-mirage** - Warm sunset gold (`#6dcbfa`) on slate
- **github-dark** - Crisp GitHub cobalt (`#58a6ff`)
- **synthwave** - 80s retrowave fuchsia (`#ff77ff`)
- **cobalt2** - High-contrast Wes Bos cobalt yellow (`#ffe50a`)
- **horizon** - Cyberpunk apricot/red (`#ed718e`)
- **shades-of-purple** - High-contrast magenta/violet (`#ff77ff`)
- **spacegray-eighties** - Muted classic warm gray & blue (`#7ba1cf`)
- **zenburn** - Low-contrast soft green (`#90cbae`)

## Creating a Custom Theme

### Method 1: Override Specific Colors

Start from a base theme and override specific colors:
```json
{
  "ui": {
    "theme": {
      "name": "default",
      "overrides": {
        "primary": "#E91E63",
        "success": "#4CAF50",
        "error": "#F44336",
        "syntaxTheme": "github"
      }
    }
  }
}
```

### Method 2: Full Theme Override

Override all colors for complete control. See `references/palette-reference.md` for every available color key and their default values across themes.

### Method 3: Custom Gradient Borders

Panel borders support angled gradients (default 30 degrees) flowing diagonally:
```json
{
  "ui": {
    "theme": {
      "overrides": {
        "gradientBorderActive": ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#8B00FF"],
        "gradientBorderAngle": 45
      }
    }
  }
}
```

Gradients support 2+ color stops. If not specified, solid `borderActive`/`borderNormal` colors are fallback.

## Tab Styles

Configure with `tabStyle` and `tabColors` in overrides:

**Tab Styles:**
- `gradient` - Colors flow continuously across all tabs (per-character interpolation)
- `per-tab` - Each tab gets a distinct solid color from array (cycles)
- `solid` - Uses theme primary/tertiary colors
- `minimal` - No background, active tab uses underline

**Built-in Presets** (use as `tabStyle` value):
- `rainbow` - Red -> Green -> Blue -> Purple (gradient)
- `sunset` - Orange -> Peach -> Pink (gradient)
- `ocean` - Deep Blue -> Cyan -> Light Blue (gradient)
- `aurora` - Purple -> Dark Purple -> Teal (gradient)
- `neon` - Magenta -> Cyan -> Green (gradient)
- `fire` - Red-Orange -> Orange -> Gold (gradient)
- `forest` - Dark Green -> Mid Green -> Light Green (gradient)
- `candy` - Pink -> Purple -> Turquoise (gradient)
- `pastel` - Pink, Green, Blue, Yellow (per-tab)
- `jewel` - Ruby, Sapphire, Amethyst, Topaz (per-tab)
- `terminal` - Red, Green, Cyan, Yellow (per-tab)
- `mono` - Theme primary color (solid)
- `accent` - Theme accent color (solid)
- `underline` - No background, underlined active (minimal)
- `dim` - No background, dim inactive (minimal)

Examples:
```json
// Use a preset
{ "overrides": { "tabStyle": "sunset" } }

// Custom gradient
{ "overrides": { "tabStyle": "gradient", "tabColors": ["#FF6B35", "#F7C59F", "#FF006E"] } }

// Per-tab distinct colors
{ "overrides": { "tabStyle": "per-tab", "tabColors": ["#FF5555", "#50FA7B", "#8BE9FD", "#F1FA8C"] } }
```

## Color Key Categories

All colors use hex format (`#RRGGBB`). Key categories:

- **Brand**: `primary`, `secondary`, `accent`
- **Status**: `success`, `warning`, `error`, `info`
- **Text**: `textPrimary`, `textSecondary`, `textMuted`, `textSubtle`, `textHighlight`, `textSelection`, `textInverse`
- **Background**: `bgPrimary`, `bgSecondary`, `bgTertiary`, `bgOverlay`, `selectionBg`
- **Border**: `borderNormal`, `borderActive`, `borderMuted`
- **Gradient border**: `gradientBorderActive`, `gradientBorderNormal` (arrays), `gradientBorderAngle` (number)
- **Tab**: `tabStyle`, `tabColors` (array)
- **Diff**: `diffAddFg`, `diffAddBg`, `diffRemoveFg`, `diffRemoveBg`
- **UI elements**: `buttonHover`, `tabTextInactive`, `link`, `toastSuccessText`, `toastErrorText`
- **Danger**: `dangerLight`, `dangerDark`, `dangerBright`, `dangerHover`
- **Blame age**: `blameAge1` through `blameAge5`
- **Third-party**: `syntaxTheme` (Chroma theme name), `markdownTheme` (`dark`/`light`)

Full color values for all themes: see `references/palette-reference.md`.

## Syntax Themes

The `syntaxTheme` value can be any Chroma theme:
- `monokai`, `dracula`, `github`, `github-dark`, `nord`, `onedark`, `solarized-dark`, `solarized-light`, `vs`, `vim`

See [Chroma Style Gallery](https://xyproto.github.io/splash/docs/) for all options.

It applies everywhere Sidecar highlights code: raw file previews, git diffs, and
fenced code blocks inside rendered Markdown. If the name is not a registered
Chroma style, Sidecar falls back deterministically to `github` for light
palettes and `monokai` for dark ones rather than failing.

## Markdown Colors

There is **no Markdown-specific color family**. Rendered Markdown — Files
preview, Notes view mode, conversation bodies, workspace document/issue/resource
panes, release notes — is styled by `internal/markdown` from the same normalized
semantic palette every other surface uses, so a new theme gets palette-correct
Markdown for free and a live theme preview (`#`) repaints already-open documents
immediately.

| Markdown role | Palette key |
| --- | --- |
| Body, paragraph, table text | `textPrimary` |
| H3–H4, image/definition terms | `textSecondary` |
| H5–H6, strikethrough, quote text, metadata | `textMuted` |
| H1, strong text, list/enumeration/task markers | `primary` |
| Other headings, inline code text | `accent` |
| Block quotes | `secondary` |
| Links and link text | `link` |
| Horizontal rules | `borderMuted` (falling back to `borderNormal`) |
| Inline code background | `bgSecondary` |
| Fenced code blocks | `syntaxTheme` |

The rendered document deliberately paints **no background** so pane chrome and
selection keep owning the canvas; only inline code and the Chroma code-block
style carry one.

### markdownTheme

`markdownTheme` is not a color. It has two behaviors:

- `dark` or `light` — the normal case. Sidecar takes only *structure* from that
  Glamour preset (margins, prefixes, list glyphs, task markers) and then
  overwrites every color from the table above. Set it to match your
  background; if it is missing or unusable, Sidecar picks a mode from
  `bgPrimary`'s luma.
- Any other value — an advanced **full-style override**: a registered Glamour
  style name, or a path to a Glamour JSON style file. That file owns the whole
  Markdown appearance and the palette mapping is skipped entirely. Use this only
  when you deliberately want Markdown to stop tracking the Sidecar palette.

Curated themes and community conversions must use `dark` or `light`; an
all-theme audit test (`internal/markdown/theme_audit_test.go`) fails on a
missing semantic color, an unknown `syntaxTheme`, or a non-structural
`markdownTheme`.

## Color Validation

Colors must be valid hex in `#RRGGBB` format. Invalid colors are ignored.
- Valid: `"#FF5500"`, `"#ff5500"` (lowercase ok)
- Invalid: `"FF5500"` (missing #), `"#F50"` (shorthand), `"red"` (named colors)

## Nerd Fonts

When `nerdFontsEnabled` is true: pill-shaped tabs (Powerline chars), pill-shaped buttons. Requires a Nerd Font installed in your terminal.

## Community Themes

Press `#` to open theme switcher, then `Tab` to browse 601 community color schemes. Supports search, live preview, color swatches. Press `Enter` to save.

Community themes are converted from iTerm2 color schemes. Stored by scheme name:
```json
{
  "ui": {
    "theme": {
      "name": "default",
      "community": "Catppuccin Mocha",
      "overrides": { "primary": "#ff79c6" }
    }
  }
}
```

To regenerate community themes from upstream:
```bash
git clone https://github.com/mbadolato/iTerm2-Color-Schemes ~/code/iTerm2-Color-Schemes
./scripts/generate-schemes.sh [path-to-repo]
```

## Per-Project Themes

Each project can have its own theme. When switching with `@`, theme changes automatically.

```json
{
  "projects": {
    "list": [
      { "name": "api", "path": "~/code/api", "theme": { "name": "dracula" } },
      { "name": "web", "path": "~/code/web", "theme": { "name": "default", "community": "Catppuccin Mocha" } },
      { "name": "tools", "path": "~/code/tools" }
    ]
  }
}
```

Set per-project: press `#`, then `ctrl+s` to toggle scope to "Set for this project".

Resolution order: project theme > global `ui.theme` > `"sidecar-modern"`.

## Programmatic Theme Registration

```go
import "github.com/marcus/sidecar/internal/styles"

myTheme := styles.Theme{
    Name:        "my-theme",
    DisplayName: "My Custom Theme",
    Colors: styles.ColorPalette{
        Primary:   "#FF5500",
        Secondary: "#00FF55",
        // ... all other colors
    },
}

styles.RegisterTheme(myTheme)
styles.ApplyTheme("my-theme")
```

## API Reference

```go
styles.ListThemes()                    // []string of available theme names
styles.GetTheme("dracula")             // Theme struct
styles.IsValidTheme("my-theme")        // bool
styles.IsValidHexColor("#FF5500")       // bool
styles.GetCurrentTheme()               // Theme
styles.GetCurrentThemeName()           // string
styles.ApplyTheme("dracula")
styles.ApplyThemeWithOverrides("default", map[string]string{"primary": "#FF5500"})

// Resolve effective theme for a project path (project > global > default)
import "github.com/marcus/sidecar/internal/theme"
resolved := theme.ResolveTheme(cfg, "/path/to/project")
theme.ApplyResolved(resolved)
```

## Modern Theme Architecture (`Sidecar Modern` Standard)

Modern Sidecar themes (`sidecar-modern`, `catppuccin-mocha`) follow a refined, disciplined design system:

1. **Single Chrome Accent**: Exactly *one* primary accent hue (e.g. Gold `#c0982f` in `sidecar-modern`, Blue `#89b4fa` in `catppuccin-mocha`). Used for cursor `❯`, active tab highlight, footer key glyphs (`keyHintFg`), and active border. Chrome does not use multi-color rainbow gradients.
2. **Structural Neutral Ramp**: Geometry and hierarchy are carried by neutral lightness steps, not saturation:
   - `BgPrimary`: Canvas background
   - `BgSecondary`: Header / footer bar fills
   - `BgTertiary`: Selected row background
   - `SelectionBg`: Text-selection highlight; must lift off the canvas (`TargetSelectionSeparation`, currently 2.65:1) without leaving the canvas ink pole
   - `SurfaceRaised`: Raised pills (key hints, bar chips) sitting subtly above canvas/bars
   - `BorderNormal` / `BorderMuted`: Rules and hairlines
   - `TextPrimary` → `TextSecondary` → `TextMuted` → `TextSubtle`: Typography ramp
3. **Tab Style**: Default to `"minimal"` with single accent underline/highlight.
4. **Semantics-Driven Colors**: Colors other than the single chrome accent are strictly earned by meaning (Done = Green, Open/ID = Teal, Destructive/Error = Red, Warning/P2 = Yellow/Gold, Links/Headings = Blue/Sapphire).

### Contrast Rules (Strict AA Standard)

When authoring or converting themes, check contrast against **all** surfaces:

1. **Multi-Fill Validation (>= 4.5:1)**:
   - `TextPrimary`, `TextSecondary`, `TextMuted`, and `TextSelection` must clear 4.5:1 on ALL three background fills: `BgPrimary`, `BgSecondary`, and `BgTertiary` (selected row).
   - All semantic accents (`Primary`, `Secondary`, `Success`, `Warning`, `Error`, `Info`, `Link`, `LaneWorking`, `LaneBlocked`, `LaneDone`, `LaneIdle`, `LanePaused`, `ProjectHues[*]`) must clear >= 4.5:1 on `BgPrimary`, `BgSecondary`, and `BgTertiary`.
2. **Raised Chrome (`SurfaceRaised`)**:
   - `TextPrimary`, `TextSecondary`, `TextMuted`, and `KeyHintFg` must clear >= 4.5:1 on `SurfaceRaised`.
   - `TextSubtle` and `TabTextInactive` must clear >= 3.0:1 on `SurfaceRaised`.
3. **Ink on Bright Fills**:
   - For bright or pastel status/danger backgrounds (e.g. `DangerBright`, `ToastSuccess`, `ToastError`), use dark canvas ink (`#0f1113` or `#181825`) for `TextInverse` / `Toast*Text`, as white (`#ffffff`) fails contrast on light reds/yellows.
   - `DangerLight` must clear >= 4.5:1 on `DangerDark`.
4. **Text-selection highlight (`SelectionBg`)**:
   - Must clear `TargetSelectionSeparation` (currently 2.65:1) against `BgPrimary` so a selected span is findable against the shell canvas. `BgTertiary` (the selected-row fill) is not enough. Bump that constant to lift every theme at once.
   - Must stay on the same ink pole as `BgPrimary`, and `TextPrimary` must still clear >= 4.5:1 on it. Do not invert selected text or lighten the highlight until headings and syntax wash out.
   - `NormalizePalette` lifts empty, inverted, or too-dim values; author the role deliberately on curated themes.
