---
name: shiny-bslib
license: CC-BY-4.0
description: >-
  Build or modernize Shiny apps with bslib (Bootstrap 5): page_sidebar/
  page_navbar/page_fillable layouts, cards, value boxes, grids, navigation,
  sidebars, filling layouts, accordions, tooltips, popovers, toasts, and bslib
  inputs; convert fluidPage/tabsetPanel/wellPanel/shinythemes apps. Covers
  theme basics; for Sass variables, fonts, brand.yml, dark mode, or thematic
  plots use shiny:bslib-theming.
compatibility: >-
  Requires R, shiny (>= 1.8.1), and bslib (>= 0.9.0). Toasts,
  input_code_editor(), and input_submit_textarea() need bslib >= 0.10.0.
  Minimum checked by loading bslib 0.9.0 from the CRAN archive; examples
  verified with bslib 0.12.0 and shiny 1.14.0 on 2026-09-29.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Modern Shiny Apps with bslib

Build professional Shiny dashboards using bslib's Bootstrap 5 components and layouts. This skill focuses on modern UI/UX patterns that replace legacy Shiny approaches.

## Quick Start

**Single-page dashboard:**
```r
library(shiny)
library(bslib)

ui <- page_sidebar(
  title = "My Dashboard",
  theme = bs_theme(version = 5),  # "shiny" preset by default
  sidebar = sidebar(
    selectInput("variable", "Variable", choices = names(mtcars))
  ),
  layout_column_wrap(
    width = 1/3,
    fill = FALSE,
    value_box(title = "Users", value = "1,234", theme = "primary"),
    value_box(title = "Revenue", value = "$56K", theme = "success"),
    value_box(title = "Growth", value = "+18%", theme = "info")
  ),
  card(
    full_screen = TRUE,
    card_header("Plot"),
    plotOutput("plot")
  )
)

server <- function(input, output, session) {
  output$plot <- renderPlot({
    hist(mtcars[[input$variable]], main = input$variable)
  })
}

shinyApp(ui, server)
```

**Multi-page dashboard:**
```r
ui <- page_navbar(
  title = "Analytics Platform",
  theme = bs_theme(version = 5),
  nav_panel("Overview", overview_ui),
  nav_panel("Analysis", analysis_ui),
  nav_panel("Reports", reports_ui)
)
```

## Core Concepts

### Page Layouts

- **`page_sidebar()`** -- Single-page dashboard with sidebar (most common)
- **`page_navbar()`** -- Multi-page app with top navigation bar
- **`page_fillable()`** -- Viewport-filling layout for custom arrangements
- **`page_fluid()`** -- Scrolling layout for long-form content

See [page-layouts.rst](references/page-layouts.rst) for detailed guidance.

### Grid Systems

- **`layout_column_wrap()`** -- Uniform grid with auto-wrapping (recommended for most cases)
- **`layout_columns()`** -- 12-column Bootstrap grid with precise control

See [grid-layouts.rst](references/grid-layouts.rst) for detailed guidance.

### Cards

Primary container for dashboard content. Support headers, footers, multiple body sections, and full-screen expansion.

See [cards.rst](references/cards.rst) for detailed guidance.

### Value Boxes

Display key metrics and KPIs with optional icons, sparklines, and built-in theming.

See [value-boxes.rst](references/value-boxes.rst) for detailed guidance.

### Navigation

- **Page-level**: `page_navbar()` for multi-page apps
- **Component-level**: `navset_card_underline()`, `navset_tab()`, `navset_pill()` for tabbed content

See [navigation.rst](references/navigation.rst) for detailed guidance.

### Sidebars

- **Page-level**: `page_sidebar()` or `page_navbar(sidebar = ...)`
- **Component-level**: `layout_sidebar()` within cards
- Supports conditional content, dynamic open/close, accordions

See [sidebars.rst](references/sidebars.rst) for detailed guidance.

### Filling Layouts

The fill system controls how components resize to fill available space. Key concepts: fillable containers, fill items, fill carriers. Fill activates when containers have defined heights.

See [filling.rst](references/filling.rst) for detailed guidance.

### Theming

- **`bs_theme(version = 5)`** uses the `"shiny"` preset, which is not plain
  Bootstrap; `preset = "<bootswatch>"` gives a different style.
- **Colors and fonts**: `bg`, `fg`, `primary`, and `font_google()` affect
  hundreds of CSS rules.
- **Dashboard background**: `class = "bslib-page-dashboard"` on
  `page_sidebar()`, or on individual `nav_panel()`s (not `page_navbar()`).
- **Plots**: call `thematic::thematic_shiny()`; pass `font = "auto"` if plot
  fonts should match too.

For anything beyond this, including Sass variables, brand.yml, dark mode,
dynamic theming, and contrast checks, use the **shiny-bslib-theming** skill
(`/shiny:bslib-theming`).

### UI Components

- **Accordions** -- Collapsible sections, especially useful in sidebars
- **Tooltips** -- Hover-triggered help text
- **Popovers** -- Click-triggered containers for secondary UI/inputs
- **Toasts** -- Temporary notification messages (bslib >= 0.10.0)

See [accordions.rst](references/accordions.rst), [tooltips-popovers.rst](references/tooltips-popovers.rst), and [toasts.rst](references/toasts.rst).

### Icons

**Recommended: `bsicons` package** (Bootstrap Icons, designed for bslib):
```r
bsicons::bs_icon("graph-up")
bsicons::bs_icon("people", size = "2em")
```

