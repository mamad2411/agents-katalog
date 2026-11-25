---
license: CC-BY-4.0
description: >-
  Advanced theming for Shiny apps using bslib and Bootstrap 5. Use when
  customizing app appearance with bs_theme(), Bootswatch themes, custom
  colors, typography, brand.yml integration, Bootstrap Sass variables,
  custom Sass/CSS rules, dark mode and color modes, dynamic theme switching,
  real-time theming, theme inspection, or making R plots match the app theme
  with thematic.
compatibility: >-
  Requires R, shiny (>= 1.8.1), bslib (>= 0.9.0). Examples verified with
  bslib 0.12.0, shiny 1.14.0, and thematic 0.1.8 on 2026-09-29.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Theming Shiny Apps with bslib

Customize Shiny app appearance with bslib's Bootstrap 5 theming system, from a
preset to Sass rules and color modes. Verify against
https://rstudio.github.io/bslib/ when an argument or default matters.

## Choose a reference

| Read | When you need |
|---|---|
| [references/typography.rst](references/typography.rst) | `font_google()` weights, `font_link()`, `font_face()`, fallback stacks, or fonts in plots |
| [references/theme-tools.rst](references/theme-tools.rst) | Common Bootstrap Sass variables, `bs_add_rules()` details, `bs_add_functions()`/`bs_add_mixins()`, `bs_bundle()`, the interactive themer, or `bs_get_variables()` |
| [references/sass-and-css-variables.rst](references/sass-and-css-variables.rst) | How Sass variables become `--bs-*` CSS custom properties, per-element `data-bs-theme`, or CSS utility classes |
| [references/dark-mode.rst](references/dark-mode.rst) | `input_dark_mode()`, `toggle_dark_mode()`, `session$setCurrentTheme()`, styles that work in both modes, or which components respond to theming |

## Quick start

```r
page_sidebar(
  theme = bs_theme(),                    # "shiny" preset (default)
  # theme = bs_theme(preset = "zephyr"), # Bootswatch: a different visual style
  ...
)

bs_theme(
  version = 5,
  bg = "#FFFFFF", fg = "#333333", primary = "#2c3e50",
  base_font = font_google("Lato"),
  heading_font = font_google("Montserrat")
)
```

If `_brand.yml` exists in the app or project directory, `bs_theme()` applies
it automatically (brand.yml support needs bslib >= 0.9.0; since bslib 0.10.0
discovery also requires the `brand.yml` R package).
`bs_theme(brand = FALSE)` disables discovery, `brand = TRUE` requires the
file, and `brand = "path/to/brand.yml"` names it.

## Presets

- **`"shiny"` (default for Bootstrap 5+):** `bs_theme()` with no preset is
  a purpose-built Shiny theme, **not** plain Bootstrap. It styles cards,
  sidebars, and value boxes. For example, its `$primary` is `#007bc2`.
  Start here and adjust colors and fonts before choosing a Bootswatch theme.
- **`"bootstrap"`:** `preset = "bootstrap"` removes the Shiny preset and
  gives unmodified Bootstrap 5 (`$primary` is `#0d6efd`).
- **Bootswatch:** `bootswatch_themes()` lists them; `bootswatch =` is an
  alias for `preset =`. Choose one that fits the app's purpose and audience;
  do not apply one by default. Examples: `"zephyr"`, `"cosmo"`, `"minty"`,
  `"flatly"`, `"litera"`, `"darkly"`, `"cyborg"`, `"simplex"`, `"sketchy"`.
- `builtin_themes()` lists bslib's own presets.

## Workflow

1. Start with the `"shiny"` preset or a Bootswatch theme close to the target.
2. Set the main colors (`bg`, `fg`, `primary`).
3. Set fonts with `font_google()` or another font helper.
4. Fine-tune Bootstrap Sass variables (see "Sass variables and placement").
5. Add Sass rules with `bs_add_rules()` only when variables are not enough.
6. Call `thematic::thematic_shiny()` so plots match.
7. Preview with `bs_themer()` during development
   ([references/theme-tools.rst](references/theme-tools.rst)).
8. Check contrast before you finish.

```r
theme <- bs_theme(preset = "minty") |>
  bs_theme_update(primary = "#1a9a7f", base_font = font_google("Lato")) |>
  bs_add_rules(".card { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }")
```

## bs_theme()

```r
bs_theme(
  version = version_default(),
  preset = NULL,        # "shiny" (default for BS5+), "bootstrap", or Bootswatch name
  ...,                  # Bootstrap Sass variable overrides
  brand = NULL,         # brand.yml: NULL (auto), TRUE (require), FALSE (disable), or path
  bg = NULL, fg = NULL,
  primary = NULL, secondary = NULL,
  success = NULL, info = NULL, warning = NULL, danger = NULL,
  base_font = NULL, code_font = NULL, heading_font = NULL,
  font_scale = NULL,    # Multiplier for all font sizes (1.5 = 150%)
  bootswatch = NULL     # Alias for preset
)
```

