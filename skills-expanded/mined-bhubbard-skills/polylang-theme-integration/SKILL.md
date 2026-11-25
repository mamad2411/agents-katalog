---
name: polylang-theme-integration
description: Guide for integrating Polylang into custom WordPress block and classic themes.
---

# Polylang Theme Integration

This skill helps integrate Polylang features into WordPress themes, both Classic and Block-based.

## Language Switchers
- **Block Themes**: Use the "Language Switcher" or "Navigation Language Switcher" blocks.
- **Classic Themes**: Use the legacy Polylang widget or add the language switcher to navigation menus.
- Custom Switcher: Use `pll_the_languages()` function in classic PHP templates to output custom HTML for language selection.

## Template Translation
- In Block Themes (FSE), use Polylang Pro features to translate template parts if available, or rely on block visibility based on language.
- Ensure all hardcoded text in theme files is wrapped in WordPress translation functions (e.g., `__()`, `_e()`) so they can be registered and translated via Polylang's Strings Translations.

## Menus and Widgets
- Create separate menus for each language and assign them to the corresponding theme locations.
- Assign widgets to specific languages or use the widget block editor options to control visibility per language.