Browse icons: https://icons.getbootstrap.com/

**Alternative: `fontawesome` package:**
```r
fontawesome::fa("envelope")
```

**Accessibility for icon-only triggers:** When an icon is used as the sole trigger for a tooltip, popover, or similar interactive element (no accompanying text), it must be accessible to screen readers. By default, icon packages mark icons as decorative (`aria-hidden="true"`), which hides them from assistive technology.

- **`bsicons::bs_icon()`**: Provide `title` — this automatically sets `a11y = "sem"`
  ```r
  tooltip(
    bs_icon("info-circle", title = "More information"),
    "Tooltip content here"
  )
  ```
- **`fontawesome::fa()`**: Set `a11y = "sem"` and provide `title`
  ```r
  tooltip(
    fa("circle-info", a11y = "sem", title = "More information"),
    "Tooltip content here"
  )
  ```

The `title` should describe the purpose of the trigger (e.g., "More information", "Settings"), not the icon itself (e.g., not "info circle icon").

### Special Inputs

- **`input_switch()`** -- Toggle switch (modern checkbox alternative)
- **`input_dark_mode()`** -- Dark mode toggle
- **`input_task_button()`** -- Button for long-running operations
- **`input_code_editor()`** -- Code editor with syntax highlighting (bslib >= 0.10.0)
- **`input_submit_textarea()`** -- Textarea with explicit submission (bslib >= 0.10.0)

See [inputs.rst](references/inputs.rst) for detailed guidance.

## Common Workflows

### Building a Dashboard

1. Choose page layout: `page_sidebar()` (single-page) or `page_navbar()` (multi-page)
2. Add theme with `bs_theme()` (consider Bootswatch for quick start)
3. Create sidebar with inputs for filtering/controls
4. Add value boxes at top for key metrics (set `fill = FALSE` on container)
5. Arrange cards with `layout_column_wrap()` or `layout_columns()`
6. Enable `full_screen = TRUE` on all visualization cards
7. Add `thematic::thematic_shiny()` for plot theming

### Modernizing an Existing App

See [migration.rst](references/migration.rst) for a complete mapping of legacy patterns to modern equivalents. Key steps:

1. Replace `fluidPage()` with `page_sidebar()` or `page_navbar()`
2. Replace `fluidRow()`/`column()` with `layout_columns()`
3. Wrap outputs in `card(full_screen = TRUE)`
4. Add `theme = bs_theme(version = 5)`
5. Convert key metrics to `value_box()` components
6. Replace `tabsetPanel()` with `navset_card_underline()`

## Guidelines

1. **Prefer bslib page functions** (`page_sidebar()`, `page_navbar()`, `page_fillable()`, `page_fluid()`) over legacy equivalents (`fluidPage()`, `navbarPage()`)
2. **Use `layout_column_wrap()` or `layout_columns()`** for grid layouts instead of `fluidRow()`/`column()`, which don't support filling layouts
3. **Wrap outputs in `card(full_screen = TRUE)`** when building dashboards -- full-screen expansion is a high-value feature
4. **Set `fill = FALSE`** on `layout_column_wrap()` containers holding value boxes (they shouldn't stretch to fill height)
5. **Pin Bootstrap version**: include `theme = bs_theme(version = 5)` or a preset theme
6. **Use `thematic::thematic_shiny()`** in the server so base R and ggplot2 plots match the app theme
7. **Use responsive widths** like `width = "250px"` in `layout_column_wrap()` for auto-adjusting columns
8. **Group sidebar inputs** with `accordion()` when sidebars have many controls
9. **See [migration.rst](references/migration.rst)** for mapping legacy Shiny patterns to modern bslib equivalents

## Avoid Common Errors

Read [best-practices.rst](references/best-practices.rst) before you finish a
dashboard, and when a layout does not fill, scroll, or respond as expected. It
covers layout patterns, mobile behavior, module patterns, and common gotchas.

1. Avoid directly nesting `card()` containers. `navset_card_*()` functions are already cards; `nav_panel()` content goes directly inside them without wrapping in `card()`
2. Only use `layout_columns()` and `layout_column_wrap()` for laying out multiple elements. Single children should be passed directly to their container functions.
3. Never nest `page_*()` functions. Only use one top-level page function per app.

## Reference Files

- **[migration.rst](references/migration.rst)** -- Legacy Shiny to modern bslib migration guide
- **[page-layouts.rst](references/page-layouts.rst)** -- Page-level layout functions and patterns
- **[grid-layouts.rst](references/grid-layouts.rst)** -- Multi-column grid systems
- **[cards.rst](references/cards.rst)** -- Card components and features
- **[value-boxes.rst](references/value-boxes.rst)** -- Value boxes for metrics and KPIs
- **[navigation.rst](references/navigation.rst)** -- Navigation containers and patterns
- **[sidebars.rst](references/sidebars.rst)** -- Sidebar layouts and organization
- **[filling.rst](references/filling.rst)** -- Fillable containers and fill items
- **[accordions.rst](references/accordions.rst)** -- Collapsible sections and sidebar organization
- **[tooltips-popovers.rst](references/tooltips-popovers.rst)** -- Hover tooltips and click-triggered popovers
- **[toasts.rst](references/toasts.rst)** -- Temporary notification messages
- **[inputs.rst](references/inputs.rst)** -- Special bslib input widgets
- **[best-practices.rst](references/best-practices.rst)** -- bslib-specific patterns and common gotchas