`bs_theme_update(theme, ...)` modifies a theme; `is_bs_theme(x)` tests one.

Main colors cascade into hundreds of CSS rules. `bg`/`fg` should share a hue
with a large luminance difference. `primary` (links, active navigation, input
focus) must contrast with both. `secondary` is the default for action buttons;
`success`, `info`, `warning`, and `danger` color states. Any color that
`htmltools::parseCssColors()` understands works.

Fonts: `base_font`, `heading_font`, and `code_font` each take a font object,
a `font_collection()`, or family names. Add fallbacks to avoid invisible text
on slow connections:

```r
bs_theme(
  base_font = font_collection(
    font_google("Lato", local = FALSE), "Helvetica Neue", "Arial", "sans-serif"
  )
)
```

## Sass variables and placement

Pass any Bootstrap Sass variable through `bs_theme(...)` or
`bs_add_variables()`. Names: https://rstudio.github.io/bslib/articles/bs5-variables/

`bs_theme(...)` and the default `bs_add_variables()` place values **before**
Bootstrap's own defaults, so they cannot refer to another Bootstrap variable
such as `$secondary`. That fails to compile with `Undefined variable`.

| `.where` | Placement and use |
|---|---|
| `"defaults"` (default) | Before Bootstrap's defaults, with `!default`. Literal values. |
| `"declarations"` | After Bootstrap's defaults. Use when the value references `$secondary`, `$primary`, and so on. |
| `"rules"` | After all rules. Rarely needed. |

```r
# Fails: $secondary is not defined yet
# bs_theme("progress-bar-bg" = "$secondary")

bs_theme() |>
  bs_add_variables("progress-bar-bg" = "$secondary", .where = "declarations")
```

For custom rules that use variables and mixins, use `bs_add_rules()`; see
[references/theme-tools.rst](references/theme-tools.rst). Prefer variables
over custom CSS, because variables cascade to every related component. For
one-off styling, prefer Bootstrap utility classes
([references/sass-and-css-variables.rst](references/sass-and-css-variables.rst)).

## Theming R plots

`bs_theme()` affects only CSS. Server-rendered plots need `thematic`. Call
`thematic_shiny()` once before `shinyApp()`. It covers base R, ggplot2, and
lattice, and turns itself off when the app stops.

```r
library(thematic)
thematic_shiny(font = "auto")
shinyApp(ui, server)
```

- Colors follow the theme by default (`bg`, `fg`, and `accent` are
  `"auto"`).
- Fonts do **not** follow the theme unless you pass `font = "auto"` (the
  default `font = NA` leaves plot fonts unchanged). thematic downloads a
  Google Font that R cannot find only when `ragg` or `showtext` is installed.
- thematic responds to `session$setCurrentTheme()` but not to client-side
  `input_dark_mode()` toggles; see
  [references/dark-mode.rst](references/dark-mode.rst).

## Dashboard background

The `bslib-page-dashboard` class adds a light grey background behind the main
content so cards stand out. It changes appearance only, not layout.

```r
page_sidebar(
  class = "bslib-page-dashboard",
  title = "My Dashboard",
  sidebar = sidebar(...),
  ...
)
```

With `page_navbar()`, put the class on individual `nav_panel()`s, **not** on
`page_navbar()`, so only dashboard pages get the grey background:

```r
page_navbar(
  title = "Analytics",
  nav_panel("Dashboard", class = "bslib-page-dashboard",
    layout_column_wrap(...)
  ),
  nav_panel("Report",
    ...   # No class: standard background for prose and reports
  )
)
```

## Contrast checks

`bs_get_contrast(theme, varnames)` returns the text color that Bootstrap's
`color-contrast()` chooses for each background variable, usually `#FFFFFF` or
`#000000`. It does **not** return a contrast ratio.

```r
bs_get_contrast(bs_theme(primary = "#1a5276"), "primary")
#>   primary
#> "#FFFFFF"
```

Measure the ratio between the background and that text color with browser
developer tools or a WCAG contrast checker. Aim for WCAG AA: 4.5:1 for normal
text and 3:1 for large text. Check both modes when the app supports dark mode.

## Best practices

1. Prefer `bs_theme()` arguments and Sass variables over custom CSS.
2. Pin the Bootstrap version: `bs_theme(version = 5)`.
3. Use fallback fonts with `font_collection()`.
4. Test inputs, buttons, cards, navigation, plots, tables, modals, toasts, and
   mobile widths.
5. Check contrast as above.
6. Keep a complex theme in its own `theme.R`
   ([references/theme-tools.rst](references/theme-tools.rst)).
