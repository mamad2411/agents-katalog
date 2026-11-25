---
name: md3e
version: 1.1.0
description: "Material Design 3 Expressive (MD3E) design system skill for Android Jetpack Compose. This skill should be used when building Android UI with Material 3 / Material 3 Expressive design language, including theming (color schemes, typography, shapes, motion), component implementation (buttons, cards, navigation, FAB, floating toolbar, button group, etc.), and design guidance (when to use which component, M3 vs M3E differences, expressive design principles). Covers both MD3E (the evolution released 2025, targeting Android 16) and baseline M3 (many components only have M3 specs). Triggers on requests like Material 3 Expressive, MD3E, Material Design 3, M3 theme, MaterialExpressiveTheme, Compose Material 3 component, or when designing/building Android UI that should follow Google Material design guidelines."
---

# Material Design 3 Expressive (MD3E) Skill

## Overview

Comprehensive knowledge of Google's Material Design 3 Expressive (MD3E) design system and its
implementation in Android Jetpack Compose (`androidx.compose.material3`). MD3E is the 2025 evolution
of M3, with research-backed updates to theming, components, motion, typography, and shapes. It targets
Android 16 but is available via the Compose Material 3 library (1.5.0-alpha+) for lower API levels.

**M3 vs M3E:** MD3E is an *expansion* of M3, not a replacement. Many components still only have M3
specs. Prefer MD3E APIs where available; fall back to M3 for components not yet updated.

## When to Use This Skill

- Building Android UI with Jetpack Compose that should follow Material design guidelines
- Setting up Material theming (color scheme, typography, shapes, motion scheme)
- Implementing or customizing Material components (buttons, cards, navigation, FAB, etc.)
- Migrating from M2→M3 or M3→M3E (`MaterialExpressiveTheme`)
- Answering questions about Material 3 / M3E specs (color roles, type scale, shape scale)
- Designing expressive UI with new MD3E components (FloatingToolbar, ButtonGroup, WideNavigationRail, etc.)
- Reviewing UI for Material design compliance

## Quick Reference: Key MD3E APIs

| Category | M3 (baseline) | MD3E (expressive) |
|----------|---------------|-------------------|
| Theme | `MaterialTheme` | `MaterialExpressiveTheme` |
| Color scheme | `lightColorScheme()` / `darkColorScheme()` | `expressiveLightColorScheme()` |
| Motion | (easing + duration tokens) | `MotionScheme.standard()` / `MotionScheme.expressive()` |
| Shapes | `Shapes(extraSmall, small, medium, large, extraLarge)` | (same, with more varied usage) |
| Experimental opt-in | `@ExperimentalMaterial3Api` | `@ExperimentalMaterial3ExpressiveApi` |

### MD3E-Only Components (require `@ExperimentalMaterial3ExpressiveApi` unless graduated)

- `HorizontalFloatingToolbar` / `VerticalFloatingToolbar` — floating contextual toolbars
- `ButtonGroup` — connected button row with overflow menu
- `SplitButtonLayout` — split button with primary + overflow actions
- `WideNavigationRail` / `ModalWideNavigationRail` — expanded rail for large screens
- `ToggleFloatingActionButton` — FAB toggling two states with morph animation
- `FloatingActionButtonMenu` — FAB that expands into a menu
- `FlexibleBottomAppBar` — bottom app bar with flexible arrangement
- `MediumFlexibleTopAppBar` / `LargeFlexibleTopAppBar` — flexible top app bars
- Expressive list items (non-interactive variants), Expressive TimePicker

## Workflow

Follow these steps when building or modifying Material UI:

1. **Set up theming** — Use `MaterialExpressiveTheme` instead of `MaterialTheme`. See the snippet
   below for the standard scaffold.
2. **Generate a theme from a brand color (optional)** — Run `scripts/generate_theme.py` to derive a
   full light/dark color scheme from one seed color. Copy `assets/templates/` into the project and
   customize, or let the script emit `Color.kt` + `Theme.kt`.
3. **Choose components** — Consult `references/components-catalog.md` for the categorized list with
   M3/MD3E tags and key parameters.
4. **Apply design tokens** — Token values live in `references/design-tokens.md`. Access at runtime via
   `MaterialTheme.colorScheme.*` / `.typography.*` / `.shapes.*` / `.motionScheme.*`.
5. **Look up API signatures** — For any composable/function, grep `references/compose-api-full.md`
   (e.g. `### ComponentName`, `fun lightColorScheme`, `MaterialExpressiveTheme`, `MotionScheme`).
6. **Look up official specs** — For design specs (anatomy, states, measurements), read files under
   `references/m3-content/` (e.g. `m3-content/components/{name}/specs.md`,
   `m3-content/styles/{category}/`).

### Standard theme scaffold

```kotlin
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.expressiveLightColorScheme
import androidx.compose.material3.MotionScheme
import androidx.compose.runtime.Composable

@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit,
) {
    MaterialExpressiveTheme(
        colorScheme = if (darkTheme) darkColorScheme() else expressiveLightColorScheme(),
        motionScheme = MotionScheme.expressive(),  // or MotionScheme.standard()
        typography = AppTypography,
        shapes = AppShapes,
        content = content,
    )
}
```

### Theme generator

```bash
python scripts/generate_theme.py --seed #6750A4 --package com.example.app --output ./theme/
```

Outputs `Color.kt` + `Theme.kt`. Uses Material Color Utilities (HCT); has a built-in fallback if the
library is not installed.

## Resources (read on demand)

Only open these when the workflow above points to them — they are large and not needed every turn.

- `references/compose-api-full.md` — Full `androidx.compose.material3` API reference (~8000 lines).
  Use for exact signatures.
- `references/design-tokens.md` — All color roles, type scale (15 styles), shape scale (5 sizes),
  motion system. Use for token values.
- `references/components-catalog.md` — Component list by category with M3/MD3E tags. Use to pick a
  component.
- `references/m3-vs-m3e-diff.md` — M3↔M3E differences, migration, I/O 2026 updates.
- `references/expressive-design-tactics.md` — The 7 official M3E design tactics with examples.
- `references/design-research.md` — HCT color science, variable fonts, motion/accessibility research.
- `references/m3-content/` — Mirror of m3.material.io (256 files). Authoritative design specs;
  read `m3-content/components/{name}/specs.md` or `m3-content/styles/{category}/` as needed.
- `assets/templates/` — Ready-to-use `MD3ETheme.kt`, `Color.kt`, `Type.kt`, `Shape.kt`. Copy into
  `ui/theme/` and customize.
- `scripts/generate_theme.py` — Seed color → complete Compose theme (see Workflow step 2).

## Design Principles (MD3E)

1. **Color as hierarchy** — Use color roles (primary/secondary/tertiary + containers + surface tones)
   for visual layers. MD3E adds `*Fixed` roles that stay constant across light/dark.
2. **Shape variety** — Mix rounded/pill/angular shapes to create tension and guide attention.
3. **Spring-based motion** — Use spring physics; `MotionScheme.expressive()` for lively,
   `MotionScheme.standard()` for subtle.
4. **Variable typography** — Use weight/size/color/spacing for editorial hierarchy.
5. **Container grouping** — Group related content in surface-toned containers to reduce load.
6. **Adaptive components** — Adapt to screen size (`WideNavigationRail` large, `NavigationBar` compact).
7. **Highlight moments** — Create 1-2 delightful interaction moments that connect emotionally.
