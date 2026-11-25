---
name: riscos-wimp-templates
description: Create or update RISC OS Wimp template descriptions as `TemplateText` files using `riscos-ccres`. Use when an agent needs to build a window template from user-specified windows, follow standard RISC OS dialogue patterns, or copy bundled window template assets such as save boxes into a new template file.
metadata:
  author: gerph@gerph.org
license: MIT
---
# RISC OS Wimp templates

Use this skill when creating or editing Wimp template descriptions stored as `TemplateText`.
The expected workflow is:

1. Decide which window templates the user needs.
2. If the window matches a bundled type, read only that type's reference in `references/` and copy the matching asset from `assets/`.
3. If the window should follow a standard RISC OS pattern rather than a bundled asset, use the `riscos-style` skill and read only the relevant dialogue guidance there.
4. Assemble the required `wimp_window` blocks into a `TemplateText` file.
5. Convert between binary template/resource files and text form with `riscos-ccres`.

## Converting with `riscos-ccres`

- To create `TemplateText` from an `&FEC` Template file, run `riscos-ccres Templates,fec TemplateText`.
- To create an `&FEC` Template file from `TemplateText`, run `riscos-ccres TemplateText Templates,fec`.
- `riscos-ccres` detects the conversion direction from the input file format.

## Bundled window types

- For a fully user-redrawn document window copied from `Templates,fec`, read [references/document.md](references/document.md) and use [assets/window_document.txt](assets/window_document.txt).
- For a simple document or object information window copied from `Templates,fec`, read [references/fileinfo.md](references/fileinfo.md) and use [assets/window_fileinfo.txt](assets/window_fileinfo.txt).
- For a ratio-based scaling popup copied from `Templates,fec`, read [references/magnifier.md](references/magnifier.md) and use [assets/window_magnifier.txt](assets/window_magnifier.txt).
- For a composite multi-page choices window copied from `Templates,fec`, read [references/multichoices.md](references/multichoices.md) and use [assets/window_multichoices.txt](assets/window_multichoices.txt) with [assets/window_mutlichoices_pane.txt](assets/window_mutlichoices_pane.txt).
- For a standard save box copied from `Templates,fec`, read [references/savebox.md](references/savebox.md) and use [assets/window_savebox.txt](assets/window_savebox.txt).
- For a modified-document close confirmation copied from `Templates,fec`, read [references/close.md](references/close.md) and use [assets/window_close.txt](assets/window_close.txt).
- For an iconbar-menu program information window copied from `Templates,fec`, read [references/proginfo.md](references/proginfo.md) and use [assets/window_proginfo.txt](assets/window_proginfo.txt).
- For a modified-document quit confirmation copied from `Templates,fec`, read [references/quit.md](references/quit.md) and use [assets/window_quit.txt](assets/window_quit.txt).

## Supporting layout references

- For standard ordinary-window defaults, grouped-box spacing, and practical grey-colour notes, read [references/window_defaults.md](references/window_defaults.md).
- For grouped icon boxes, read [references/icons_grouped.md](references/icons_grouped.md).
- For grouped radio-icon sets, read [references/icons_groupedradios.md](references/icons_groupedradios.md).
- For colour-selector label, swatch, and menu-button placement, read [references/icons_colourselector.md](references/icons_colourselector.md).
- For a compact four-choice radio-icon layout, read [references/icons_compactradios.md](references/icons_compactradios.md).
- For a label, value field, and chooser/menu button row, read [references/icons_menuselector.md](references/icons_menuselector.md).
- For a slider-style selector with decrement and increment arrows, read [references/icons_sliderselector.md](references/icons_sliderselector.md).
- For a numeric selector with bump icons and a units suffix, read [references/icons_numericselector.md](references/icons_numericselector.md).
- For the standard bottom-of-dialogue action-button row with a divider and right-aligned default button, read [references/icons_dialoguebuttons.md](references/icons_dialoguebuttons.md).
- For option icons that toggle between off and on states, read [references/icons_option.md](references/icons_option.md).
- For a simple label-plus-display informational row, read [references/icons_infobox.md](references/icons_infobox.md).
- For a label-plus-arbitrary-input row, read [references/icons_input.md](references/icons_input.md).

## Output rules

- Keep each bundled asset as a complete `wimp_window` block that can be copied into a larger `TemplateText` file.
- Preserve the icon order from the source template and record icon numbers in the matching reference file.
- Any plain text longer than `11` characters should normally be encoded as indirected text, even for static labels, to avoid template-string truncation.
- When laying out a dialogue, measure the content spacing from the visible work area, not from the outer title bar or screen position.
- For simple stacked dialogue content, balance the vertical layout so the gap from the top of the visible work area to the first row matches the gap from the last content row to the divider or button-row separator.
- Keep related clickable icons in the same logical set the same width and height where practical, usually by sizing the whole set to the largest required hit area, except where differing control styles are intentionally signalling different actions.
- Do not normalise paired `R5`/`R6` buttons to the same size; check the style-guide sizing rules for those button types first.
- Prefer one reference file per window type so only the relevant window description is loaded.
- When the user asks for multiple windows, combine only the required assets instead of loading every reference.

## Maintaining this skill

When adding a new window type to the skill, read [references/updating-the-skill.md](references/updating-the-skill.md) and follow that process exactly.
