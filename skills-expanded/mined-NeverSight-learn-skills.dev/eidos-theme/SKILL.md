---
name: eidos-theme
description: Generates and manages file-based themes for Eidos spaces. Use this skill when asked to create, modify, or analyze custom themes in Eidos workspaces.
---

# Eidos Theme Management

This skill guides you through generating and managing Eidos themes through the file system. Eidos themes are space-isolated and file-based.

## Quick Start

Themes are managed on a **per-space** basis, meaning different Eidos spaces can have completely independent visual appearances.

A custom theme is defined by a standard `theme.css` file stored in a dedicated directory within the space's hidden `.eidos/themes/` folder.

### Theme Directory Structure

The structure of a space's theme directory looks like this:

```
[SPACE_ROOT]/.eidos/themes/
└── [theme-name]/
    └── theme.css
```

- `[SPACE_ROOT]` refers to the root directory where the Eidos space is stored.
- `[theme-name]` is the unique ID/name of your custom theme.
- `theme.css` is the core stylesheet defining the CSS variables.

## Creating and Activating a Theme

To create or modify an Eidos theme:

1. **Locate Space Root**: Determine the root path of the space you are meant to work with.
2. **Setup Folder**: Navigate to `.eidos/themes/` relative to the space root. If you are creating a new theme, make a new directory folder named after the theme (e.g., `my-custom-theme`).
3. **Write `theme.css`**: Create or edit the `theme.css` inside the theme folder.
   *The `theme.css` must provide CSS color variables using `hsl()` values for both light mode (`:root`) and dark mode (`.dark`).*
4. **Activate / Use Theme via CLI**: Once the files are created or modified, execute the activation command using the Eidos CLI tool.
   ```bash
   eidos theme use <theme-name>
   ```
   *(If you wish to reset any applied theme and revert to default, run `eidos theme use` without arguments).*

Other helpful CLI commands for validating themes exist:
- `eidos theme list` (Find installed themes)
- `eidos theme current` (View active theme)

## Theme Structure & Variables

Use the reference file [themes.md](references/themes.md) for the complete list of required structure and common CSS variables. Do not guess what CSS colors/variables are supported; always refer to `themes.md`.

You can also rely on the [theme.css](assets/theme.css) included in the `assets/` directory as a fully functional and complete template for building themes.

## Publishing and Sharing

If the user wants to share or publish the theme, remind them that they can contribute the theme along with a `screenshot.png` to the Official Theme Registry (https://github.com/eidos-space/registry) by creating a Pull Request.
