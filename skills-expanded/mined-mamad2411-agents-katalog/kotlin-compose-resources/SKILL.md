---
name: kotlin-compose-resources
description: >-
  Use when adding or reviewing shared Compose Multiplatform strings, images, fonts,
  or files via composeResources / Res.* — qualifiers, generation, and when to use
  Android res/ or iOS asset catalogs instead.
---

# Compose Multiplatform Resources

Use this skill when implementing or reviewing user-facing resources in shared Compose UI (`sharedUI` / `commonMain`).

## Goals

- No hardcoded user-facing strings or raw asset paths in shared UI
- Correct `composeResources` layout and generated `Res` usage
- Clear split vs platform-native resource systems

## Prefer official defaults

- Put shared Compose resources under `src/commonMain/composeResources/` (or the module’s documented composeResources root).
- Access via generated `Res` (`stringResource(Res.string.*)`, `painterResource(Res.drawable.*)`, etc.).
- Use qualifiers (locale, theme, density) per Compose Multiplatform resources docs.
- Keep Android `res/` and iOS asset catalogs for **platform-only** needs (launcher icons, system notifications, native screens).

Docs: https://kotlinlang.org/docs/multiplatform/compose-images-resources.html

## Layout expectations

Typical tree:

```text
commonMain/composeResources/
  values/strings.xml
  values-es/strings.xml
  drawable/
  font/
  files/
```

- Prefer XML string resources for localizable copy.
- Prefer vector/raster drawables under `drawable/` for shared UI imagery.
- Do not commit generated `Res` sources by hand; let the Compose resources plugin generate them.

## Usage rules

- Shared composables: `stringResource(Res.string.foo)` — not string literals for user-visible text.
- Design-system demos/previews may use literals only when they are not shipped UI copy.
- Pass already-resolved `String` into state holders when the holder must stay resource-free; resolve at the UI edge when possible.
- Do not hardcode `dp` spacing when the project has design tokens — that belongs to UI/design-system skills, not this one.

## When NOT to use composeResources

| Need | Prefer |
|------|--------|
| Android launcher / notification icons | Android `res/` |
| iOS App Icon / native SwiftUI assets | Asset Catalog |
| Non-Compose shared logic needing strings | Design carefully — usually UI resolves strings; avoid pulling Compose Resources into pure logic modules |
| Binary configs unrelated to UI | `files/` only if truly needed by UI; else data layer |

## Review flags

- Hardcoded user-facing strings in `sharedUI` / common composables
- Resources placed under Android `res/` that should be shared with other Compose targets
- Edited generated `Res` files
- Missing locale qualifiers when the product claims localization
- Logic modules depending on Compose Resources solely for copy

## Related skills

- `kotlin-ui-compose-multiplatform` — composable structure
- `kotlin-ui-adaptive-resources` — window-size / adaptive **layout** (not string resources)
